#include "bsort.h"
#include <assert.h>
#include <stdio.h>

static void random_keys(size_t n, unsigned int keys[n])
{
    for (size_t i = 0; i < n; i++)
        keys[i] = rand() % 10; // keys in 0, ..., 9
}

typedef void (*order_func)(
    size_t n,
    const unsigned int keys[n],
    size_t order[n]);

static void test_sort(order_func f)
{
    size_t n = 50;
    unsigned int keys[n];
    size_t order[n];
    for (int rep = 0; rep < 1; rep++)
    {
        random_keys(n, keys);
        f(n, keys, order);
        for (size_t i = 1; i < n; i++)
        {
            assert(keys[order[i - 1]] <= keys[order[i]]);
        }
    }
}

int main(void)
{
    test_sort(bsort_order);
    return 0;
}
