fn count_keys(keys: impl Iterator<Item = usize>) -> Vec<usize>{
    let (_, upper_bound) = if let (lower_bound, Some(upper_bound)) = keys.size_hint() { (lower_bound, upper_bound) } else { panic!("We cannot find an upper bound to the iterator") };
    let mut counts = vec![0 as usize; upper_bound];  
    for k in keys{
        counts[k] += 1 
    }
    return counts
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn count_keys_works() {
        let result = count_keys(vec![1, 2, 2, 1, 4].into_iter());
        assert_eq!(result, vec![0, 2, 2, 0, 1]);
    }
}