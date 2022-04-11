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

#endif // BSORT_H
