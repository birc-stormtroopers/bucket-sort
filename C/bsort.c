#include "bsort.h"
#include <stdio.h>
#include <string.h>

static size_t max_key(size_t n, unsigned int const keys[n])
{
    unsigned int max = 0;
    for (size_t i = 0; i < n; i++)
        max = (max < keys[i]) ? keys[i] : max;
    return max;
}

static inline size_t no_buckets(size_t n, unsigned int const keys[n])
{
    return (n == 0) ? 0 : (max_key(n, keys) + 1);
}

static void compute_buckets(size_t k, unsigned int buckets[k],
                            size_t n, const unsigned int keys[n])
{
    // Count the keys
    memset(buckets, 0, k * sizeof *buckets);
    for (size_t i = 0; i < n; i++)
        buckets[keys[i]]++;

    // Then compute the cumulative sum
    unsigned int acc = 0, b;
    for (size_t i = 0; i < k; i++)
    {
        b = buckets[i];
        buckets[i] = acc;
        acc += b;
    }
}

void bsort_order(size_t n,
                 const unsigned int keys[n],
                 size_t order[n])
{
    size_t k = no_buckets(n, keys);
    unsigned int *buckets = malloc(k * sizeof *buckets);

    // Copy the indices into tmp in sorted order.
    compute_buckets(k, buckets, n, keys);
    for (size_t i = 0; i < n; i++)
        order[buckets[keys[i]]++] = i;

    free(buckets);
}
