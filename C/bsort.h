#ifndef BSORT_H
#define BSORT_H

#include <stdlib.h>

/*
 * Given the keys, put the order they have when
 * sorted into the order[n] buffer.
 */
void bsort_order(size_t n,
                 const unsigned int keys[n],
                 size_t order[n]);

// Rearrange x according to order
void reorder(size_t n, unsigned int x[n], const size_t order[n]);

// In-place sorting keys and values

struct data // Some fake example data
{
    unsigned int key;
    // pretend that there is more data here...
};
void inplace_bsort(size_t n, struct data x[n]);

#endif // BSORT_H
