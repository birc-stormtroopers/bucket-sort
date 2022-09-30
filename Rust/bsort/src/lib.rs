use std::{iter, slice::SliceIndex};

fn count_keys(keys: impl Iterator<Item = usize>) -> Vec<usize>{
    let (_, upper_bound) = if let (lower_bound, Some(upper_bound)) = keys.size_hint() { (lower_bound, upper_bound) } else { panic!("We cannot find an upper bound to the iterator") };
    let mut counts = vec![0 as usize; upper_bound];  
    for k in keys{
        counts[k] += 1 
    }
    return counts
}

fn count_sort(x: Vec<usize>) -> Vec<usize>{
    let mut i = 0 as usize;
    let mut out = vec![0 as usize; x.len()];
    let counts = count_keys(x.into_iter());
    for (k, count) in counts.iter().enumerate(){
        for (j, value) in iter::repeat(k).take(*count).enumerate(){
            out[i+j] = value;
        }
        i += count;
    }
    return out
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn count_keys_works() {
        let result = count_keys(vec![1, 2, 2, 1, 4].into_iter());
        assert_eq!(result, vec![0, 2, 2, 0, 1]);
    }
    #[test]
    fn count_sort_works() {
        let result = count_sort(vec![1, 2, 1, 2, 4]);
        assert_eq!(result, vec![1, 1, 2, 2, 4]);
    }
}