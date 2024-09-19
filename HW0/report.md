

Experimental Environment
=
1. Env: Github Workspace

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
