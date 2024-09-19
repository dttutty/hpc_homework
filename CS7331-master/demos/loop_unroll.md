## Loop unrolling

### Description 

This demo introduces the loop unrolling compiler optimization. 


### Outline 

   * [Manually Unrolling a Loop](#manual)
   * [Automatic Loop Unrolling in LLVM](#auto)
   * [Loop Unroll `pragma`](#pragma)
   * [Selecting the Best Unroll Factor](#best_uf)

### <a name="manual"></a>Manually Unrolling a Loop

Consider the code for calculating the vector dot-product. 

```C
double dot_prod(double *x, double *y, int n) {
  double res = 0.0;
  for (unsigned i = 0; i < n; i++) 
     res += x[i] * y[i]; 
  return res;
}
```

We will examine the effect of loop unrolling on this loop. 

**Is it wothwhile to unroll this loop?**

Unrolling is a relatively safe transformation in the sense that even if it doesn't give us
improvement it rarely causes performance degradation.  This particular loop however is amenable
to `simd` parallelization. If we apply unrolling it may damage or destroy the opportunity for
vectorization. In some cases, excessive unrolling can also cause problems with instruction cache. 

To isolate effect of loop unrolling, we will compile the codes in this tutorial with vectorization
disabled. To get a _baseline_ performance, we first compile the code without loop unrolling. 

```
clang -O1 -mllvm -vectorize-loops=0 -o matvec matvec.c
```

`-mllvm -vectorize-loops=0` not to vectorize loops. At `-O1` optimization level loop unrolling is
not applied. 

```
./matvec 10000 10
```

Let's use `perf` to get some basic stats. 

```
(knuth)% perf stat ./matvec 10000 10
Result = 2.6386e+09
dot prod loop = 2313.89 ms

 Performance counter stats for './matvec 10000 10':

       4535.311963      task-clock (msec)         #    0.999 CPUs utilized          
                12      context-switches          #    0.003 K/sec                  
                 0      cpu-migrations            #    0.000 K/sec                  
           195,462      page-faults               #    0.043 M/sec                  
     9,655,445,844      cycles                    #    2.129 GHz                    
     4,586,289,371      stalled-cycles-frontend   #   47.50% frontend cycles idle   
     2,407,886,753      stalled-cycles-backend    #   24.94% backend cycles idle    
    13,101,676,894      instructions              #    1.36  insn per cycle         
                                                  #    0.35  stalled cycles per insn
     2,899,319,045      branches                  #  639.277 M/sec                  
         3,861,015      branch-misses             #    0.13% of all branches        

       4.538107656 seconds time elapsed
```

Note the number of branches executed. 

Now let's manually unroll the loop by a factor of 2. 
```
double dot_prod(double *x, double *y, int n) { 
  double res = 0.0;
  for (unsigned i = 0; i < n; i = i + 2) { 
    res += x[i] * y[i]; 
    res += x[i + 1] * y[i + 1]; 
  }
  return res;
}
```

Let's compile this code with same options as before and check the performance. 

```
(knuth)% clang -O1 -mllvm -vectorize-loops=0 -o matvec matvec.c
(knuth)% perf stat ./matvec 10000 10
Result = 2.6386e+09
dot prod loop = 2246.71 ms

 Performance counter stats for './matvec 10000 10':

       4431.502330      task-clock (msec)         #    1.000 CPUs utilized          
                 5      context-switches          #    0.001 K/sec                  
                 0      cpu-migrations            #    0.000 K/sec                  
           195,461      page-faults               #    0.044 M/sec                  
     9,628,562,313      cycles                    #    2.173 GHz                    
     4,566,208,245      stalled-cycles-frontend   #   47.42% frontend cycles idle   
     2,366,683,419      stalled-cycles-backend    #   24.58% backend cycles idle    
    12,594,698,933      instructions              #    1.31  insn per cycle         
                                                  #    0.36  stalled cycles per insn
     2,397,055,297      branches                  #  540.913 M/sec                  
         3,878,530      branch-misses             #    0.16% of all branches        

       4.432175099 seconds time elapsed
```

Slight improvement in performance. Mainly coming from the reduce number of branch instructions. 

**Would the performance be better if we unrolled more?**

Let's try it out. 

```
(knuth)% clang -O1 -Rpass=unroll -mllvm -vectorize-loops=0 -o matvec matvec.c
(knuth)% perf stat ./matvec 10000 10
Result = 2.6386e+09
dot prod loop = 2127.71 ms

 Performance counter stats for './matvec 10000 10':

       4347.378031      task-clock (msec)         #    1.000 CPUs utilized          
                 5      context-switches          #    0.001 K/sec                  
                 0      cpu-migrations            #    0.000 K/sec                  
           195,463      page-faults               #    0.045 M/sec                  
     9,203,572,677      cycles                    #    2.117 GHz                    
     4,594,047,457      stalled-cycles-frontend   #   49.92% frontend cycles idle   
     2,035,236,461      stalled-cycles-backend    #   22.11% backend cycles idle    
    11,844,628,355      instructions              #    1.29  insn per cycle         
                                                  #    0.39  stalled cycles per insn
     2,147,047,022      branches                  #  493.872 M/sec                  
         7,610,398      branch-misses             #    0.35% of all branches        

       4.348130567 seconds time elapsed

```

Again, slight improvement from the reduced number of branches. 



### <a name="auto"></a>Automatic Loop unrolling in LLVM

Manually unrolling loops is tedious and error-prone. LLVM will automatically try to unroll a
loop. But it will only do this at optimization _-O2_ and  higher. Let's check to see if LLVM will
unroll this loop. 

```
(knuth)% clang -O2 -Rpass=unroll -mllvm -vectorize-loops=0 -o matvec matvec.c
matvec.c:19:4: remark: unrolled loop by a factor of 4 with run-time trip count [-Rpass=loop-unroll]
   for (unsigned i = 0; i < n; i++) 
   ^
matvec.c:19:4: remark: unrolled loop by a factor of 4 with run-time trip count [-Rpass=loop-unroll]
matvec.c:19:4: remark: unrolled loop by a factor of 4 with run-time trip count [-Rpass=loop-unroll]
```

32 appears to work better on this platform. 

`Rpass` option gives optimization diagnostics.  LLVM chooses to unroll the loop by a factor
of 4. Note, the loop in question is inspected for unrolling by multiple passes but is transformed
only once.

Let's check to see if it gives us any performance benefits. 

```
perf stat ./matvec 10000 10
Result = 2.6386e+09
dot prod loop = 1891.31 ms

 Performance counter stats for './matvec 10000 10':

       4079.253403      task-clock (msec)         #    1.000 CPUs utilized          
                 3      context-switches          #    0.001 K/sec                  
                 0      cpu-migrations            #    0.000 K/sec                  
           195,462      page-faults               #    0.048 M/sec                  
     9,114,419,859      cycles                    #    2.234 GHz                    
     4,756,064,040      stalled-cycles-frontend   #   52.18% frontend cycles idle   
     2,659,204,024      stalled-cycles-backend    #   29.18% backend cycles idle    
    10,848,819,329      instructions              #    1.19  insn per cycle         
                                                  #    0.44  stalled cycles per insn
     2,148,483,901      branches                  #  526.686 M/sec                  
         7,698,090      branch-misses             #    0.36% of all branches        

       4.079849115 seconds time elapsed

```

Appears to be doing quite a bit better than our hand transformed version. 

**Why**?

The performance comparison is not correct, we really should be comparing with the `-O2` version. 

**How do we do that?**

### <a name="pragma"></a>Loop Unroll pragma

LLVM provides a loop unrolling `pragma`. We can insert it in front of any for loop (just like OpenMP
`parallel for`). The `pragma` allows us to enable or disable unrolling for a particular loop in the
program (cannot do this via command-line flags). Let's disable unrolling so that we can build the
code at `-O2` without unrolling. 

```
#pragma clang loop unroll(disable)
for (i = 0; i < n; i++) {
  res += x[i] * y[i]; 
}
```

```
(knuth)% clang -O2 -Rpass=unroll -mllvm -vectorize-loops=0 -o matvec matvec.c
(knuth)% perf stat ./matvec 10000 10
Result = 2.6386e+09
dot prod loop = 2336.78 ms

 Performance counter stats for './matvec 10000 10':

       4450.291687      task-clock (msec)         #    1.000 CPUs utilized          
                 6      context-switches          #    0.001 K/sec                  
                 0      cpu-migrations            #    0.000 K/sec                  
           195,461      page-faults               #    0.044 M/sec                  
     9,514,280,401      cycles                    #    2.138 GHz                    
     4,446,370,993      stalled-cycles-frontend   #   46.73% frontend cycles idle   
     2,280,432,658      stalled-cycles-backend    #   23.97% backend cycles idle    
    13,094,428,143      instructions              #    1.38  insn per cycle         
                                                  #    0.34  stalled cycles per insn
     2,896,962,479      branches                  #  650.960 M/sec                  
         3,864,426      branch-misses             #    0.13% of all branches        

       4.451048190 seconds time elapsed

```

Notice, no loops were unrolled. Performance is a little worse without unrolling. 

### <a name="best_uf"></a>Selecting The Best Unroll Factor

**Is 4 the best unroll factor for this loop?**

The loop unroll `pragma` can be used to specify an unroll factor. Let's try out a few different
ones. 

```
#pragma clang loop unroll_count(8) 
  for (i = 0; i < n; i++) 
	  res += x[i] * y[i]; 
```
```
#pragma clang loop unroll_count(20) 
  for (i = 0; i < n; i++) 
	  res += x[i] * y[i]; 
```
```
#pragma clang loop unroll_count(40) 
  for (i = 0; i < n; i++) 
	  res += x[i] * y[i]; 
```

For this particular loop on this platform 40 seems to work best. 

**Will the same unroll factor work well on other platforms?**

No!

