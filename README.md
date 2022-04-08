# Experimenting with bucket sort

This repo contains a bit of code for learning about count and bucket sort. It isn't a proper lesson, so adjust your expectations, but if you look at the `python` directory then there really is an exercise (and my own solution to it, if you feel lazy today).





The kind of bucket sort we consider here is really called a *histogram sort*. The more general bucket sort isn't guaranteed to run in linear time, as it splits keys into buckets and then needs to sort the buckets using some other method. We ignore the second part, since in bioinformatics we most frequently sort things where the second step isn't needed. Still, now you know that if you hear people talk about bucket sort as something else than what you see here, they might not be wrong. We are just looking at a specific kind of bucket sort.
