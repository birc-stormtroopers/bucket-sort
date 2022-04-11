#include "bsort.h"
#include <stdio.h>
#include <string.h>

// We cannot reuse these functions from bsort_order because the data structures have changed
// and C doesn't have much (if any) way of handling polymorphic data.
static size_t max_key(size_t n, struct data x[n])
{
    unsigned int max = 0;
    for (size_t i = 0; i < n; i++)
        max = (max < x[i].key) ? x[i].key : max;
    return max;
}

static inline size_t no_buckets(size_t n, struct data x[n])
{
    return (n == 0) ? 0 : (max_key(n, x) + 1);
}

static void compute_buckets(size_t k, unsigned int buckets[k],
                            size_t n, struct data x[n])
{
    // Count the keys
    memset(buckets, 0, k * sizeof *buckets);
    for (size_t i = 0; i < n; i++)
        buckets[x[i].key]++;

    // Then compute the cumulative sum
    unsigned int acc = 0, b;
    for (size_t i = 0; i < k; i++)
    {
        b = buckets[i];
        buckets[i] = acc;
        acc += b;
    }
}

// Swap two pieces of data that we have pointers to.
// When we know their addresses, we don't have to care about
// which array they sit in, in any, we can always just swap.
static inline void swap(struct data *a, struct data *b)
{
    struct data tmp = *a;
    *a = *b;
    *b = tmp;
}

// Macros let us simplify the main code a little bit...
// Side-effects can be dangerous, like incrementing twice or such
// but the macros are simple and safe here.
#define BUCKET(i) (buckets[x[i].key])
#define SWAP_TO_BUCKET(i) swap(&x[i], &x[BUCKET(i)++])

void inplace_bsort(size_t n, struct data x[n])
{
    size_t k = no_buckets(n, x);
    unsigned int *buckets = malloc(k * sizeof *buckets);

    compute_buckets(k, buckets, n, x);
    for (size_t i = 0; i < n; i++)
        while (i >= BUCKET(i))
            SWAP_TO_BUCKET(i);

    free(buckets);
}
