# Bucket sorting in C

The basic bucket sort algorithms are quite easy to implement in C. They don't use any advanced langauge features, and C isn't much harder to use when you are just manipulating buffers of memory (although it can be a bit tricky when you also need to handle memory allocation and deallocation, but there isn't much of that in bucket sort).

C doesn't have built-in tuples or pairs, so thinking in key-value pairs is less straightforward. For any real application, the key-value pairs would be some structures anyway, but to get you started reading C code I will consider a simpler situation amd show you an alternative way of thinking about sorting. Instead of sorting an array of elements, we can compute the *order* they have. By that I mean computing an array `order` of indices into the array such that if I run through the indices as they are in `order` I would get the original elements in sorted order.

If you look at the `bsort_order()` function in `bsort.c` it takes three arguments: the length of the input (we can't get the length of arrays directly in C as they are just blocks of memory), the keys we want to sort with, and buffer to write the order in.

```C
void bsort_order(size_t n,
                 const unsigned int keys[n],
                 size_t order[n])
{
    // Figure out how large the buckets array should be
    size_t k = no_buckets(n, keys);
    // Allocate memory for the buckets (we have to free this later)
    unsigned int *buckets = malloc(k * sizeof *buckets);

    // Copy the indices into tmp in sorted order.
    compute_buckets(k, buckets, n, keys);
    for (size_t i = 0; i < n; i++)
        order[buckets[keys[i]]++] = i;

    free(buckets);
}
```

After we have computed the order, we can get the keys in sorted order

```C
    for (size_t i = 1; i < n; i++)
        assert(keys[order[i - 1]] <= keys[order[i]]);
```

We are not looking at the actual values anywhere since the keys suffice to give us their order.

Even though we don't allocate memory (beyond that which we need for the buckets) the function isn't really in-place. We still need memory for the `order` array, we just don't allocate it in the function but expect the caller to have allocated it for us.

We are also doing slightly less than the full bucket sort. If we needed to rearrange the data after we get the order, we would need a helper-buffer to move from the original array into a new, ordered, array witout overwriting things we haven't copied yet.

```C
void reorder(size_t n, unsigned int x[n], const size_t order[n])
{
    unsigned int *y = malloc(n * sizeof *y);

    // Place the elements in y without overwriting anything in x
    for (size_t i = 0; i < n; i++)
        y[i] = x[order[i]];
    // then copy the result back into x
    for (size_t i = 0; i < n; i++)
        x[i] = y[i];

    free(y);
}
```

Without the helper buffer, there is a lot of bookkeeping we need to do so we don't delete a value we need to copy later, and we end up in the same situation as where we make in-place but unstable sorting algorithms.

The `bsort_order()` function *could* return a freshly allocated chunk of memory for `order`, so the caller didn't have to, but memory management is hard, and the fewer funtions you do it in the better. By making the caller responsible for allocating the `order` memory we make it easier for ourselves here, and we reduce the risk of confusion about whether `order` should be freed later. If the caller allocates `order`, he should know that he also needs to free it.

To show you that the inplace functions aren't more complicated in C, I have included one of those as well. Here, to make it non-trivial (and having only keys that I can sort with count-sort anyway) I have added a data structure with keys and data, and we will sort an array of those. (The implementation is in `inplace.c`).

```C
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
```
