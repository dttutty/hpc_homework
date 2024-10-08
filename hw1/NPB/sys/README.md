This directory contains utilities and files used by the build process. You should not need to change anything in this directory. 

Original Files
--------------
**`setparams.c`**  
Source for the setparams program. This program is used internally in the build process to create the file "npbparams.h" for each benchmark. npbparams.h contains Fortran or C parameters to build a benchmark for a specific class. The setparams program is never run directly by a user. Its invocation syntax is `setparams benchmark-name class`.  
It examines the file "npbparams.h" in the current directory. If the specified parameters are the same as those in the npbparams.h file, nothing it changed. If the file does not exist or corresponds to a different class/number of nodes, it is (re)built.  
One of the more complicated things in npbparams.h is that it contains, in a Fortran string, the compiler flags used to build a benchmark, so that a benchmark can print out how it was compiled. 

**`make.common`**  
A makefile segment that is included in each individual benchmark program makefile. It sets up some standard macros (COMPILE, etc) and makes sure everything is configured correctly (npbparams.h)

**`Makefile`**  
Builds setparams

**`README`**  
This file. 


Created files
-------------
**`setparams`**  
See descriptions above

