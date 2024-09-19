## Compilers and the Compilation Process

### Description

Get exposure to different compilers and their capabilities

  * `--version` flag
  * `-v` or `--verbose` flag
  * `-c` and `-S` flags 
  

### Outline 
  * [Compiler Choices](#choices)
  * [Compilation Steps](#steps)
  * [Performance](#performance)
  * [Optimizations](#optimizations)
  
### <a name="choices"></a>Compiler Choices

The choice of a compiler can lead to huge performance differences in your code. 
Let's log into `knuth` and check out the installed compilers. `gcc` comes pre-installed on most
Linux distributions. However, the default installation may not be that recent. 
```
(knuth)% gcc --version
gcc (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0
Copyright (C) 2017 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

LLVM is another compiler that has become mainstream in recent years. The LLVM compiler
infrastructure is not a compiler but rather a set of compilers and toolchains. The C/C++ compiler in
LLVM is known as `clang`.

```
(knuth)% clang --version
clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final)
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /usr/bin
```

On some systems `clang` may be pre-installed. However, it is likely to be really old. LLVM is
known for it's streamlined design and is heavily used for compiler research and for developing new
compilers, tools and optimizations. There are even LLVM front-ends for interpreted languages like
Python. 

Major vendors also release their own compilers. 

```
(knuth)% icc --version
icc (ICC) 14.0.3 20140422
Copyright (C) 1985-2014 Intel Corporation.  All rights reserved.
```

It used to be the case that vendor compilers could produce much better quality code than their
open-source counterparts. But that difference seems to be narrowing, at least for less-complex
applications. Vendor compilers are not pre-installed and generally you have to pay to use them. But
most have educational discounts. The Intel compiler and associated tools is free to use for [students](https://software.intel.com/content/www/us/en/develop/tools/compilers/c-compilers.html) 

*What other compilers have you used in the past?*

There is one other compiler that is rarely used today. It is known as the _native_ compiler (note,
this is different from native vs cross-compilation). It is a compiler that comes with the
system. The C/C++ native compiler is known as `cc`. 

```
(knuth)% cc --version
cc (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0
Copyright (C) 2017 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

Today, the native compiler has pretty much been subsumed by `gcc` and `clang`. Often `cc` will just
link to one of these two compilers.  

```
(knuth)% ls -ltr `which cc`
lrwxrwxrwx 1 root root 20 Feb  5  2019 /usr/bin/cc -> /etc/alternatives/cc
(knuth)% 
```

`knuth` has its own native compiler (although in reality it's just an older version of `gcc`). 

On the Mac, the native compiler links to `clang`. 

```
(ritchie)% cc --version
Apple clang version 11.0.0 (clang-1100.0.33.17)
Target: x86_64-apple-darwin18.7.0
Thread model: posix
InstalledDir: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin 
```


### <a name="steps"></a>Compilation Steps 

For the rest of the demo we will use an implementation of the `knapsack` code parallelized with
OpenMP. Note, this code is poorly written. 

```C++
omp_set_num_threads(threads);
#pragma omp parallel for
  for (int t = 1; t <= threads; t++) {
    int m, result, jopt, mopt;
    int innerLB = x - ((t - 1) * BLOCK);

    for (int xx = innerLB; (xx < vessel_cap) && (xx < innerLB + BLOCK); xx++) {
      if(xx < weight[t + (K - 1)])
        itemsjo[t + (K - 1)][xx] = itemsjo[t + (K - 1) - 1][xx];
      else {
        int temp1 = itemsjo[t + (K - 1) - 1][xx];
	    int temp2 = itemsjo[t + (K - 1)][xx - weight[t + (K - 1)]] + value[t + (K - 1)];
        if (temp1 > temp2)
          itemsjo[t + (K - 1)][xx]= temp1;
        else
          itemsjo[t + (K - 1)][xx]= temp2;
	  }
    }
  }
```

Let's compile the code with `gcc`

```
(knuth)% g++ -o knapsack knapsack.cpp
/tmp/ccOzES92.o: In function `looprun(int**, int)':
knapsack.cpp:(.text+0x1f7): undefined reference to `omp_set_num_threads'
collect2: error: ld returned 1 exit status
```

_What did we do wrong?_

Need the `-fopenmp` flag. 

```
(knuth)% g++ -o knapsack knapsack.cpp -fopenmp
(knuth)% ls -ltr
total 248
-rw-rw-r-- 1 aq10 aq10   5235 Sep 21 22:12 knapsack.cpp
-rw-rw-r-- 1 aq10 aq10 225175 Sep 21 22:12 input
-rwxrwxr-x 1 aq10 aq10  19264 Sep 21 23:30 knapsack
```

Now let's compile the code again with `--verbose` or `-v`

```
(knuth)% g++ -v -o knapsack knapsack.cpp -fopenmp
Using built-in specs.
COLLECT_GCC=g++
COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-linux-gnu/7/lto-wrapper
OFFLOAD_TARGET_NAMES=nvptx-none
OFFLOAD_TARGET_DEFAULT=1
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Ubuntu 7.5.0-3ubuntu1~18.04' --with-bugurl=file:///usr/share/doc/gcc-7/README.Bugs --enable-languages=c,ada,c++,go,brig,d,fortran,objc,obj-c++ --prefix=/usr --with-gcc-major-version-only --program-suffix=-7 --program-prefix=x86_64-linux-gnu- --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --libdir=/usr/lib --enable-nls --enable-bootstrap --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --with-default-libstdcxx-abi=new --enable-gnu-unique-object --disable-vtable-verify --enable-libmpx --enable-plugin --enable-default-pie --with-system-zlib --with-target-system-zlib --enable-objc-gc=auto --enable-multiarch --disable-werror --with-arch-32=i686 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --enable-multilib --with-tune=generic --enable-offload-targets=nvptx-none --without-cuda-driver --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu
Thread model: posix
gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04) 
COLLECT_GCC_OPTIONS='-v' '-o' 'knapsack' '-fopenmp' '-shared-libgcc' '-mtune=generic' '-march=x86-64' '-pthread'
 /usr/lib/gcc/x86_64-linux-gnu/7/cc1plus -quiet -v -imultiarch x86_64-linux-gnu -D_GNU_SOURCE -D_REENTRANT knapsack.cpp -quiet -dumpbase knapsack.cpp -mtune=generic -march=x86-64 -auxbase knapsack -version -fopenmp -fstack-protector-strong -Wformat -Wformat-security -o /tmp/ccCtKqTT.s
GNU C++14 (Ubuntu 7.5.0-3ubuntu1~18.04) version 7.5.0 (x86_64-linux-gnu)
	compiled by GNU C version 7.5.0, GMP version 6.1.2, MPFR version 4.0.1, MPC version 1.1.0, isl version isl-0.19-GMP

GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
ignoring duplicate directory "/usr/include/x86_64-linux-gnu/c++/7"
ignoring nonexistent directory "/usr/local/include/x86_64-linux-gnu"
ignoring nonexistent directory "/usr/lib/gcc/x86_64-linux-gnu/7/../../../../x86_64-linux-gnu/include"
#include "..." search starts here:
#include <...> search starts here:
 /usr/include/c++/7
 /usr/include/x86_64-linux-gnu/c++/7
 /usr/include/c++/7/backward
 /usr/lib/gcc/x86_64-linux-gnu/7/include
 /usr/local/include
 /usr/lib/gcc/x86_64-linux-gnu/7/include-fixed
 /usr/include/x86_64-linux-gnu
 /usr/include
End of search list.
GNU C++14 (Ubuntu 7.5.0-3ubuntu1~18.04) version 7.5.0 (x86_64-linux-gnu)
	compiled by GNU C version 7.5.0, GMP version 6.1.2, MPFR version 4.0.1, MPC version 1.1.0, isl version isl-0.19-GMP

GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
Compiler executable checksum: 3eb3dc290cd5714c3e1c3ae751116f07
COLLECT_GCC_OPTIONS='-v' '-o' 'knapsack' '-fopenmp' '-shared-libgcc' '-mtune=generic' '-march=x86-64' '-pthread'
 as -v --64 -o /tmp/ccg8JExP.o /tmp/ccCtKqTT.s
GNU assembler version 2.30 (x86_64-linux-gnu) using BFD version (GNU Binutils for Ubuntu) 2.30
COMPILER_PATH=/usr/lib/gcc/x86_64-linux-gnu/7/:/usr/lib/gcc/x86_64-linux-gnu/7/:/usr/lib/gcc/x86_64-linux-gnu/:/usr/lib/gcc/x86_64-linux-gnu/7/:/usr/lib/gcc/x86_64-linux-gnu/
LIBRARY_PATH=/usr/lib/gcc/x86_64-linux-gnu/7/:/usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/:/usr/lib/gcc/x86_64-linux-gnu/7/../../../../lib/:/lib/x86_64-linux-gnu/:/lib/../lib/:/usr/lib/x86_64-linux-gnu/:/usr/lib/../lib/:/usr/lib/gcc/x86_64-linux-gnu/7/../../../:/lib/:/usr/lib/
Reading specs from /usr/lib/gcc/x86_64-linux-gnu/7/libgomp.spec
COLLECT_GCC_OPTIONS='-v' '-o' 'knapsack' '-fopenmp' '-shared-libgcc' '-mtune=generic' '-march=x86-64' '-pthread'
 /usr/lib/gcc/x86_64-linux-gnu/7/collect2 -plugin /usr/lib/gcc/x86_64-linux-gnu/7/liblto_plugin.so -plugin-opt=/usr/lib/gcc/x86_64-linux-gnu/7/lto-wrapper -plugin-opt=-fresolution=/tmp/ccxlwZdL.res -plugin-opt=-pass-through=-lgcc_s -plugin-opt=-pass-through=-lgcc -plugin-opt=-pass-through=-lpthread -plugin-opt=-pass-through=-lc -plugin-opt=-pass-through=-lgcc_s -plugin-opt=-pass-through=-lgcc --build-id --eh-frame-hdr -m elf_x86_64 --hash-style=gnu --as-needed -dynamic-linker /lib64/ld-linux-x86-64.so.2 -pie -z now -z relro -o knapsack /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/Scrt1.o /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/crti.o /usr/lib/gcc/x86_64-linux-gnu/7/crtbeginS.o /usr/lib/gcc/x86_64-linux-gnu/7/crtoffloadbegin.o -L/usr/lib/gcc/x86_64-linux-gnu/7 -L/usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu -L/usr/lib/gcc/x86_64-linux-gnu/7/../../../../lib -L/lib/x86_64-linux-gnu -L/lib/../lib -L/usr/lib/x86_64-linux-gnu -L/usr/lib/../lib -L/usr/lib/gcc/x86_64-linux-gnu/7/../../.. /tmp/ccg8JExP.o -lstdc++ -lm -lgomp -lgcc_s -lgcc -lpthread -lc -lgcc_s -lgcc /usr/lib/gcc/x86_64-linux-gnu/7/crtendS.o /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/crtn.o /usr/lib/gcc/x86_64-linux-gnu/7/crtoffloadend.o
COLLECT_GCC_OPTIONS='-v' '-o' 'knapsack' '-fopenmp' '-shared-libgcc' '-mtune=generic' '-march=x86-64' '-pthread'
```

There are several steps embedded within the overall _compilation_ process. When we run
`gcc` (or `clang` or whatever compiler), a series of commands are invoked behind the scenes to
convert the assembly generated by the compiler into an executable binary. Let's look at the
compilation steps for `icc`. 

```
(knuth)% icc -v -o knapsack knapsack.cpp -openmp
icc version 14.0.3 (gcc version 4.8.1 compatibility)
/opt/intel/composer_xe_2013_sp1.3.174/bin/intel64/mcpcom    -_g -mP3OPT_inline_alloca -D__HONOR_STD -D__ICC=1400 -D__INTEL_COMPILER=1400 -D__INTEL_COMPILER_UPDATE=3 -D__PTRDIFF_TYPE__=long "-D__SIZE_TYPE__=unsigned long" -D__WCHAR_TYPE__=int "-D__WINT_TYPE__=unsigned int" "-D__INTMAX_TYPE__=long int" "-D__UINTMAX_TYPE__=long unsigned int" -D__LONG_MAX__=9223372036854775807L -D__QMSPP_ -D__OPTIMIZE__ -D__NO_MATH_INLINES -D__NO_STRING_INLINES -D__GNUC_GNU_INLINE__ -D__GNUG__=4 -D__GNUC__=4 -D__GNUC_MINOR__=8 -D__GNUC_PATCHLEVEL__=1 -D__LP64__ -D_LP64 -D_GNU_SOURCE=1 -D__DEPRECATED=1 -D__GXX_WEAK__=1 -D__GXX_ABI_VERSION=1002 "-D__USER_LABEL_PREFIX__= " -D__REGISTER_PREFIX__= -D__INTEL_RTTI__ -D__EXCEPTIONS=1 -D__unix__ -D__unix -D__linux__ -D__linux -D__gnu_linux__ -B -Dunix -Dlinux "-_Asystem(unix)" -D__ELF__ -D__x86_64 -D__x86_64__ "-_Acpu(x86_64)" "-_Amachine(x86_64)" -D_MT -D__INTEL_COMPILER_BUILD_DATE=20140422 -D_OPENMP=201307 -D__INTEL_OFFLOAD -D__i686 -D__i686__ -D__pentiumpro -D__pentiumpro__ -D__pentium4 -D__pentium4__ -D__tune_pentium4__ -D__SSE2__ -D__SSE__ -D__MMX__ -_k -_8 -_l -_a -_b --gnu_version=481 -_W5 --gcc-extern-inline -p --bool -tused -x --openmp --openmp_tasks --openmp_simd --openmp_offload --multibyte_chars --array_section --simd --simd_func --offload_mode=1 --offload_target_names=mic,MIC --offload_unique_string=icc63316968zvLOxt --bool -mP1OPT_version=14.0-intel64 -mGLOB_diag_file=/tmp/icc1pnXCD.diag -mP1OPT_print_version=FALSE -mCG_use_gas_got_workaround=F -mP2OPT_align_option_used=TRUE -mGLOB_gcc_version=481 "-mGLOB_options_string=-v -o knapsack -openmp" -mGLOB_cxx_limited_range=FALSE -mCG_extend_parms=FALSE -mGLOB_compiler_bin_directory=/opt/intel/composer_xe_2013_sp1.3.174/bin/intel64 -mGLOB_as_output_backup_file_name=/tmp/iccTKXCSNas_.s -mIPOPT_activate -mIPOPT_lite -mGLOB_em64t -mGLOB_instruction_tuning=0x0 -mGLOB_product_id_code=0x22006d91 -mCG_bnl_movbe=T -mGLOB_extended_instructions=0x8 -mP3OPT_use_mspp_call_convention -mPGOPTI_value_profile_use=T -mPAROPT_openmp=TRUE -mP2OPT_il0_array_sections=TRUE -mGLOB_offload_mode=1 -mP2OPT_offload_unique_var_string=icc63316968zvLOxt -mP2OPT_hlo_level=2 -mP2OPT_hlo -mP2OPT_hpo_rtt_control=0 -mIPOPT_args_in_regs=0 -mP2OPT_disam_assume_nonstd_intent_in=FALSE -mGLOB_imf_mapping_library=/opt/intel/composer_xe_2013_sp1.3.174/bin/intel64/libiml_attr.so -mIPOPT_obj_output_file_name=/tmp/icc1pnXCD.o -mIPOPT_whole_archive_fixup_file_name=/tmp/iccwarch79LWsl -mGLOB_linker_version=2.30 -mGLOB_long_size_64 -mGLOB_routine_pointer_size_64 -mGLOB_driver_tempfile_name=/tmp/icctempfilek3q2Dq -mP3OPT_asm_target=P3OPT_ASM_TARGET_GAS -mGLOB_async_unwind_tables=TRUE -mGLOB_obj_output_file=/tmp/icc1pnXCD.o -mGLOB_source_dialect=GLOB_SOURCE_DIALECT_C_PLUS_PLUS -mP1OPT_source_file_name=knapsack.cpp -mGLOB_eh_linux knapsack.cpp
#include "..." search starts here:
#include <...> search starts here:
 /opt/intel/composer_xe_2013_sp1.3.174/compiler/include/intel64
 /opt/intel/composer_xe_2013_sp1.3.174/compiler/include
 /usr/include/c++/7
 /usr/include/c++/7/backward
 /usr/local/include
 /usr/lib/gcc/x86_64-linux-gnu/7/include
 /usr/lib/gcc/x86_64-linux-gnu/7/include-fixed
 /usr/include
 /usr/include/x86_64-linux-gnu
 /usr/include/x86_64-linux-gnu/c++/7
End of search list.
ld    /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/crt1.o /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/crti.o /usr/lib/gcc/x86_64-linux-gnu/7/crtbegin.o --eh-frame-hdr --build-id -dynamic-linker /lib64/ld-linux-x86-64.so.2 -o knapsack -L/opt/intel/composer_xe_2013_sp1.3.174/compiler/lib/intel64 -L/usr/lib/gcc/x86_64-linux-gnu/7/ -L/usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/ -L/usr/lib/gcc/x86_64-linux-gnu/7/../../../../lib/ -L/lib/x86_64-linux-gnu/ -L/lib/../lib64 -L/lib/../lib/ -L/usr/lib/x86_64-linux-gnu/ -L/usr/lib/../lib/ -L/usr/lib/gcc/x86_64-linux-gnu/7/../../../ -L/lib64 -L/lib/ -L/usr/lib /tmp/icc1pnXCD.o -Bdynamic -Bstatic -limf -lsvml -lirng -Bdynamic -lm -Bstatic -lipgo -ldecimal -Bdynamic -liomp5 --as-needed -lcilkrts --no-as-needed -lstdc++ -lgcc -lgcc_s -Bstatic -lirc -Bdynamic -lpthread -Bstatic -lsvml -Bdynamic -lc -lgcc -lgcc_s -Bstatic -lirc_s -Bdynamic -ldl -lc /usr/lib/gcc/x86_64-linux-gnu/7/crtend.o /usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/crtn.o
```

Notice the steps are different. Sometimes compilers may use proprietary assemblers, linkers and
loaders. In this instance, both `gcc` and `icc` are using the GNU linker. But `gcc` is using the
wrapper `collect2`.

If we want to just _compile_ the source then we can use the `-c` or compile option. 

```
(knuth)% g++ -c knapsack.cpp 
```

_Will this compile? Are we forgetting something?_

No! The `-fopenmp` flag is just for the linker. Function definitions are only searched at link time. 
 
```
(knuth)% ls -ltr
total 284
-rw-rw-r-- 1 aq10 aq10   5235 Sep 21 22:12 knapsack.cpp
-rw-rw-r-- 1 aq10 aq10 225175 Sep 21 22:12 input
-rwxrwxr-x 1 aq10 aq10  39976 Sep 21 23:37 knapsack
-rw-rw-r-- 1 aq10 aq10  12912 Sep 22 00:57 knapsack.o
```

To generate the actual assembly file, we can specify the `-S` option. 

```
(knuth)% g++ -o knapsack.s -S knapsack.cpp 
(knuth)% ls -ltr 
total 312
-rw-rw-r-- 1 aq10 aq10   5235 Sep 21 22:12 knapsack.cpp
-rw-rw-r-- 1 aq10 aq10 225175 Sep 21 22:12 input
-rwxrwxr-x 1 aq10 aq10  39976 Sep 21 23:37 knapsack
-rw-rw-r-- 1 aq10 aq10  12912 Sep 22 00:57 knapsack.o
-rw-rw-r-- 1 aq10 aq10  26436 Sep 22 01:01 knapsack.s
```

We can compare the LOC in the source and assembly files with `wc`. 

```
(knuth)% wc -l knapsack.cpp 
233 knapsack.cpp
(knuth)% wc -l knapsack.s 
1303 knapsack.s
```

The generated assembly file is considerably larger than the source. Roughly a single high-level
instruction is being translated to four assembly instructions. The `-S` is standard across most
compilers. 

Let's look at the assembly file generated by the Intel compiler. 
```
(knuth)% icc -o knapsack_icc.s -S knapsack.cpp 
knapsack.cpp(61): warning #3180: unrecognized OpenMP #pragma
        #pragma omp parallel for 
                ^
```

_What happened?_

Recall that the OpenMP directives are processed by the OpenMP pre-processor. The OpenMP pre-processor is
different for `gcc` and `icc`. It is integrated within the Intel compiler while in `gcc` it is a
separate pass. Let's re-compile with the `-openmp` flag. 

```
(knuth)% icc -o knapsack_icc.s -S knapsack.cpp -openmp
(knuth)% ls -ltr
total 504
-rw-rw-r-- 1 aq10 aq10   5235 Sep 21 22:12 knapsack.cpp
-rw-rw-r-- 1 aq10 aq10 225175 Sep 21 22:12 input
-rwxrwxr-x 1 aq10 aq10  39976 Sep 21 23:37 knapsack
-rw-rw-r-- 1 aq10 aq10  12912 Sep 22 00:57 knapsack.o
-rw-rw-r-- 1 aq10 aq10  26436 Sep 22 01:01 knapsack.s
-rw-rw-r-- 1 aq10 aq10 194391 Sep 22 01:05 knapsack_icc.s
(knuth)% wc -l knapsack_icc.s 
3460 knapsack_icc.s
```

The assembly file generated by `icc` is considerably larger and also looks quite different. 

```
(knuth)% more knapsack_icc.s 
(knuth)% more knapsack_gcc.s 
```


### <a name="performance"></a>Performance 

Now let's look at the performance differences of the generated code. 

```
(knuth)% g++ -o knapsack_gcc knapsack.cpp -fopenmp
(knuth)% perf stat ./knapsack_gcc input 1
Running knapsack with 1 threads.
Items: 20000   Capacity: 20000
Results saved in file results.dat 

 Performance counter stats for './knapsack_gcc input 1':

       6323.921790      task-clock (msec)         #    1.000 CPUs utilized          
                 6      context-switches          #    0.001 K/sec                  
                 0      cpu-migrations            #    0.000 K/sec                  
           390,937      page-faults               #    0.062 M/sec                  
    14,717,283,882      cycles                    #    2.327 GHz                    
     3,925,998,270      stalled-cycles-frontend   #   26.68% frontend cycles idle   
     1,688,498,193      stalled-cycles-backend    #   11.47% backend cycles idle    
    35,933,942,894      instructions              #    2.44  insn per cycle         
                                                  #    0.11  stalled cycles per insn
     3,503,180,735      branches                  #  553.957 M/sec                  
         3,045,630      branch-misses             #    0.09% of all branches        

       6.324724347 seconds time elapsed
```

Let's try `icc`. 

```
(knuth)% icc -o knapsack_icc knapsack.cpp -openmp
(knuth)% perf stat ./knapsack_icc input 1
Running knapsack with 1 threads.
Items: 20000   Capacity: 20000
Results saved in file results.dat 

 Performance counter stats for './knapsack_icc input 1':

       2157.929547      task-clock (msec)         #    0.999 CPUs utilized          
                15      context-switches          #    0.007 K/sec                  
                12      cpu-migrations            #    0.006 K/sec                  
           390,969      page-faults               #    0.181 M/sec                  
     4,556,832,452      cycles                    #    2.112 GHz                    
     1,570,510,758      stalled-cycles-frontend   #   34.46% frontend cycles idle   
     1,140,771,161      stalled-cycles-backend    #   25.03% backend cycles idle    
     8,986,335,809      instructions              #    1.97  insn per cycle         
                                                  #    0.17  stalled cycles per insn
     1,919,462,192      branches                  #  889.493 M/sec                  
         2,131,077      branch-misses             #    0.11% of all branches        

       2.159027952 seconds time elapsed
```

This comparison is not totally fair. _Why_?

The default optimization level in `gcc` is `-O0`. Let's re-compile and look at performance at `-O3`.

```
(knuth)% g++ -o knapsack_gcc knapsack.cpp -fopenmp -O3 
(knuth)% perf stat ./knapsack_gcc input 1
Running knapsack with 1 threads.
Items: 20000   Capacity: 20000
Results saved in file results.dat 

 Performance counter stats for './knapsack_gcc input 1':

       2373.841928      task-clock (msec)         #    1.000 CPUs utilized          
                 1      context-switches          #    0.000 K/sec                  
                 0      cpu-migrations            #    0.000 K/sec                  
           390,935      page-faults               #    0.165 M/sec                  
     4,732,596,959      cycles                    #    1.994 GHz                    
     1,991,945,706      stalled-cycles-frontend   #   42.09% frontend cycles idle   
     1,469,143,072      stalled-cycles-backend    #   31.04% backend cycles idle    
     8,984,763,204      instructions              #    1.90  insn per cycle         
                                                  #    0.22  stalled cycles per insn
     1,620,515,603      branches                  #  682.655 M/sec                  
         2,804,623      branch-misses             #    0.17% of all branches        

       2.374381403 seconds time elapsed
```

```
(knuth)% clang++ -o knapsack_clang knapsack.cpp -fopenmp -O3
(knuth)% perf stat ./knapsack_clang input 1
Running knapsack with 1 threads.
Items: 20000   Capacity: 20000
Results saved in file results.dat 

 Performance counter stats for './knapsack_clang input 1':

       2580.984862      task-clock (msec)         #    0.999 CPUs utilized          
                14      context-switches          #    0.005 K/sec                  
                12      cpu-migrations            #    0.005 K/sec                  
           390,971      page-faults               #    0.151 M/sec                  
     5,138,151,665      cycles                    #    1.991 GHz                    
     1,805,540,747      stalled-cycles-frontend   #   35.14% frontend cycles idle   
     1,174,927,351      stalled-cycles-backend    #   22.87% backend cycles idle    
    10,735,111,280      instructions              #    2.09  insn per cycle         
                                                  #    0.17  stalled cycles per insn
     1,710,990,427      branches                  #  662.922 M/sec                  
         2,154,794      branch-misses             #    0.13% of all branches        

       2.582872269 seconds time elapsed
```

```
(knuth)% icc -o knapsack_icc knapsack.cpp -openmp -O3
(knuth)% perf stat ./knapsack_icc input 1
Running knapsack with 1 threads.
Items: 20000   Capacity: 20000
Results saved in file results.dat 

 Performance counter stats for './knapsack_icc input 1':

       2265.316170      task-clock (msec)         #    1.000 CPUs utilized          
                13      context-switches          #    0.006 K/sec                  
                12      cpu-migrations            #    0.005 K/sec                  
           390,973      page-faults               #    0.173 M/sec                  
     4,509,580,733      cycles                    #    1.991 GHz                    
     1,529,919,309      stalled-cycles-frontend   #   33.93% frontend cycles idle   
     1,110,872,518      stalled-cycles-backend    #   24.63% backend cycles idle    
     8,966,171,403      instructions              #    1.99  insn per cycle         
                                                  #    0.17  stalled cycles per insn
     1,919,497,167      branches                  #  847.342 M/sec                  
         2,010,495      branch-misses             #    0.10% of all branches        

       2.266405112 seconds time elapsed
```

Note, although the performances are similar. They are not similar for the same reasons. 

_What about parallel performance?_

Let's look at performance scalability of the three versions at 1, 2, 4, 8 and 16 threads. 
```
(knuth)% g++ -o knapsack_gcc -O3 -fopenmp knapsack.cpp 
(knuth)% for i in 1 2 4 8 16; do echo -n -e "Threads $i\t"; (time ./knapsack_gcc input $i > /dev/null) 2>&1 | grep "real" ; done 
Threads 1	real	0m1.958s
Threads 2	real	0m1.649s
Threads 4	real	0m1.396s
Threads 8	real	0m1.443s
Threads 16	real	0m2.426s
```

```
(knuth)% clang++ -o knapsack_clang -O3 -fopenmp knapsack.cpp 
(knuth)% for i in 1 2 4 8 16; do echo -n -e "Threads $i\t"; (time ./knapsack_clang input $i > /dev/null) 2>&1 | grep "real" ; done 
Threads 1	real	0m2.141s
Threads 2	real	0m1.706s
Threads 4	real	0m1.609s
Threads 8	real	0m1.685s
Threads 16	real	0m2.606s
```

```
(knuth)% icc -o knapsack_icc -O3 -openmp knapsack.cpp 
(knuth)% for i in 1 2 4 8 16; do echo -n -e "Threads $i\t"; (time ./knapsack_icc input $i > /dev/null) 2>&1 | grep "real" ; done 
Threads 1	real	0m1.897s
Threads 2	real	0m1.657s
Threads 4	real	0m1.372s
Threads 8	real	0m1.712s
Threads 16	real	0m2.716s
```

The code is parallelized in a pipelined fashion. So, not a lot of gains with parallelization. Also, not
a lot of difference in the parallel performance of the three versions. 

Let's compare the performance obtained from sequential optimizations and the improvements with parallelization 

```
(knuth)% g++ -o knapsack_gcc knapsack.cpp -fopenmp 
(knuth)% time ./knapsack_gcc input 1
Running knapsack with 1 threads.
Items: 20000   Capacity: 20000
Results saved in file results.dat 

real	0m6.144s
user	0m5.336s
sys	    0m0.808s
(knuth)% g++ -o knapsack_gcc -fopenmp -O3 knapsack.cpp 
(knuth)% time ./knapsack_gcc input 1
Running knapsack with 1 threads.
Items: 20000   Capacity: 20000
Results saved in file results.dat 

real	0m1.969s
user	0m1.233s
sys	    0m0.736s
(knuth)% time ./knapsack_gcc input 4
Running knapsack with 4 threads.
Items: 20000   Capacity: 20000
Results saved in file results.dat 

real	0m1.400s
user	0m2.151s
sys	    0m0.698s
(knuth)% time ./knapsack_gcc input 1
```

Sequential optimizations dominate!

### <a name="optimizations"></a>Optimizations 

Let's look at the optimizations `gcc` is applying to achieve the performance improvements for the
sequential version. 

```
(knuth)% gcc -Q --help=optimizers 
The following options control optimizations:
  -O<number>                  		
  -Ofast                      		
  -Og                         		
  -Os                         		
  -faggressive-loop-optimizations 	[enabled]
  -falign-functions           		[disabled]
  -falign-jumps               		[disabled]
  -falign-labels              		[disabled]
  -falign-loops               		[disabled]
  -fassociative-math          		[disabled]
  -fasynchronous-unwind-tables 		[enabled]
  -fauto-inc-dec              		[enabled]
  -fbranch-count-reg          		[disabled]
  -fbranch-probabilities      		[disabled]
```

To count the number of optimizations applied, we can use the following command.

```
(knuth)% gcc -Q -O3 --help=optimizers | grep enabled | wc -l
142
```

Let's take a look at the optimizations applied by `clang`

```
(knuth)% clang++ -O3 -mllvm -debug-pass=Arguments -fopenmp knapsack.cpp
Pass Arguments:  -tti -targetlibinfo -tbaa -scoped-noalias -assumption-cache-tracker -ee-instrument -simplifycfg -domtree -sroa -early-cse -lower-expect
Pass Arguments:  -tti -targetlibinfo -tbaa -scoped-noalias -assumption-cache-tracker -profile-summary-info -forceattrs -inferattrs -callsite-splitting -ipsccp -called-value-propagation -globalopt -domtree -mem2reg -deadargelim -domtree -basicaa -aa -loops -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instcombine -simplifycfg -basiccg -globals-aa -prune-eh -inline -functionattrs -argpromotion -domtree -sroa -basicaa -aa -memoryssa -early-cse-memssa -domtree -basicaa -aa -lazy-value-info -jump-threading -lazy-value-info -correlated-propagation -simplifycfg -domtree -basicaa -aa -loops -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instcombine -libcalls-shrinkwrap -loops -branch-prob -block-freq -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -pgo-memop-opt -domtree -basicaa -aa -loops -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -tailcallelim -simplifycfg -reassociate -domtree -loops -loop-simplify -lcssa-verification -lcssa -basicaa -aa -scalar-evolution -loop-rotate -licm -loop-unswitch -simplifycfg -domtree -basicaa -aa -loops -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instcombine -loop-simplify -lcssa-verification -lcssa -scalar-evolution -indvars -loop-idiom -loop-deletion -loop-unroll -mldst-motion -aa -memdep -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -gvn -basicaa -aa -memdep -memcpyopt -sccp -domtree -demanded-bits -bdce -basicaa -aa -loops -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instcombine -lazy-value-info -jump-threading -lazy-value-info -correlated-propagation -domtree -basicaa -aa -memdep -dse -loops -loop-simplify -lcssa-verification -lcssa -aa -scalar-evolution -licm -postdomtree -adce -simplifycfg -domtree -basicaa -aa -loops -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instcombine -barrier -elim-avail-extern -basiccg -rpo-functionattrs -globalopt -globaldce -basiccg -globals-aa -float2int -domtree -loops -loop-simplify -lcssa-verification -lcssa -basicaa -aa -scalar-evolution -loop-rotate -loop-accesses -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -loop-distribute -branch-prob -block-freq -scalar-evolution -basicaa -aa -loop-accesses -demanded-bits -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -loop-vectorize -loop-simplify -scalar-evolution -aa -loop-accesses -loop-load-elim -basicaa -aa -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instcombine -simplifycfg -domtree -loops -scalar-evolution -basicaa -aa -demanded-bits -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -slp-vectorizer -opt-remark-emitter -instcombine -loop-simplify -lcssa-verification -lcssa -scalar-evolution -loop-unroll -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instcombine -loop-simplify -lcssa-verification -lcssa -scalar-evolution -licm -alignment-from-assumptions -strip-dead-prototypes -globaldce -constmerge -domtree -loops -branch-prob -block-freq -loop-simplify -lcssa-verification -lcssa -basicaa -aa -scalar-evolution -branch-prob -block-freq -loop-sink -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instsimplify -div-rem-pairs -simplifycfg
Pass Arguments:  -domtree
Pass Arguments:  -domtree
Pass Arguments:  -tti -targetlibinfo -assumption-cache-tracker -targetpassconfig -machinemoduleinfo -tbaa -scoped-noalias -collector-metadata -profile-summary-info -machine-branch-prob -domtree -basicaa -aa -objc-arc-contract -pre-isel-intrinsic-lowering -atomic-expand -domtree -basicaa -loops -loop-simplify -scalar-evolution -iv-users -loop-reduce -expandmemcmp -gc-lowering -shadow-stack-gc-lowering -unreachableblockelim -domtree -loops -branch-prob -block-freq -consthoist -partially-inline-libcalls -post-inline-ee-instrument -scalarize-masked-mem-intrin -expand-reductions -domtree -interleaved-access -indirectbr-expand -domtree -loops -codegenprepare -rewrite-symbols -domtree -dwarfehprepare -safe-stack -stack-protector -domtree -basicaa -aa -loops -branch-prob -isel -machinedomtree -expand-isel-pseudos -x86-domain-reassignment -tailduplication -opt-phis -slotindexes -stack-coloring -localstackalloc -dead-mi-elimination -machinedomtree -machine-loops -machine-trace-metrics -early-ifcvt -machine-combiner -x86-cmov-conversion -machinedomtree -machine-loops -machinelicm -machine-cse -machinepostdomtree -machine-block-freq -machine-sink -peephole-opt -dead-mi-elimination -lrshrink -x86-cf-opt -detect-dead-lanes -processimpdefs -unreachable-mbb-elimination -livevars -machinedomtree -machine-loops -phi-node-elimination -twoaddressinstruction -slotindexes -liveintervals -simple-register-coalescing -rename-independent-subregs -machine-scheduler -machine-block-freq -livedebugvars -livestacks -virtregmap -liveregmatrix -edge-bundles -spill-code-placement -lazy-machine-block-freq -machine-opt-remark-emitter -greedy -virtregrewriter -stack-slot-coloring -machinelicm -edge-bundles -machine-block-freq -machinepostdomtree -shrink-wrap -lazy-machine-block-freq -machine-opt-remark-emitter -prologepilog -branch-folder -tailduplication -machine-cp -postrapseudos -machinedomtree -machine-loops -post-RA-sched -gc-analysis -machine-block-freq -machinepostdomtree -block-placement -x86-execution-deps-fix -machinedomtree -machine-loops -x86-fixup-bw-insts -x86-fixup-LEAs -x86-evex-to-vex-compress -funclet-layout -stackmap-liveness -livedebugvalues -fentry-insert -machinedomtree -machine-loops -xray-instrumentation -patchable-function -lazy-machine-block-freq -machine-opt-remark-emitter -machinedomtree -machine-loops
```

To count the number of optimizations applied we can use the following command.
```
(knuth)% clang++ -O3 -mllvm -debug-pass=Arguments -fopenmp knapsack.cpp 2>&1 | awk '{print NF}'
13
244
3
3
143
```

`clang` is applying many more than `gcc` but some optimizations may be repeated. Also, just because
an optimization is being applied doesn't mean that is yielding in performance benefits. In fact, in
some cases, an optimization can degrade performance. 








