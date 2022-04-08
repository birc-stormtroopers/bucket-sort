# Python bucket sorts

In this directory you will find implementations of bucket sort in Python (in `bsort.py` with tests in `test_bsort.py`). You can use them to experiment with.

To run the tests in this directory you can use

```sh
> python3 -m doctest *.py ; python3 -m pytest
```

(if you don't have `pytest` installed, run `python3 -m pip install pytest`).

The code is my solution to an exercise for next term's CTiB. The problem description is listed below, and if you feel up to solving problems from an advanced programming class, then go ahead. It might be a lot more fun than looking at my solution...


# CTiB Exercise

In this exercise we will learn how to implement a more efficient bucket sort. It has the same amortised complexity as the one you have already seen, `O(n + m)` where `n` is the number of elements to sort and `m` is the number of keys (values) you have, but it avoids a lot of data structure overhead and uses less memory. And the good news is that it is only slightly harder to implement than what you have already seen.

To fully understand the distinction between "keys" and "values" when we are sorting--something that we won't have much use for in this class, but you will have to trust me is very important--we consider two cases:

- Sorting a list of integers `x: list[int]` where each is in the range `0 <= x[i] < m`. This is the case where we have only "keys"; and you can probably guess that the values in `x` must then be the keys.
- Sorting a list of pairs `x: list[tuple[int,Any]]` where the first element in the pairs are the keys, in the same range `[0,m)` as the first case, and the second can be any object we associate with that key.

## Count sort

The first case looks simpler than the second, and it is. Here, we can use [*count sort*](https://en.wikipedia.org/wiki/Counting_sort), as you have already seen it. First, you count how many of each key you see. If you go to `src/bsort.py` you will find a template for `count_keys(x)` function. Go and implement it.

With that in hand, you can run through the keys in increasing order, and for each `k` you output `counts[k]` `k`s. That is how many times `x` had a `k`, so you are outputting the right number of them, and if you output them in order, you output the keys in sorted order.

To do this, you can create a block of `counts[k]` `k`s with `[k] * counts[k]` and add them to a list with `out.extend([k] * counts[k])`. So count sort can be as simple as this:

```python
def count_sort(x: list[int]) -> list[int]:
    counts = count_keys(x)
    out = []
    for k, count in enumerate(counts):
        out.extend([k] * count)
    return out
```

Growing a list can be more expensive than pre-allocating one of the right length, though, and in some languages you don't have lists that you can append, so I want to make it just a little more difficult. Implement a `count_sort()` function (see `src/bsort.py`) where you allocate the output list in one go, and then insert the keys in it.

```python
def count_sort(x: list[int]) -> list[int]:
    counts = count_keys(x)
    out = [0] * len(x) # the output has some length as x
    ... # fill out out
    return out
```

This isn't actually going to be more efficient in Python, (it will be a little slower), but if you can do that, you can do a count sort in any language and not just Python.

Now you can do a count sort, and you have most of what you need to implement a bucket sort as well.

## Bucket sort

The kind of bucket sort I want you to implement resembles the `count_sort()` above in that we will allocate an `out` list for the output and that and the key counts is the only extra list we will use. No list of lists to append to or any such thing, just a simple list of integers.

Our input is a list of pairs `x = [(k0,x0), (k1,x1), ..., ]` and we want to rearrange it such that the pairs are sorted with respect to their keys, but in a stable manner, such that pairs with the same key will come out in the same order as they came in.

but how do we move the pairs to their right position?

We will count the keys

```python
counts = count_keys([k for k, _ in x])
```

as before, but we cannot simply output a `count[k]` number of `k`s. We need to copy the right pair to each position.

The key observation is now that the `counts` tell us how large each bucket in the output is. If our keys are `[1, 2, 1, 2, 4]` the counts will be

```
0 => 0  # we don't have any zeros
1 => 2  # we have two 1s
2 => 2  # we have two 2s
3 => 0  # we have zero 3s
4 => 1  # we have one 4
```

which tells us that the output will have a bucket with size 0 for the 0s, then a bucket of size 2 for the 1s, then a bucket of size 2 for the 2s, a bucket of size zero for the 3s, and finally a bucket of size 1 for the 4s.

```
      0s,1s start here
         |     2s start here
         |     |      3,4s start here
         |     |      |
         v     v      v
out = [  1 1   2 2    4  ]
        |-2-| |-2-| |-1-|
```

If you do a cumulative sum of the key counts

```
[0, 2, 2, 0, 1] => [0, 0, 2, 4, 4]
```

(write the function `cumsum()` to do that) then you can get

```python
buckets = cumsum(count_keys([k for k, _ in x]))
```

and `bucket[k]` will tell you at which index in the output the `k` keys will start.

If you now run through `x` and for each pair `(k,v)` you put that pair at `out[bucket[k]]` and increment `bucket[k]` by one, you will have placed all the pairs in their right position.

That is how bucket sort is *really* done.

Try to implement it in the function `bucket_sort()`.

