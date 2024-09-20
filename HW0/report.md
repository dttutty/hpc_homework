

Experimental Environment
=
Platform: Github Workspace

- Host name
```bash
$  hostname
codespaces-4bf82d
```
- CPU manufacturer, model, and clock rate.
```bash
$ lscpu
Vendor ID:  AuthenticAMD
Model name: AMD EPYC 7763 64-Core Processor
CPU MHz:    3242.790
```
- Number of physical cores and logical cores
```bash
$ cat /proc/cpuinfo | grep "cpu cores" | uniq
cpu cores       : 1
$ cat /proc/cpuinfo | grep "processor" | wc -l
2
```
- Cache configuration: number of cache levels, capacity and line size in each level
```bash
$ lscpu
L1d cache:                          32 KiB
L1i cache:                          32 KiB
L2 cache:                           512 KiB
L3 cache:                           32 MiB
$ getconf LEVEL1_ICACHE_LINESIZE
64
$ getconf LEVEL1_DCACHE_LINESIZE
64
$ getconf LEVEL2_CACHE_LINESIZE
64
$ getconf LEVEL3_CACHE_LINESIZE
64
```
- OS and kernel version  

| Name | Value |
|--|--|
| Kernel | 6.5.0-1025-azure |  
| OS | Ubuntu 20.04.6 LTS |
```bash
$ uname -a
Linux codespaces-4bf82d 6.5.0-1025-azure #26~22.04.1-Ubuntu SMP Thu Jul 11 22:33:04 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
$ cat /etc/os-release
NAME="Ubuntu"
VERSION="20.04.6 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.6 LTS"
```
- GCC version
```bash
$ gcc --version
gcc (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0
```

Measurement: Precision and Accuracy
=
Server: Brooks
- Execution time measured by bash builtin command: `time`

| unit: `second`| N=100, n=1 | N=100, n=10000 | N=1000, n=1000 | N=10000, n=1 |
|--|--|--|--|--|
| Real time| $\bar{t}$=0.0016, $\sigma$=0.0018 |$\bar{t}$=0.3382, $\sigma$=0.0049|$\bar{x}$=3.2731, $\sigma$=0.0052|$\bar{x}$=1.1386, $\sigma$=0.0074|
| User time| $\bar{t}$=0.0009, $\sigma$=0.003 |$\bar{t}$=0.3372, $\sigma$=0.0058|$\bar{x}$= 3.2681, $\sigma$=0.0059|$\bar{x}$= 1.0068, $\sigma$=0.0139|
|Sys time| $\bar{t}$=0.0001, $\sigma$=0.003 |$\bar{t}$=0.0008, $\sigma$=0.0016|$\bar{x}$= 0.0044, $\sigma$=0.0028|$\bar{x}$= 0.1316, $\sigma$=0.0156|

- Execution time measured by C function: `getitmeofday()`

| unit: `microsecond` | N=100, n=1 | N=100, n=10000 | N=1000, n=1000 | N=10000, n=1 |
|--|--|--|--|--|
|`Matrix_vector_mult()` time|$\bar{x}$=0.0606, $\sigma$=0.0165|$\bar{x}$=392.7668, $\sigma$=5.0062|$\bar{x}$=3895.9326, $\sigma$=16.7791|$\bar{x}$=326.9620, $\sigma$=2.4587|
|`main()` execution time|$\bar{x}$=0.2639, $\sigma$=0.0587|$\bar{x}$=392.9192, $\sigma$=5.0025|$\bar{x}$=3908.1603, $\sigma$=16.9118|$\bar{x}$=1121.0341, $\sigma$=3.5908|

- Execution time measured by `perf`

- the C `getitmeofday()` function
```bash
$ ./a.out 100 1
matrix_vector_mult execution time: 0.078917 ms
total execution time: 0.364065 ms
Result = 2.31e+07
```
```
$ ./a.out 100 10000
matrix_vector_mult execution time: 335.279942 ms
total execution time: 335.572958 ms
Result = 2.31e+07
```
```
$ ./a.out 1000 100
matrix_vector_mult execution time: 3251.953840 ms
total execution time: 3268.044949 ms
Result = 2.59e+08
```
```
$ ./a.out 10000 1
matrix_vector_mult execution time: 325.662851 ms
total execution time: 1110.962868 ms
Result = 2.64e+09
```
- perf
```bash
$ perf stat ./a.out 100 1
Result = 2.31e+07

 Performance counter stats for './a.out 100 1':

              0.93 msec task-clock                #    0.679 CPUs utilized          
                 0      context-switches          #    0.000 K/sec                  
                 0      cpu-migrations            #    0.000 K/sec                  
                75      page-faults               #    0.081 M/sec                  
         1,266,082      cycles                    #    1.365 GHz                    
            15,571      stalled-cycles-frontend   #    1.23% frontend cycles idle   
            51,538      stalled-cycles-backend    #    4.07% backend cycles idle    
         1,848,184      instructions              #    1.46  insn per cycle         
                                                  #    0.03  stalled cycles per insn
           347,600      branches                  #  374.807 M/sec                  
     <not counted>      branch-misses                                                 (0.00%)

       0.001365841 seconds time elapsed

       0.001456000 seconds user
       0.000000000 seconds sys
```
```
$ perf stat ./a.out 100 10000
Result = 2.31e+07

 Performance counter stats for './a.out 100 10000':

            340.76 msec task-clock                #    0.998 CPUs utilized          
                33      context-switches          #    0.097 K/sec                  
                 0      cpu-migrations            #    0.000 K/sec                  
                75      page-faults               #    0.220 K/sec                  
     1,214,473,475      cycles                    #    3.564 GHz                      (82.86%)
         2,030,398      stalled-cycles-frontend   #    0.17% frontend cycles idle     (83.57%)
           424,241      stalled-cycles-backend    #    0.03% backend cycles idle      (83.57%)
     2,036,482,450      instructions              #    1.68  insn per cycle         
                                                  #    0.00  stalled cycles per insn  (83.57%)
       105,000,218      branches                  #  308.138 M/sec                    (83.58%)
         1,006,605      branch-misses             #    0.96% of all branches          (82.85%)

       0.341327152 seconds time elapsed

       0.341253000 seconds user
       0.000000000 seconds sys
```
```
$ perf stat ./a.out 1000 1000
Result = 2.59e+08

 Performance counter stats for './a.out 1000 1000':

          3,281.22 msec task-clock                #    0.999 CPUs utilized          
               330      context-switches          #    0.101 K/sec                  
                 0      cpu-migrations            #    0.000 K/sec                  
             2,016      page-faults               #    0.614 K/sec                  
    12,050,317,206      cycles                    #    3.673 GHz                      (83.31%)
         2,986,448      stalled-cycles-frontend   #    0.02% frontend cycles idle     (83.30%)
         3,554,291      stalled-cycles-backend    #    0.03% backend cycles idle      (83.31%)
    20,119,959,119      instructions              #    1.67  insn per cycle         
                                                  #    0.00  stalled cycles per insn  (83.31%)
     1,027,132,402      branches                  #  313.034 M/sec                    (83.43%)
         1,058,446      branch-misses             #    0.10% of all branches          (83.35%)

       3.282913997 seconds time elapsed

       3.281294000 seconds user
       0.000000000 seconds sys
```
```
$ perf stat ./a.out 10000 1
Result = 2.64e+09

 Performance counter stats for './a.out 10000 1':

          1,139.25 msec task-clock                #    0.999 CPUs utilized          
               117      context-switches          #    0.103 K/sec                  
                 0      cpu-migrations            #    0.000 K/sec                  
           195,464      page-faults               #    0.172 M/sec                  
     4,149,634,566      cycles                    #    3.642 GHz                      (83.16%)
       104,987,713      stalled-cycles-frontend   #    2.53% frontend cycles idle     (83.15%)
        40,131,812      stalled-cycles-backend    #    0.97% backend cycles idle      (83.40%)
    10,886,577,655      instructions              #    2.62  insn per cycle         
                                                  #    0.01  stalled cycles per insn  (83.50%)
     1,903,150,462      branches                  # 1670.528 M/sec                    (83.50%)
         1,024,534      branch-misses             #    0.05% of all branches          (83.29%)

       1.140148459 seconds time elapsed

       1.015126000 seconds user
       0.123893000 seconds sys
```
