# Vectorization with OpenMP


## Description 

This demo introduces the `simd` directive in OpenMP with the following objectives 

 - understand the use of the OpenMP `simd` directive
 - understand how `simd` directives our executed by the compiler 
 - understand when it is beneficial to use `simd` over `parallel for`
 - understand the use of the `reduction` clause 

## Outline
* [ `parallel for` And Task Granularity](#task_granularity)
* [The `simd` Construct](#simd)
* [The `reduction` Clause](#reduction)

## <a name="task_granularity"></a>`parallel for` And Task Granularity 

Consider the following code that adds two vectors and stores the result in a third vector. The
computation is repeated `REPS` times. For now, we have `REPS` set to 1000. 

```C
for (j = 0; j < REPS; j++) {
  for (i = 0; i < M; i++)
    c[i] =  a[i] + b[i];
}
```

We can parallelize the inner loop that performs the vector addition using the `parallel for`
directive. 

```C
for (j = 0; j < REPS; j++) {
#pragma omp parallel for
  for (i = 0; i < M; i++)
    c[i] =  a[i] + b[i];
}
```

Let's see if parallelizing the vector-add loop improves performance.

```
(shadowfax)% gcc -o vec_add vec_add.c -fopenmp -O2
(shadowfax)% ./vec_add 1024 1
result = 4235.220
parallel loop = 2.80 ms
(shadowfax)% ./vec_add 1024 2
result = 4235.220
parallel loop = 3.35 ms
(shadowfax)% ./vec_add 1024 4
result = 4235.220
parallel loop = 3.40 ms
(shadowfax)% ./vec_add 1024 8
result = 4235.220
parallel loop = 4.53 ms
```

_What's happening? Can we explain this behavior with something that we have covered in the previous
lectures?_

The amount of work done per thread is an important consideration when parallelizing code. The amount
of work per thread is also referred to as _task granularity_. The work done by each thread must be
sufficient to mitigate the overhead of thread creation and migration. In this particular example, it is not. 


## <a name="simd"></a> The `simd` construct

Fortunately, OpenMP provides another construct for fine-grain data parallelization. Recall the `simd aligned`
directive from the [Meng _et al._
paper](https://link.springer.com/chapter/10.1007/978-3-319-45550-1_2). The `simd` construct can be
applied to a loop to indicate that the loop should be vectorized. Vectorization refers to
Single-Instruction-Multiple-Data or SIMD-style parallelization. All most all processors today are
equipped with one or more vector units dedicated to performing SIMD operations. Vectorized loops are
off-loaded to these vector units. No separate threads are created. The `simd` directive has the same format as
the `parallel` directive and can be placed before any `for` loop in the program. 

```C
for (j = 0; j < REPS; j++) {
#pragma omp simd
  for (i = 0; i < M; i++)
    c[i] =  a[i] + b[i];
}
```

When OpenMP sees a `simd` directive, it tells the compiler to generate vectorized code for the
loop. The compiler can also vectorize loops on its own. But the compiler is generally conservative
when it comes to vectorization and will only vectorize a loop if it is certain that it is safe
to do so. 

Let's compile the code and see if vectorization gives us any benefits over generic parallelization. 

```
(shadowfax)% gcc -o vec_add vec_add.c -fopenmp
(shadowfax)% ./vec_add 1024 1
result = 4235.220
parallel loop = 7.83 ms
```

_What happened? Why did vectorization make the performance worse?_

Remember, OpenMP is instructing the compiler to vectorize the loop. We need to find out if loop was
indeed vectorized. The `fopt-info-all` in `gcc` prints a report about all the optimizations that
were applied during compilation. Let's try it out.

```
(shadowfax)% gcc -o vec_add vec_add.c -fopenmp -fopt-info-all
```

_Nothing! What's going on? Is the compiler not applying any optimization?_

_What is the default optimization level for `gcc`?_

Notice, that we compiled at the default optimization level which is _-O0_. For `gcc` this means that
it is not applying any optimizations. Let's try compiling with _-O2_. 

```
(shadowfax)% gcc -o vec_add vec_add.c -fopenmp -O2 -fopt-info-all
...
...
vec_add.c:57:11: note:   def_stmt =  _21 = _17 + _19;
vec_add.c:57:11: note: create vector_type-pointer variable to type: vector(2) double  vectorizing a pointer ref: *c_45
vec_add.c:57:11: note: created c_45
vec_add.c:57:11: note: add new stmt: MEM[(double *)vectp_c.27_118] = vect__21.26_117;
vec_add.c:57:11: note: ------>vectorizing statement: i_51 = i_87 + 1;
vec_add.c:57:11: note: ------>vectorizing statement: vectp_a.20_112 = vectp_a.20_111 + 16;
vec_add.c:57:11: note: ------>vectorizing statement: vectp_b.23_115 = vectp_b.23_114 + 16;
vec_add.c:57:11: note: ------>vectorizing statement: vectp_c.27_119 = vectp_c.27_118 + 16;
vec_add.c:57:11: note: ------>vectorizing statement: if (i_51 < _59)

loop at vec_add.c:57: if (ivtmp_122 < bnd.17_107)
vec_add.c:57:11: note: LOOP VECTORIZED

vec_add.c:26:5: note: vectorized 1 loops in function.
vec_add.c:26:5: note: loop turned into non-loop; it never loops
```

Now, we see that the loop is being vectorized. But even at the _-O2_ level, the compiler would
not have vectorized this particular loop if OpenMP hadn't explicitly asked it to do so. We can check missed
vectorization opportunities in `gcc` using the `-fopt-info-vec-missed` flag. 

```
(shadowfax)% gcc -o vec_add vec_add.c -fopenmp -O2 -fopt-info-vec-missed
vec_add.c:56:11: note: Unknown misalignment, naturally aligned
vec_add.c:56:11: note: Unknown misalignment, naturally aligned
vec_add.c:56:11: note: Unknown misalignment, naturally aligned
vec_add.c:56:11: note: not ssa-name.
vec_add.c:56:11: note: use not simple.
vec_add.c:56:11: note: not ssa-name.
vec_add.c:56:11: note: use not simple.
vec_add.c:56:11: note: not ssa-name.
vec_add.c:56:11: note: use not simple.
vec_add.c:56:11: note: not ssa-name.
vec_add.c:56:11: note: use not simple.
```

The compiler opts not to vectorize the loop because it does not know if the references are _aligned_
and because it cannot determine the number of iterations in the loop which depends on the runtime
value of `M`. 

Now, let's re-try the experiment and see if vectorization buys us anything over the regular
data-parallel version of the code 

```
(shadowfax)% gcc -o vec_add vec_add.c -fopenmp -O2
(shadowfax)% ./vec_add 1024 1
result = 4235.220
parallel loop = 0.88 ms
```

Lo and Behold! We have almost a factor of four improvement over the `parallel for` version. 

_What kind of performance do we expect, if we double the number threads?_

```
(shadowfax)% ./vec_add 1024 2
result = 4235.220
parallel loop = 0.88 ms
(shadowfax)% ./vec_add 1024 4
result = 4235.220
parallel loop = 0.88 ms
```

_What's happening?_

For vectorized loops no new threads are created. The entire vector computation is off-loaded to the
vector unit. So, vector performance has nothing to do with the number of threads used. 

### <a name="reduction"></a> The `reduction` Clause 

Let's look at another example which is also a potential candidate for vectorization. This code
performs a sum reduction of the two vectors and stores the final result in a scalar. 

```
for (j = 0; j < REPS; j++) {
  for (i = 0; i < M; i++)
    sum +=  a[i] + b[i];
}
```

Let's compile the code and measure performance of the sequential version. 

```
(shadowfax)% gcc -o sum_reduce sum_reduce.c -O2 -fopenmp
(shadowfax)% ./sum_reduce 1024 1
result = 2.168e+09
parallel loop = 2.61 ms
```

Let's insert the `simd` directive to parallelize the loop. 

```
for (j = 0; j < REPS; j++) {
#pragma omp simd
  for (i = 0; i < M; i++)
    sum +=  a[i] + b[i];
}
```

Now, time the SIMD version of the code. 

```
(shadowfax)% gcc -o sum_reduce sum_reduce.c -O2 -fopenmp
(shadowfax)% ./sum_reduce 1024 1
result = 2.168e+09
parallel loop = 2.57 ms
```

_What happened?_

Let's first check if the loop was vectorized. 

```
(shadowfax)% gcc -o sum_reduce sum_reduce.c -O2 -fopenmp -fopt-info-all
sum_reduce.c:56:11: note: init: stmt relevant? if (i_47 < _55)
sum_reduce.c:56:11: note: worklist: examine stmt: sum_46 = sum_9 + _22;
sum_reduce.c:56:11: note: vect_is_simple_use: operand sum_9
sum_reduce.c:56:11: note: def_stmt: sum_9 = PHI <sum_46(11), sum_89(9)>
sum_reduce.c:56:11: note: type of def: unknown
sum_reduce.c:56:11: note: Unsupported pattern.
sum_reduce.c:56:11: note: not vectorized: unsupported use in stmt.
sum_reduce.c:56:11: note: unexpected pattern.
sum_reduce.c:25:5: note: vectorized 0 loops in function.
```

Even after we specified the `simd` directive and used the _-O2_ option the loop was not vectorized. 

_Why do you think that is?_

It is actually illegal to run this loop in parallel. There is a loop-carried _dependence_ on the
`sum` variable (more on [dependence](https://en.wikipedia.org/wiki/Data_dependency) later in the
semester). The value of `sum` that is read in iteration `i` is produced in iteration `i-1`. 

It is entirely true that loop cannot be parallelized. It is just that it cannot be parallelized in a
typical SIMD fashion.  Because reductions appear so frequently in programs (think Amdahl!), OpenMP
provides a special clause specifically for these patterns. The clause can be combined with the
`simd` construct and used as follows  

```
for (j = 0; j < REPS; j++) {
#pragma omp simd reduction(+:sum)
  for (i = 0; i < M; i++)
    sum +=  a[i] + b[i];
}
```

The colon separated parameter specifies what kind of operation is being performed and the variable
that is involved in the dependence. Let's recompile with the `reduction` clause inserted. 
performance. 

First make sure loop is being vectorized. 

```
gcc -o sum_reduce sum_reduce.c -O2 -fopenmp -fopt-info-all
loop at sum_reduce.c:56: if (ivtmp_137 < bnd.18_122)
sum_reduce.c:56:11: note: LOOP VECTORIZED

sum_reduce.c:25:5: note: vectorized 1 loops in function.
sum_reduce.c:25:5: note: loop turned into non-loop; it never loops.
sum_reduce.c:25:5: note: loop with 2 iterations completely unrolled
sum_reduce.c:25:5: note: loop turned into non-loop; it never loops
sum_reduce.c:25:5: note: loop turned into non-loop; it never loops.
sum_reduce.c:25:5: note: loop with 2 iterations completely unrolled
```

It is. Now let's measure the performance. 

```
(shadowfax)% gcc -o sum_reduce sum_reduce.c -O2 -fopenmp
(shadowfax)% ./sum_reduce 1024 1
result = 2.168e+09
parallel loop = 1.31 ms
(shadowfax)% ./sum_reduce 1024 2
result = 2.168e+09
parallel loop = 1.31 ms
```

Notice, the performance improvement is not particularly great. This is because the loop is not fully
parallelized. There is some synchronization necessary between iterations. 


