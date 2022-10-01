use std::{iter, any::Any};

fn count_keys<'a>(keys: impl Iterator<Item = &'a usize>) -> Vec<usize> {
    let (_, upper_bound) = if let (lower_bound, Some(upper_bound)) = keys.size_hint() {
        (lower_bound, upper_bound)
    } else {
        panic!("We cannot find an upper bound to the iterator")
    };
    let mut counts = vec![0 as usize; upper_bound];
    for k in keys {
        counts[*k] += 1
    }
    return counts;
}

fn count_sort(x: Vec<&usize>) -> Vec<usize> {
    let mut i = 0 as usize;
    let mut out = vec![0 as usize; x.len()];
    let counts = count_keys(x.into_iter());
    for (k, count) in counts.iter().enumerate() {
        for (j, value) in iter::repeat(k).take(*count).enumerate() {
            out[i + j] = value;
        }
        i += count;
    }
    return out;
}
fn cumsum(x: Vec<usize>) -> Vec<usize> {
    let mut out = vec![0 as usize; x.len()];
    for i in 1..x.len(){
         out[i] = out[i-1] + x[i-1]
    }   
    return out
}

fn bucket_sort_inplace<T: Any>(mut keys: Vec<usize>, mut values: Vec<T>) -> (Vec<usize>, Vec<T>){
    let mut buckets = cumsum(count_keys(keys.iter()));
    for (i, mut k) in keys.to_owned().into_iter().enumerate(){
        while i > buckets[k]{
            values.swap(i, buckets[k]);
            keys.swap(i, buckets[k]);
            buckets[k] += 1;
            k = keys[i];
        }               
    }
    return (keys, values)
}

fn bucket_sort<T: Any + Copy>(keys: Vec<usize>, values: Vec<T>) -> (Vec<usize>, Vec<T>){
    let mut buckets = cumsum(count_keys(keys.iter()));
    let mut sorted_values = values.to_owned();
    let mut sorted_keys = keys.to_owned();
    for (i, k) in keys.iter().enumerate(){
        sorted_values[buckets[*k]] = values[i];
        sorted_keys[buckets[*k]] = keys[i];
        buckets[*k] += 1
    }
    return (sorted_keys, sorted_values)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn count_keys_works() {
        let result = count_keys(vec![&1, &2, &2, &1, &4].into_iter());
        assert_eq!(result, vec![0, 2, 2, 0, 1]);
    }
    #[test]
    fn count_sort_works() {
        let result = count_sort(vec![&1, &2, &1, &2, &4]);
        assert_eq!(result, vec![1, 1, 2, 2, 4]);
    }
    #[test]
    fn cumsum_works_with_unique_values() {
        let result = cumsum(vec![1, 2, 3]);
        assert_eq!(result, vec![0, 1, 3]);
    }    
    #[test]
    fn cumsum_works_with_non_unique_values() {
        let result = cumsum(vec![0, 2, 2, 0, 1]);
        assert_eq!(result, vec![0, 0, 2, 4, 4]);
    }
    #[test]
    fn bucket_sort_inplace_works() {
        let keys = vec![1, 2, 1, 2, 4];
        let values = vec!['a', 'b', 'c', 'd', 'e'];
        let (result, _) = bucket_sort_inplace(keys, values);
        assert_eq!(
            result,
            vec![1, 1, 2, 2, 4]);
    }
    #[test]
    fn bucket_sort_works() {
        let keys = vec![1, 2, 1, 2, 4];
        let values = vec!['a', 'b', 'c', 'd', 'e'];
        let (result_keys, result_values) = bucket_sort(keys, values);
        assert_eq!(result_keys,vec![1, 1, 2, 2, 4]);
        assert_eq!(result_values, vec!['a', 'c', 'b', 'd', 'e']);
    }        
    }

