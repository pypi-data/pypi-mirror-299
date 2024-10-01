use itertools::{enumerate, izip};
use num_traits::{Float, FromPrimitive};
use numpy::ndarray::{ArrayView1, ArrayView2, Axis, ScalarOperand};
use std::{
    cell::UnsafeCell,
    fmt::{Debug, Display},
    iter::zip,
    mem,
    ops::{AddAssign, MulAssign, SubAssign},
    ptr,
    thread::available_parallelism,
};

#[derive(Copy, Clone)]
pub struct UnsafeSlice<'a, T> {
    slice: &'a [UnsafeCell<T>],
}
unsafe impl<'a, T: Send + Sync> Send for UnsafeSlice<'a, T> {}
unsafe impl<'a, T: Send + Sync> Sync for UnsafeSlice<'a, T> {}
impl<'a, T> UnsafeSlice<'a, T> {
    pub fn new(slice: &'a mut [T]) -> Self {
        let ptr = slice as *mut [T] as *const [UnsafeCell<T>];
        Self {
            slice: unsafe { &*ptr },
        }
    }

    pub fn shadow(&mut self) -> Self {
        Self { slice: self.slice }
    }

    pub fn slice(&self, start: usize, end: usize) -> Self {
        Self {
            slice: &self.slice[start..end],
        }
    }

    pub fn set(&mut self, i: usize, value: T) {
        let ptr = self.slice[i].get();
        unsafe {
            ptr::write(ptr, value);
        }
    }

    pub fn copy_from_slice(&mut self, i: usize, src: &[T])
    where
        T: Copy,
    {
        let ptr = self.slice[i].get();
        unsafe {
            ptr::copy_nonoverlapping(src.as_ptr(), ptr, src.len());
        }
    }
}

const CONCAT_GROUP_LIMIT: usize = 4 * 239 * 5000;
type Task<'a, 'b, D> = (Vec<usize>, Vec<ArrayView2<'a, D>>, UnsafeSlice<'b, D>);
#[inline]
fn fill_concat<D: Copy>((offsets, arrays, mut out): Task<D>) {
    offsets.iter().enumerate().for_each(|(i, &offset)| {
        out.copy_from_slice(offset, arrays[i].as_slice().unwrap());
    });
}
pub fn fast_concat_2d_axis0<D: Copy + Send + Sync>(
    arrays: Vec<ArrayView2<D>>,
    num_rows: Vec<usize>,
    num_columns: usize,
    limit_multiplier: usize,
    mut out: UnsafeSlice<D>,
) {
    let mut cumsum: usize = 0;
    let mut offsets: Vec<usize> = vec![0; num_rows.len()];
    for i in 1..num_rows.len() {
        cumsum += num_rows[i - 1];
        offsets[i] = cumsum * num_columns;
    }

    let bumped_limit = CONCAT_GROUP_LIMIT * 16;
    let total_bytes = offsets.last().unwrap() + num_rows.last().unwrap() * num_columns;
    let (mut group_limit, mut tasks_divisor) = if total_bytes <= bumped_limit {
        (CONCAT_GROUP_LIMIT, 8)
    } else {
        (bumped_limit, 1)
    };
    group_limit *= limit_multiplier;

    let prior_num_tasks = total_bytes.div_ceil(group_limit);
    let prior_num_threads = prior_num_tasks / tasks_divisor;
    if prior_num_threads > 1 {
        group_limit = total_bytes.div_ceil(prior_num_threads);
        tasks_divisor = 1;
    }

    let nbytes = mem::size_of::<D>();

    let mut tasks: Vec<Task<D>> = Vec::new();
    let mut current_tasks: Option<Task<D>> = Some((Vec::new(), Vec::new(), out.shadow()));
    let mut nbytes_cumsum = 0;
    izip!(num_rows.iter(), offsets.into_iter(), arrays.into_iter()).for_each(
        |(&num_row, offset, array)| {
            nbytes_cumsum += nbytes * num_row * num_columns;
            if let Some(ref mut current_tasks) = current_tasks {
                current_tasks.0.push(offset);
                current_tasks.1.push(array);
            }
            if nbytes_cumsum >= group_limit {
                nbytes_cumsum = 0;
                if let Some(current_tasks) = current_tasks.take() {
                    tasks.push(current_tasks);
                }
                current_tasks = Some((Vec::new(), Vec::new(), out.shadow()));
            }
        },
    );
    if let Some(current_tasks) = current_tasks.take() {
        if !current_tasks.0.is_empty() {
            tasks.push(current_tasks);
        }
    }

    let max_threads = available_parallelism()
        .expect("failed to get available parallelism")
        .get();
    let num_threads = (tasks.len() / tasks_divisor).min(max_threads * 8).min(512);
    if num_threads <= 1 {
        tasks.into_iter().for_each(fill_concat);
    } else {
        let pool = rayon::ThreadPoolBuilder::new()
            .num_threads(num_threads)
            .build()
            .unwrap();

        pool.scope(move |s| {
            tasks.into_iter().for_each(|task| {
                s.spawn(move |_| fill_concat(task));
            });
        });
    }
}

pub trait AFloat:
    Float
    + AddAssign
    + SubAssign
    + MulAssign
    + FromPrimitive
    + ScalarOperand
    + Send
    + Sync
    + Debug
    + Display
{
}
impl<T> AFloat for T where
    T: Float
        + AddAssign
        + SubAssign
        + MulAssign
        + FromPrimitive
        + ScalarOperand
        + Send
        + Sync
        + Debug
        + Display
{
}

fn mean<T: AFloat>(a: ArrayView1<T>) -> T {
    let mut sum = T::zero();
    let mut num = T::zero();
    for &x in a.iter() {
        if x.is_nan() {
            continue;
        }
        sum += x;
        num += T::one();
    }
    if num.is_zero() {
        T::nan()
    } else {
        sum / num
    }
}

fn corr<T: AFloat>(a: ArrayView1<T>, b: ArrayView1<T>) -> T {
    let valid_indices: Vec<usize> = zip(a.iter(), b.iter())
        .enumerate()
        .filter_map(|(i, (&x, &y))| {
            if x.is_nan() || y.is_nan() {
                None
            } else {
                Some(i)
            }
        })
        .collect();
    if valid_indices.is_empty() {
        return T::nan();
    }
    let a = a.select(Axis(0), &valid_indices);
    let b = b.select(Axis(0), &valid_indices);
    let a_mean = a.mean().unwrap();
    let b_mean = b.mean().unwrap();
    let a = a - a_mean;
    let b = b - b_mean;
    let cov = a.dot(&b);
    let var1 = a.dot(&a);
    let var2 = b.dot(&b);
    cov / (var1.sqrt() * var2.sqrt())
}

pub fn mean_axis1<T: AFloat>(a: &ArrayView2<T>, num_threads: usize) -> Vec<T> {
    let mut res: Vec<T> = vec![T::zero(); a.nrows()];
    let mut slice = UnsafeSlice::new(res.as_mut_slice());
    if num_threads <= 1 {
        enumerate(a.rows()).for_each(|(i, row)| {
            slice.set(i, mean(row));
        });
    } else {
        let pool = rayon::ThreadPoolBuilder::new()
            .num_threads(num_threads)
            .build()
            .unwrap();
        pool.scope(|s| {
            enumerate(a.rows()).for_each(|(i, row)| {
                s.spawn(move |_| slice.set(i, mean(row)));
            });
        });
    }
    res
}

pub fn corr_axis1<T: AFloat>(a: &ArrayView2<T>, b: &ArrayView2<T>, num_threads: usize) -> Vec<T> {
    let mut res: Vec<T> = vec![T::zero(); a.nrows()];
    let mut slice = UnsafeSlice::new(res.as_mut_slice());
    if num_threads <= 1 {
        zip(a.rows(), b.rows()).enumerate().for_each(|(i, (a, b))| {
            slice.set(i, corr(a, b));
        });
    } else {
        let pool = rayon::ThreadPoolBuilder::new()
            .num_threads(num_threads)
            .build()
            .unwrap();
        pool.scope(move |s| {
            zip(a.rows(), b.rows()).enumerate().for_each(|(i, (a, b))| {
                s.spawn(move |_| slice.set(i, corr(a, b)));
            });
        });
    }
    res
}

pub fn searchsorted<T: Ord>(arr: &ArrayView1<T>, value: &T) -> usize {
    arr.as_slice()
        .unwrap()
        .binary_search(value)
        .unwrap_or_else(|x| x)
}

pub fn batch_searchsorted<T: Ord>(arr: &ArrayView1<T>, values: &ArrayView1<T>) -> Vec<usize> {
    values
        .iter()
        .map(|value| searchsorted(arr, value))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn assert_allclose<T: AFloat>(a: &[T], b: &[T]) {
        let atol = T::from_f64(1e-6).unwrap();
        let rtol = T::from_f64(1e-6).unwrap();
        a.iter().zip(b.iter()).for_each(|(&x, &y)| {
            assert!(
                (x - y).abs() <= atol + rtol * y.abs(),
                "not close - x: {:?}, y: {:?}",
                x,
                y
            );
        });
    }

    macro_rules! test_fast_concat_2d_axis0 {
        ($dtype:ty) => {
            let array_2d_u = ArrayView2::<$dtype>::from_shape((1, 3), &[1., 2., 3.]).unwrap();
            let array_2d_l =
                ArrayView2::<$dtype>::from_shape((2, 3), &[4., 5., 6., 7., 8., 9.]).unwrap();
            let arrays = vec![array_2d_u, array_2d_l];
            let mut out: Vec<$dtype> = vec![0.; 3 * 3];
            let out_slice = UnsafeSlice::new(out.as_mut_slice());
            fast_concat_2d_axis0(arrays, vec![1, 2], 3, 1, out_slice);
            assert_eq!(out.as_slice(), &[1., 2., 3., 4., 5., 6., 7., 8., 9.]);
        };
    }

    macro_rules! test_mean_axis1 {
        ($dtype:ty) => {
            let array =
                ArrayView2::<$dtype>::from_shape((2, 3), &[1., 2., 3., 4., 5., 6.]).unwrap();
            let out = mean_axis1(&array, 1);
            assert_allclose(out.as_slice(), &[2., 5.]);
            let out = mean_axis1(&array, 2);
            assert_allclose(out.as_slice(), &[2., 5.]);
        };
    }

    macro_rules! test_corr_axis1 {
        ($dtype:ty) => {
            let array =
                ArrayView2::<$dtype>::from_shape((2, 3), &[1., 2., 3., 4., 5., 6.]).unwrap();
            let out = corr_axis1(&array, &(&array + 1.).view(), 1);
            assert_allclose(out.as_slice(), &[1., 1.]);
            let out = corr_axis1(&array, &(&array + 1.).view(), 2);
            assert_allclose(out.as_slice(), &[1., 1.]);
        };
    }

    #[test]
    fn test_fast_concat_2d_axis0_f32() {
        test_fast_concat_2d_axis0!(f32);
    }
    #[test]
    fn test_fast_concat_2d_axis0_f64() {
        test_fast_concat_2d_axis0!(f64);
    }

    #[test]
    fn test_mean_axis1_f32() {
        test_mean_axis1!(f32);
    }
    #[test]
    fn test_mean_axis1_f64() {
        test_mean_axis1!(f64);
    }

    #[test]
    fn test_corr_axis1_f32() {
        test_corr_axis1!(f32);
    }
    #[test]
    fn test_corr_axis1_f64() {
        test_corr_axis1!(f64);
    }

    #[test]
    fn test_searchsorted() {
        let array = ArrayView1::<i64>::from_shape(5, &[1, 2, 3, 5, 6]).unwrap();
        assert_eq!(searchsorted(&array, &0), 0);
        assert_eq!(searchsorted(&array, &1), 0);
        assert_eq!(searchsorted(&array, &3), 2);
        assert_eq!(searchsorted(&array, &4), 3);
        assert_eq!(searchsorted(&array, &5), 3);
        assert_eq!(searchsorted(&array, &6), 4);
        assert_eq!(searchsorted(&array, &7), 5);
        assert_eq!(batch_searchsorted(&array, &array), vec![0, 1, 2, 3, 4]);
    }
}
