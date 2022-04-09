# Experimenting with bucket sort

This repo contains a bit of code for learning about count and bucket sort. It isn't a proper lesson, so adjust your expectations, but if you look at the `python` directory then there really is an exercise (and my own solution to it, if you feel lazy today).

If you have had CTiB or GSA, you will already have seen these techniques for sorting, although the CTiB version was a simple but inefficient Python version. Here, we can explore how the techniques really work [1].

## Count and bucket sort

Both algorithms aim at sorting some set of values according to a key that is a small non-negative integer. You *can* use them to sort more complex objects, and they should be in your programming arsenal for that, but we can talk about that another day if you are interested. Here, we'll just assume that we have one of two situations. Either you have some sequence of `n` small integers `[ k1, k2, k3, ..., kn ]` or you have key-value pairs `[ (k1,v1), (k2,v2), (k3, v3), ..., (kn,vn) ]` where we for all keys `k` we have `0 <= k < K` for some `K`.

In the first case we want to produce a sequence `[ k1', k2', ..., kn' ]` that is the keys `[ k1, k2, k3, ..., kn ]` in sorted order. (And you know what sorted means).

In the second case, you want to produce a permutation of the key-value pairs `[ (k1,v1), (k2,v2), (k3, v3), ..., (kn,vn) ]` `[ (k1',v1'), (k2',v2'), ..., (kn',vn') ]` where they keys are in sorted order.

The first case is particularly easy, exactly because the keys are small non-negative integers. That means that we can efficiently (in time `O(n+K)` and space `O(K)`) build a table that maps each `k`, `0 <= k < K`, to the number of occurrences of `k` in the input. For example, if our input were `[1, 2, 1, 1, 2, 2, 1, 4, 1]` we would map

```
0 -> 0
1 -> 5
2 -> 3
3 -> 0
4 -> 1
```

with `K == 5`. Since we are indexing with small integers, a natural representation of such a map, with minimal overhead, is an array `[0, 5, 3, 0, 1]`.

If we have a count of our input keys we already know what the output should be. If there are zero 0s we start with putting zero 0s in the output. Then, if there are 5 1s we put five ones in the output. We then have 3 2s, so we put three twos, and so on.

![Count sort](figs/bucket-sort/Count-sort.png)

We don't need to know anything about the input except for how many times we have each key to correctly construct the output. Since we only use counts, this algorithm is called *count sort*.

The second case is slightly more complicated. It is not enough just to output the right number of keys, we need to output the right values as well, and in the right order, and values can be arbitrarily more complicated than the keys. Still, the output will come in blocks (called buckets) of the same key. If you have the same keys as above, just with associated values, you would still get a block of five key-value pairs where the keys are 1, then a block of three key-value pairs where the key is 2, and then finally a single pair with the key 4.

![Bucket sort](figs/bucket-sort/Bucket-sort.png)



## Stable and unstable sorting

When we have key-value pairs, the same key might appear with more than one value, `(ki,vi)` and `(kj,vj)` with `ki == kj`. Sorting the pairs tells us that if `ki < kj` then `(ki,vi)` must come before `(kj,vj)` but if `ki == kj` we haven't put any restrictions on the order of pairs with the same key. Sometimes, however, that is useful, and we say that a sorting algorithm is *stable* if when `ki == kj` and index `i` < `j`, then `(ki,vi)` comes before `(kj,vj)`. That is, the sort is stable if pairs with the same keys come in the same order in the output as they have in the input.



----

[1] The kind of bucket sort we consider here is really called a *histogram sort*. The more general bucket sort isn't guaranteed to run in linear time, as it splits keys into buckets and then needs to sort the buckets using some other method. We ignore the second part, since in bioinformatics we most frequently sort things where the second step isn't needed. Still, now you know that if you hear people talk about bucket sort as something else than what you see here, they might not be wrong. We are just looking at a specific kind of bucket sort.
