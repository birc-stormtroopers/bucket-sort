"""Module for bucket sorting."""

from typing import Any, Iterable
from itertools import tee


def max_key(keys: Iterable[int]) -> int:
    """
    Give us the maximum value in keys, but handle empty iterators.

    This really is just max(keys) but in a version where max([])
    is defined to return -1. That works well with how we use
    the maximal key in count_keys().

    Runs in O(1) space and O(len(keys)) time.

    >>> max_key([])
    -1
    >>> max_key([1, 4, 3, 2])
    4
    """
    m = -1
    for k in keys:
        m = max(m, k)
    return m


def count_keys(keys: Iterable[int]) -> list[int]:
    """
    Count how many times we see each key in `keys`.

    We assume that all elements in `keys` are
    non-negative. This is not a requirement for
    bucket sort in general--it can handle negative
    numbers--but it is a little more complicated and
    we will keep it simple here. We can play with negative
    number another day.

    We return a list, `counts`. The list has
    `len(counts) == max(keys) + 1` so we can index into
    any key (including those that might not be included in
    `keys`) and for each key `0 <= k <= max(keys)`
    `counts[k]` is the number of times `k` occurs in `x`.

    Unlike the CTiB exercise, this implementation takes
    an iterator as input so we can use it with generator
    expressions and thus generate all keys from more
    complex objects in O(1) space (see the bucket sort
    algorithms below).

    The function runs in O(len(keys)+max(keys)) time
    and O(max(keys)) space; the max(keys) because we need
    to create the counts array of length max(keys) + 1.
    In many cases, keys are bounded by a constant, in which
    case the O(max(keys)) = O(1) and we run in O(len(keys))
    time and O(1) space.

    >>> count_keys([1, 2, 2, 1, 4])
    [0, 2, 2, 0, 1]
    """
    # We need to tee the iterator so we can run through
    # the keys twice. If we didn't, generator expressions
    # would be consumed in the max_key() call.
    keys, max_keys = tee(iter(keys), 2)
    no_keys = max_key(max_keys) + 1
    counts = [0] * no_keys
    for k in keys:
        counts[k] += 1
    return counts


def count_sort(x: list[int]) -> list[int]:
    """
    Sort the values in x using count sort.

    The values in x must satisfy the constraints
    mentioned in `count_keys()`.

    >>> count_sort([])
    []
    >>> count_sort([1, 2, 1, 2, 4])
    [1, 1, 2, 2, 4]
    """
    i, counts, out = 0, count_keys(x), [0] * len(x)
    for k, count in enumerate(counts):
        out[i:i+count] = [k] * count
        i += count
    return out


def cumsum(x: list[int]) -> list[int]:
    """
    Calculate the cumulative sum of x.

    The cumsum is computed in-place and the result is
    placed in x. This means that cumsum runs in O(1)
    space and O(len(x)) time.

    We return x for usage convinience.

    >>> cumsum([1, 2, 3])
    [0, 1, 3]
    >>> cumsum([0, 2, 2, 0, 1])
    [0, 0, 2, 4, 4]
    """
    acc = 0
    for i, v in enumerate(x):
        x[i] = acc
        acc += v
    return x


def bucket_sort(x: list[tuple[int, Any]]) -> list[tuple[int, Any]]:
    """
    Sort the keys and values in x using bucket sort.

    The keys in x must satisfy the constraints
    mentioned in `count_keys()`.

    >>> bucket_sort([])
    []
    >>> bucket_sort([(1, "a"), (2, "b"), (1, "c"), (2, "d"), (4, "e")])
    [(1, 'a'), (1, 'c'), (2, 'b'), (2, 'd'), (4, 'e')]
    """
    buckets = cumsum(count_keys(k for k, _ in x))
    out = [(0, None)] * len(x)
    for k, v in x:
        out[buckets[k]] = (k, v)
        buckets[k] += 1
    return out


def inplace1(x: list[tuple[int, Any]]) -> list[tuple[int, Any]]:
    """
    Sort the keys and values in x using bucket sort.

    The sort is done inplace so the only additional memory we use is
    that necessary for the bucket counts.

    We return x for convinience.

    >>> inplace1([])
    []
    >>> y = inplace1([(1, "a"), (2, "b"), (1, "c"), (2, "d"), (4, "e")])
    >>> [k for k, _ in y]
    [1, 1, 2, 2, 4]
    """
    buckets = cumsum(count_keys(k for k, _ in x))
    cur_buckets = buckets.copy()

    for i, (k, _) in enumerate(x):
        while not (buckets[k] <= i < cur_buckets[k]):
            # We must swap x[i] to its correct bucket
            x[i], x[cur_buckets[k]] = x[cur_buckets[k]], x[i]
            cur_buckets[k] += 1
            k, _ = x[i]  # get key for new value in x[i]

    return x


def inplace2(x: list[tuple[int, Any]]) -> list[tuple[int, Any]]:
    """
    Sort the keys and values in x using bucket sort.

    The sort is done inplace so the only additional memory we use is
    that necessary for the bucket counts.

    We return x for convinience.

    >>> inplace2([])
    []
    >>> y = inplace2([(1, "a"), (2, "b"), (1, "c"), (2, "d"), (4, "e")])
    >>> [k for k, _ in y]
    [1, 1, 2, 2, 4]
    """
    buckets = cumsum(count_keys(k for k, _ in x))
    for i, (k, _) in enumerate(x):
        # If we only swap down, we know that we never handle
        # an entry already placed in its bucket
        while i > buckets[k]:
            x[i], x[buckets[k]] = x[buckets[k]], x[i]
            buckets[k] += 1
            k, _ = x[i]
    return x
