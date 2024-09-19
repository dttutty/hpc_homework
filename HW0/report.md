

Experimental Environment
=
1. Env: Github Workspace

- Host name
```bash
@dttutty ➜ /workspaces/hpc_homework (main) $  hostname
codespaces-4bf82d
```
- CPU manufacturer, model, and clock rate.
```bash
@dttutty ➜ /workspaces/hpc_homework (main) $ lscpu
Vendor ID:  AuthenticAMD
Model name: AMD EPYC 7763 64-Core Processor
CPU MHz:    3242.790
```
- Number of physical cores and logical cores
```bash
@dttutty ➜ /workspaces/hpc_homework (main) $ cat /proc/cpuinfo | grep "cpu cores" | uniq
cpu cores       : 1
@dttutty ➜ /workspaces/hpc_homework (main) $ cat /proc/cpuinfo | grep "processor" | wc -l
2
```