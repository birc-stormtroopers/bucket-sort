#include "bsort.h"
#include <assert.h>
#include <stdio.h>

static void random_keys(size_t n, unsigned int keys[n])
{
    for (size_t i = 0; i < n; i++)
        keys[i] = rand() % 10; // keys in 0, ..., 9
}

static void test_bsort_order(void)
{
    size_t n = 50;
    unsigned int keys[n];
    size_t order[n];
    for (int rep = 0; rep < 10; rep++)
    {
        random_keys(n, keys);
        bsort_order(n, keys, order);
        for (size_t i = 1; i < n; i++)
        {
            assert(keys[order[i - 1]] <= keys[order[i]]);
        }

        reorder(n, keys, order);
        for (size_t i = 1; i < n; i++)
        {
            assert(keys[i - 1] <= keys[i]);
        }
    }
}

static void test_inplace(void)
{
    size_t n = 50;
    unsigned int keys[n];
    struct data x[n];
    for (int rep = 0; rep < 10; rep++)
    {
        random_keys(n, keys);
        for (size_t i = 0; i < n; i++)
        {
            x[i].key = keys[i];
        }
        inplace_bsort(n, x);
        for (size_t i = 1; i < n; i++)
        {
            assert(x[i - 1].key <= x[i].key);
        }
    }
}

int main(void)
{
    test_bsort_order();
    test_inplace();
    return 0;
}
