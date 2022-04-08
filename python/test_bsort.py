"""Testing the bsort module."""

import random
from bsort import (
    count_keys,
    count_sort,
    bucket_sort
)
# the Counter class also counts, but doesn't
# give us sorted keys, so we cannot use it for
# bucket sort. We can use it for testing, though.
from collections import Counter


def test_count_keys() -> None:
    """Test the count_keys() function."""
    for _ in range(10):
        keys = random.sample(range(100), random.randint(1, 10))
        counts = count_keys(keys)
        true_counts = Counter(keys)
        for k, count in enumerate(counts):
            assert count == true_counts[k]


def test_count_sort() -> None:
    """Test the count_sort() function."""
    for _ in range(10):
        x = random.sample(range(100), random.randint(1, 10))
        count_sorted = count_sort(x)
        x.sort()
        assert x == count_sorted


def test_bucket_sort() -> None:
    """Test the bucket_sort() function."""
    for _ in range(10):
        n = random.randint(1, 10)
        vals = list(range(n))
        keys = random.sample(range(100), n)
        x = list(zip(keys, vals))
        bucket_sorted = bucket_sort(x)
        x.sort(key=lambda p: p[0])
        assert x == bucket_sorted
