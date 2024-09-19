## Spatial Locality 

### Description 

This tutorial discusses spatial locality and its impact on cache performance. Loop interchange is
discussed as a means to exploit spatial locality in programs that operate on multi-dimensional arrays. 

### Regular vs Irregular Access 

Consider the following code for copying a segment of an integer array into another array. 

```C++
  int N = atoi(argv[1]);                            
  int M = atoi(argv[2]);                            
                                                    
  int *a, *b;                                       
                                                    
  a = (int *) malloc(sizeof(int) * N);              
  b = (int *) malloc(sizeof(int) * M);              
                                                    
  for (unsigned i = 0; i < N; i++)                  
    a[i] = rand() / (double) (RAND_MAX/VAL_RANGE);  
                                                    
  for (unsigned i = 0; i < M; i++)                  
    b[i] = a[i];                                    
```


Let's run the code and look at its performance. 

```
(knuth)% g++ -o array_copy array_copy.cpp
(knuth)% time ./array_copy 10000000 1000000
PASS

real	0m0.206s
user	0m0.190s
sys     0m0.016s
```

Now let's look at a convoluted (and inefficient) way of copying an array segment. 

```C++
int get_rand(bool *rands, int range) {              
  int rand_num;                                     
  do                                                
    rand_num = rand() % range;                      
  while(rands[rand_num]);                           
  rands[rand_num] = true;                           
  return rand_num;                                  
}                                                   


  bool *rands = (bool *) malloc(sizeof (bool) * M); 
  for (unsigned i = 0; i < M; i++)                  
    rands[i] = false;                               
                                                    
  for (unsigned i = 0; i < N; i++)                  
    a[i] = rand() / (double) (RAND_MAX/VAL_RANGE);  
                                                    
  for (unsigned i = 0; i < M; i++) {                
    int j = get_rand(rands, M);                     
    b[i] = a[j];                                    
  }                                                 
                                                    
```

Rather than going through the array sequentially, the above code randomly selects the elements to be
copied into `b`. The length of the array segment remains the same and it has a check to make sure
that same element is not copied more than once. 

Let's run this code and look at its performance. 

```
(knuth)% g++ -o array_copy_rand array_copy_rand.cpp
(knuth)% time ./array_copy_rand 10000000 1000000
FAIL

real	0m0.492s
user	0m0.472s
sys     0m0.020s
```

The random copy takes more than twice as long. Comparing the overall performance of these two codes
is not totally fair. The random version is doing more work with calls to `rand()` and storing values
in an  auxiliary array. We can however, get a sense of how well they are exploiting locality by looking at
the cache performance. 

```
(knuth)% get_L1_miss_rates.sh ./array_copy 10000000 1000000
L1 load miss rate (miss/access): 	    0.0040
L1 store miss rate (miss/access): 	    0.0060
(knuth)% get_L1_miss_rates.sh ./array_copy_rand 10000000 1000000
L1 load miss rate (miss/access): 	    0.0277
L1 store miss rate (miss/access): 	    0.0064
```

Although the L1 miss rates are relatively low, the random access code's load miss rate is almost 7
times higher than the sequential access code. This increase can be attributed directly to the
unexploited spatial locality. The cache line size on this system is 64 Bytes (as some of you
discovered in HW0). Each line can hold 16 integer values. A new cache line is brought in on an L1
miss. With sequential access, the subsequent 15 access are going to be hits and then it is going to
miss again. With random access all bets are off. It may or may not access any of the other
elements in the newly fetched cache line. The performance counter values suggest that the random
version is touching only two elements per cache line. Needless to say, this will vary form run to run. 


### Processing multi-dimensional arrays 

Consider the simple code for initializing a two-dimensional array. 

```C++
  int N = atoi(argv[1]);                            
                                                    
  int **a = (int **) malloc(sizeof(int *) * N);           
                                                    
  int i,j;                                          
  for (i = 0; i < N; i++)                           
    a[i] = (int *) malloc(sizeof(int) * N);         
                                                    
  for (i = 0; i < N; i++)                           
    for (j = 0; j < N; j++)                         
      a[i][j] = 17;                                 
```


**How long will it take to execute this code on this system?**

Let's find out. 

```
(knuth)% g++ -o multi_dim_array multi_dim_array.cpp 
(knuth)% time ./multi_dim_array 25000
```

Now let's look at a very similar code that accomplishes the same task. 

```C++
  int N = atoi(argv[1]);                            
                                                    
  int **a = (int **) malloc(sizeof(int *) * N);     
                                                    
  int i,j;                                          
  for (i = 0; i < N; i++)                           
    a[i] = (int *) malloc(sizeof(int) * N);         
                                                    
  for (j = 0; j < N; j++)                           
    for (i = 0; i < N; i++)                         
      a[i][j] = 17;                                 
                                                    
 ```                                                   

**How long will it take to execute this code on this system?**

Let's find out

```
(knuth)% g++ -o multi_dim_array_alt multi_dim_array_alt.cpp 
(knuth)% time ./multi_dim_array_alt 25000
```

**What happened?**

Maybe something to do with cache utilization. Let's check the cache numbers. 

```
(knuth)% get_store_miss_rates.sh ./multi_dim_array 25000
L1 store miss rate (miss/access): 	0.03
LLC store miss rate (miss/access): 	0.91
(knuth)% get_store_miss_rates.sh ./multi_dim_array_alt 25000
L1 store miss rate (miss/access): 	0.39
LLC store miss rate (miss/access): 	0.12
```

There is a substantial increase in the L1 miss rate. But the LLC miss rate is actually going down. Since
LLC misses are more costly, this is likely to have a bigger impact on performance. Why is the
alternate implementation performing so poorly even with a lower LLC miss rate?

**Can we explain this discrepancy?**

Let's look at the actual counts rather than miss rates. 

```
(knuth)% perf stat -e LLC-stores,LLC-store-misses ./multi_dim_array 25000
17

Performance counter stats for './multi_dim_array 25000':

        47,332,065      LLC-stores                                                  
        43,342,742      LLC-store-misses                                            

       3.600265671 seconds time elapsed

(knuth)% perf stat -e LLC-stores,LLC-store-misses ./multi_dim_array_alt 25000
17

 Performance counter stats for './multi_dim_array_alt 25000':

       673,143,822      LLC-stores                                                  
        80,758,509      LLC-store-misses                                            

      17.493527690 seconds time elapsed
```

`multi_dim_array_alt` is performing many more stores to LLC. As a result, although it is incurring
twice as many store misses, the miss rate numbers are low. 


**Why is `multi_dim_array_alt` performing a higher number of stores?**

This is explained by the higher miss rate in L1. An L1 miss translates into an access to a lower
level cache. Looking at just the cache miss rate numbers can sometimes be misleading. For codes that
have issue with cache utilization, we should look at a number of metrics and try to understand the
full picture. 



### Loop Interchange

C/C++ plus is a row-major language. This means that the row elements are contiguous in memory. This
means that there exists spatial locality from one row element to the next. To exploit spatial
locality in row-major languages, we want to ensure that consecutive elements of a row are accessed
close together in time. For doubly nested loops, this means making the column-index the inner
loop. In general, for any nested loop going through a multi-dimensional array we want to make sure
the innermost loop strides through the contiguous dimension. 

The programmers may not always be aware that this is how code should be written. For this reason,
compilers will transform the loop nest to ensure this is the case. This optimization is known as
loop interchange (or loop permutation). 

**Why did the compiler not perform loop interchange in our example code?**

It is possible that the `gcc` does not have this optimization in its collection. Let's check to see
if it does. 

```
(knuth)% g++ -Q -O3 --help=optimizers | more
```

Although it is not listed, we can check the `gcc` man page to see that `gcc` does indeed perform
loop interchange when `-floop-nest-optimize` is set. 

```
(knuth)% man g++
```

Search for `loop-nest-optimize`

```
       -ftree-loop-linear
       -floop-interchange
       -floop-strip-mine
       -floop-block
       -floop-unroll-and-jam
           Perform loop nest optimizations.  Same as -floop-nest-optimize.  To use
           this code transformation, GCC has to be configured with --with-isl to
           enable the Graphite loop transformation infrastructure.
```

Let's try compiling with `-floop-nest-optimize` enabled. 

```
(knuth)% g++ -o multi_dim_array_alt -O3 -floop-nest-optimize multi_dim_array_alt.cpp
(knuth)% get_store_miss_rates.sh ./multi_dim_array_alt 25000
```
 
Still no dice! 

It is difficult for the compiler to determine if loop interchange is safe. It needs to know that
dependencies are not being violated. In order to establish that it needs to know if there is any
aliasing going on. 


