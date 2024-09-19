# CS7331 Fall 2024
# Benchmarks 


## CPU 

  * [SPEC CPU 2017](https://www.spec.org/benchmarks.html#cpu). **Not Free** but CRL has a
    license. Must work on CRL machines. 
  * [MiBench](https://vhosts.eecs.umich.edu/mibench/). Primarily for embedded systems but can
    evaluate CPU performance as well.
  * [Polybench](https://github.com/MatthiasJReisinger/PolyBenchC-4.2.1.git). Numerical
    computations. Relatively easy to build and execute. 
  * [NAS Parallel Benchmarks](https://github.com/GMAP/NPB-CPP). Use this if you want to evaluate
    parallel performance. 
  * [PARSEC Benchmark Suite](https://github.com/bamos/parsec-benchmark). Benchmark suite for
    multi-threaded performance evaluation. Covers a wider domain than NAS. 
  * [Anghabench](https://github.com/brenocfg/AnghaBench). One million compilable C benchmarks. Can
    only compile codes cannot run them. 
	 
  
### GPU 

   * [CUDA SDK](https://developer.nvidia.com/cuda-downloads). Includes sample codes for evaluating
     NVIDIA GPUs. 
   * [Rodinia](https://www.cs.virginia.edu/rodinia/doku.php?id=start). Includes CUDA, OpenMP and
     OpenCL versions of the code 
   * [Parboil](https://github.com/abduld/Parboil). Compute-intensive CPU-GPU kernels 
   

### HPC 

   * [HPCC](https://hpcchallenge.org/hpcc/). Benchmarks used to evaluate HPC systems. Includes DGEM
     the key computation for top500 
   * [ECP Proxy Applications](https://proxyapps.exascaleproject.org/). Performance-critical
     computation "kernels" extracted from exascale applications. 
   * [OpenDwarfs](https://github.com/vtsynergy/OpenDwarfs). Suite consists of applications
     consisting of 13 most commonly used computation/communication patterns. 

### Generators 

   * [CSmith](https://github.com/csmith-project/csmith). Random C program generator. 
   * [CUDAsmith](https://github.com/gongbell/CUDAsmith). Random CUDA kernel generator. 
   * [Benchpress](https://github.com/fivosts/BenchPress). ML-driven benchmark generator. 
      
