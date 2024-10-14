
# Problem Size
| class | Noof Attr | Noof Non-Zero | Noof Iter | Shift |
|-------|-----------|---------------|-----------|-------|
| S     | 1400      | 7             | 15        | 10.0  |
| W     | 7000      | 8             | 15        | 12.0  |
| A     | 14000     | 11            | 15        | 20.0  |
| B     | 75000     | 13            | 75        | 60.0  |
| C     | 150000    | 15            | 75        | 110.0 |


# Server Detail
`AMD EPYC 7V13` supports the following SIMD and vector-related instruction sets: `sse` `sse2` `ssse3`  `sse4_1` `sse4_2`   `sse4a` `misalignsse` `avx` `avx2`
| Specification     | Value                     |
|-------------------|---------------------------|
| Host              | brooks                    |
| Model name        | AMD EPYC 7V13 64-Core     |
| Core(s) per socket| 64                        |
| Socket(s)         | 2                         |
| Hyper-Threading?  | No                        |
| Thread(s)         | 128                       |



# Experiments Details
## Rolled Version

|conf | description|
|-------------------|---------------------------|
|`baseline`| without parallelization or SIMD (shown as a grey horizontal line on each figure)|
|`conf_rolled_1`:|As many `simd` parallelization directives as possible|
|`conf_rolled_2`|As many `parallel for simd` parallelization directives as possible|
|`conf_rolled_3`|As many `parallel for` parallelization directives as possible|

**Attention**: 
- in order to save time, I repeated `conf_rolled_1` with each conbination of `CLASS` and `thread numbers` 10 times to obtain the mean `Mop/s` and its standard deviation. For `conf_rolled_2` and `conf_rolled_3, I only repeated for 2 times.

- `#pragma omp` is ignored in following tables to save space

| `for` | `conf_rolled_1` | `conf_rolled_2`| `conf_rolled_3`|
|--|--|--|--|
| 1st     | `simd`                            | `parallel for simd`                    | `parallel for`                    |
| 2nd     | `simd reduction(+ : rho)`         | `parallel for simd reduction(+ : rho)` | `parallel for reduction(+ : rho)` |
| 3rd     | DISABLED                          | DISABLED                 		       | DISABLED                 		   |
| -4th    | `parallel for private(k, sum)`    | SAME as LEFT      		               | SAME as LEFT     		           |
| --5th   | DISABLED                          | SAME as LEFT                           | SAME as LEFT                      |
| -6th    | `simd`                            | `parallel for simd`                    | `parallel for`                    |
| -7th    | `simd`                            | `parallel for simd`                    | `parallel for`                    |
| -8th    | `simd reduction(+ : d)`           | `parallel for simd reduction(+ : d)`   | `parallel for reduction(+ : d)`   |
| -9th    | `simd`                            | `parallel for simd`                    | `parallel for`                    |
| -10th   | `simd reduction(+ : rho)`         | `parallel for simd reduction(+ : rho)` | `parallel for reduction(+ : rho)` |
| -11th   | `simd`                            | `parallel for simd`                    | `parallel for`                    |
| 12th    | `parallel for private(k, d)`      | SAME as LEFT      				       | SAME as LEFT      				   |
| -13th   | DISABLED                          | DISABLED                               | DISABLED                          | 
| 14th    | `simd`                            | `parallel for simd`                    | `parallel for`                    |
| 15th    | `simd reduction(+ : sum)`         | `parallel for simd reduction(+ : sum)` | `parallel for reduction(+ : sum)` |

### CLASS=S
![](NPB/result_pic/R/S.png)
### CLASS=W
![](NPB/result_pic/R/W.png)
### CLASS=A
![](NPB/result_pic/R/A.png)
### CLASS=B
![](NPB/result_pic/R/B.png)
### CLASS=C
![](NPB/result_pic/R/C.png)

## Unrolled by 2 Version

| `for` | `conf_unrolled_by2_1` |
|--|--|
| 1st     | `parallel for simd`                    |
| 2nd     | `parallel for simd reduction(+ : rho)` |
| 3rd     | DISABLED                 		       | 
| -4th    | `for private(j, k)`                    |
| --5th   | `simd reduction(+:sum1, sum2)`         |
| -6th    | `parallel for simd`                    |
| -7th    | `parallel for simd`                    |
| -8th    | `parallel for simd reduction(+ : d)`   |
| -9th    | `parallel for simd`                    |
| -10th   | `parallel for simd reduction(+ : rho)` |
| -11th   | `parallel for simd`                    |
| 12th    | `parallel for private(k, d)`      	   |
| -13th   | DISABLED                               |
| 14th    | `parallel for simd`                    |
| 15th    | `parallel for simd reduction(+ : sum)` |

### CLASS=S
![](NPB/result_pic/U1/S.png)
### CLASS=W
![](NPB/result_pic/U1/W.png)
### CLASS=A
![](NPB/result_pic/U1/A.png)
### CLASS=B
![](NPB/result_pic/U1/B.png)
### CLASS=C
![](NPB/result_pic/U1/C.png)


## Unrolled by 8 Version

| `for` | `conf_unrolled_by8_1` |
|--|--|
| 1st     | `simd`                            |
| 2nd     | `simd reduction(+ : rho)`         |
| 3rd     | DISABLED                          |
| -4th    | `parallel for private(j, k, sum)` |
| an additional one after the 4th | DISABLED            
| --5th   | DISABLED                          |
| -6th    | `simd`                            |
| -7th    | `simd`                            | 
| -8th    | `simd reduction(+ : d)`           |
| -9th    | `simd`                            |
| -10th   | `simd reduction(+ : rho)`         |
| -11th   | `simd`                            |
| 12th    | `parallel for private(k, d)`      |
| -13th   | DISABLED                          |
| 14th    | `simd`                            |
| 15th    | `simd reduction(+ : sum)`         |

# My Idea

1. Why are the following 2 nested loops not suitable for SIMD?  
```#pragma omp parallel for private(k, sum) // omp_flags_4_
    for (j = 1; j <= lastrow - firstrow + 1; j++)
    {
      sum = 0.0;
      for (k = rowstr[j]; k < rowstr[j + 1]; k++) 
      {
        sum = sum + a[k] * p[colidx[k]];
      }
      w[j] = sum;
    }
```
```
#pragma omp parallel for private(k, d) // omp_flags_12_
  for (j = 1; j <= lastrow - firstrow + 1; j++)
  {
    d = 0.0;
    for (k = rowstr[j]; k <= rowstr[j + 1] - 1; k++)
    {
      d = d + a[k] * z[colidx[k]];
    }
    w[j] = d;
  }
```  
Because `p[colidx[k]]` and `z[colidx[k]]` involves indirect memory access and the data is not contiguous, the above 2 nested loops are not suitable for SIMD.

2. Why is the 3rd for loop not suitable for parallelization?  
Because the following variables depend on results from previous iterations, if we add a parallel directive to the 3rd for loop, multiple threads will read from and write to these variables simultaneously, leading to incorrect results.
`rho0 = rho;`  
`alpha = rho0 / d;`  
`beta = rho / rho0;`  
`p[j] = r[j] + beta * p[j];`  
`z[j] = z[j] + alpha * p[j];`  
`r[j] = r[j] - alpha * q[j];`  
3. Is there potententional for improvement?  
When I set the threads to best threads number (on which the largest mop/s value can be achieved), I continuouly run the binary file

#  Analysis and Discussion

1. What is the maximum speedup your code is able to achieve on top of the baseline sequential version? Clearly indicate what you consider to be the baseline.
The baseline I have chosen is the config without parallelization or SIMD (shown as a grey horizontal line on each figure). The maximum speedup for each class is shown below. The speedup ratio is calculated as the maximum speed (Mop/s) divided by the baseline speed (Mop/s).

| class | max speedup | threads num | config |
|-------|---------------|---------------------------|----------------------|
| S     | 2.69x         | 36                        | conf_rolled_1: mostly simd |
| W     | 5.59x         | 48                        | conf_rolled_1: mostly simd |
| A     | 9.30x         | 40                        | conf_rolled_2: mostly parallel for simd |
| B     | 24.30x        | 80                        | conf_rolled_2: mostly parallel for simd |
| C     | 32.10x        | 124                       | conf_rolled_3: mostly parallel for |


2. Do the performance improvements meet your expectations? Why or why not?
The results align with my expectations in terms of parallel efficiency: larger problems benefit significantly from parallelism,  smaller ones suffer from parallel overhead.


3. What is the optimal number of threads for CG on your system? Why?
The optimal number of threads for each class is shown in the table above. From this, we can conclude that:  
- As the size of the problem increases, more threads are required to fully exploit the advantages of parallelism, leading to a higher speedup ratio.
- For smaller problems, the parallelization overhead is relatively significant compared to the computational workload, so the optimal number of threads is smaller.


For small size problem, the overhead of parallel is relatively big, so the best thread nums is smaller.


1. Evaluate how loop unrolling affects the performance of parallel codes. Unrolled versions of one of the loops
in conj-grad is given in comments in the source file. Run these versions, and possibly add your own, and
compare the parallel performance with the rolled version.
