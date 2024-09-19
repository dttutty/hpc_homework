## Temporal Locality

### Description 

This tutorial discusses temporal locality and its impact on cache performance. Loop tiling is
discussed as a means to exploit temporal locality in programs whose working set does not fit in the
target cache. 

### Outline 

  * [The Working Set](#working_set)
  * [Cache Miss Rates ](#cache)
  * [Loop Tiling](#tiling)
  * [Overall Performance](#performance)
  
  
### <a name="working_set"></a>The Working Set

Consider the following simple code scaling the values in a two-dimensional array by a constant factor. 

```C
int main(int argc, char *argv[]) {                  
  float **a, **b;                                   
                                                    
  int dim = atoi(argv[1]);                          
                                                    
  a = (float **) malloc(sizeof(float *) * dim);     
  b = (float **) malloc(sizeof(float *) * dim);     
                                                    
  int i,j,k;                                        
  for (i = 0; i < dim; i++) {                       
    a[i] = (float *) malloc(sizeof(float) * dim);   
    b[i] = (float *) malloc(sizeof(float) * dim);   
  }                                                 
                                                    
  for (i = 0; i < dim; i++)                         
    for (j = 0; j < dim; j++) {                     
      a[i][j] = 2.3;                                
      b[i][j] = 1.7;                                
    }                                               
                                                    
  float scale = 0.17;                               
  for (k = 0; k < 100; k++)                         
    for (i = 0; i < dim; i++)                       
      for (j = 0; j < dim; j++)                     
        a[i][j] = b[i][j] * scale;                  
                                                    
                                                    
  printf("a[17][17] = %3.2f\n",a[17][17]);          
                                                    
  return 0;                                         
                                                    
}                                                   
```

Each element in `b` is multiplied by `scale` and stored in `a`. The entire scaling operation is
repeated 100 times. 

**How much data is touched between each iteration of the outer _k_ look when dim = 100?**

In each iteration, the code sweeps through the entirety of the `a` and `b` arrays. The size of each
array is 100 x 100 x 4 = 40KB. So the total data accessed between each iteration is 80K. The
program will access the _same_ 80K of data in each of the 100 iterations of the _k_ loop. Programs 
that repeatedly sweep over the same fixed-sized data are said to operate on a _working set_. The
working set exhibits high degrees of temporal locality. In the example above, data corresponding to
`a` and `b` arrays will be brought in from main memory in the first of the _k_. There is
temporal locality on the working set in each of the remaining 99 iterations. Ideally, we want these
accesses to hit in cache. But in order for them to hit in the cache the working set must fit in the
cache. If the working set is larger than the cache, then when we go access the data a second time,
some of the data brought into the cache in the previous iteration will have been evicted from the
cache. 

**Does the working set of this program fit in our L3 cache if dim == 100?**

To answer this question, let's first check out the cache configuration on `knuth`. 

```
(knuth)% getconf -a | grep CACHE
LEVEL1_ICACHE_SIZE                 32768
LEVEL1_ICACHE_ASSOC                8
LEVEL1_ICACHE_LINESIZE             64
LEVEL1_DCACHE_SIZE                 32768
LEVEL1_DCACHE_ASSOC                8
LEVEL1_DCACHE_LINESIZE             64
LEVEL2_CACHE_SIZE                  262144
LEVEL2_CACHE_ASSOC                 8
LEVEL2_CACHE_LINESIZE              64
LEVEL3_CACHE_SIZE                  15728640
LEVEL3_CACHE_ASSOC                 20
LEVEL3_CACHE_LINESIZE              64
LEVEL4_CACHE_SIZE                  0
LEVEL4_CACHE_ASSOC                 0
LEVEL4_CACHE_LINESIZE              0
```

The L1 data cache size is 32K. Clearly the working set does not fit. It will fit in L1 if `dim` is
smaller. On the other hand, it may even exceed L3 for larger values of `dim`


### <a name="cache"></a>Cache Miss Rates 

Let's look at the cache performance of the program for a range of dim sizes. 

```
(knuth)% gcc -o scale scale.c 
(knuth)% ./get_miss_rates.sh scale
500	    0.16%
1000	0.41%
1500	65.42%
2000	97.63%
2500	98.86%
3000	96.23%
3500	98.62%
4000	99.02%
```

We see a spike in the LLC miss rates when dim hits 1500. 

**Can we explain why this is the case?**

The working set size at dim = 1000 is 1000 x 1000 x 4 x 2 = ~ 8 MB which still fits in L3. But at
1500 the working set is 1500 x 1500 x 4 x 2 = ~ 18 MB, which exceeds L3 and causes the
spike. However, even at 18 MB some of the data remain in cache when the program attempts to access
them in the next iteration. When the working set is close to double the size of L3 then all of the
data is evicted between iterations which causes the miss rate to be close to a 100%. 

**Why is the miss rate not 100%?**

Because of spatial locality. 


### <a name="tiling"></a>Loop Tiling

Tiling is one of the most well-known code transformations that can help exploit temporal
locality. The main idea is to break up the working set into smaller _tiles_ such that
each tile fits in the cache. The transformation is a little more complex than the loop interchange
transformation we looked at earlier. 

Let us try to apply tiling to the example code. What we want to do is this: instead of sweeping through
the entire `a` and `b` arrays and then starting on the next iteration of _k_, we will pick a small
tile of `a` and `b` and sweep over it 100 times, and then pick the next small tile and sweep over
that 100 times and so on. To do this first, we will apply a transformation called
strip mining. Strip mining was originally invented for vector machines with different goals. But the
transformation is a good fit as the first step for tiling a loop nest. 

```C
float scale = 0.17;                                                          
int jj;                                                                      
  for (k = 0; k < 100; k++)                                                  
    for (i = 0; i < dim; i++)                                                
	  for (j = 0; j < dim; j = j + BLOCK)                                          
        for (jj = j; jj < (j + BLOCK); jj++)                                   
          a[i][jj] = b[i][jj] * scale;                                         
                                                                               
```


Strip-mining adds a new loop to the nest and is defining the strip (tile) that will be repeatedly
processed. It is saying that we will be processing BLOCK number of columns at a time. 

Now we perform an interchange and move the strip-mined loop all the way to the outside. 

```C
 float scale = 0.17;                                                          
  int jj;                                                                      
  for (j = 0; j < dim; j = j + BLOCK)                                          
    for (k = 0; k < 100; k++)                                                  
      for (i = 0; i < dim; i++)                                                
        for (jj = j; jj < (j + BLOCK); jj++)                                   
          a[i][jj] = b[i][jj] * scale;                                         
                                                                               
  printf("a[17][17] = %3.2f\n",a[17][17]);                                     
```

And that's it! This has the desired. 

Let's see if it improves our cache performance. 

```
(knuth)% gcc -o scale_tiled scale_tiled.c 
(knuth)% ./get_miss_rates.sh scale_tiled 100
500	0.14%
1000	0.08%
1500	0.40%
2000	0.64%
2500	0.68%
3000	0.66%
3500	0.68%
4000	0.67%
```

Cache miss rate does not increase even if we increase the dim size. 

## <a name="performance"></a>Overall Performance

Notice, although we have significant reduction in LLC miss rates, there is not much difference in
overall performance. 

```
(knuth)% time ./scale 2000
(knuth)% time ./scale_tiled 2000 100
```

**Can we explain why this is?**
