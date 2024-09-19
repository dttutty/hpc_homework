## LibTooling from Scratch

### Description

This tutorial provides a basic introduction to LLVM LibTooling. LibTooling is a collection of
libraries that support the development of standalone code refactoring and analysis tools based on Clang. A set
of pre-built LibTools are included in the LLVM package (build with `clang-tools-extra` in cmake). These
are referred to as Clang Tools. 

The tutorial borrows from 

   * [LLVM 12 DocumentationL LibTooling ](https://clang.llvm.org/docs/LibTooling.html)
   * [Libtooling - Basics of how to write a tool using LibTooling](https://freecompilercamp.org/libtooling/)

Both have a few pitfalls and may not work out of the box. Also, this tutorial is aimed at folks who
are new to LLVM and tries to provide additional explanations in each step. 

### Outline 

  * [Obtaining LLVM source](#obtaining_source)
  * [Configuring the Environment](#configuring)
  * [Building LLVM](#building)
  * [Installing LLVM](#installing)
  * [Hello World!](#hello_world)
  * [Running the LibTool on C++ code](#running)
  

### <a name="obtaining_source"></a>Obtaining LLVM source 

For this tutorial, we will use `shadowfax`. First let's check if LLVM is installed. 
```
(shadowfax)% which clang
/usr/bin/clang
```

Yes. 

If `clang` is not installed you can do a system-level installation on Ubuntu systems with the
following. 
```
(shadowfax)% sudo apt-get install clang
```

Let's check the version number. 
```
(shadowfax)% clang --version 
clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final)
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /usr/bin
```

If you want to build your own LLVM-based tools, LLVM must be built and installed from source. This
means that you will typically have multiple version of  `clang` on your system. During development,
it is important to make sure that the relevant paths are pointing to the right installation of
LLVM. You should get the latest (LLVM 12 at the time of writing this tutorial) or a fairly recent version of
the source tree. You can obtain the most recent source from the LLVM GiHub. 

```
(shadowfax)% git clone https://github.com/llvm/llvm-project.git 
```

The above pulls in all the required tools and components needed to get started with LLVM.

[ time on `shadowfax.cs.txstate.edu` 21m ]

### <a name="configuring"></a>Configuring the Environment

#### Source and Build Directories 

The forked repo in `llvm_project/` is called the _source_ directory. We will refer to this directory
as `$LLVM_SRC` in the rest of the tutorial. `$LLVM_SRC` contains the core LLVM source under
`llvm_project/llvm`. Although it is possible to build LLVM inside the source directory, 
it is not recommended. You want to create a separate _build_ directory outside of the source
tree. We will refer to this directory as the `$LLVM_BUILD`. 

```
(shadowfax)% mkdir $HOME/llvm
```

You can create multiple LLVM builds from the same source. 

#### CMake 
LLVM uses [CMake](https://cmake.org/) for the build system. If you do not have `cmake`, you will
need to install it.

```
(shadowfax)% sudo apt-get install cmake
```

```
(shadowfax)% which cmake
/usr/bin/cmake
(shadowfax)% cmake --version
cmake version 3.10.2

CMake suite maintained and supported by Kitware (kitware.com/cmake).
```

Note, the default installation on Ubuntu is likely to be older than what LLVM needs. For example,
LLVM 12 requires `cmake` 3.13.4 or newer. It won't build without this.  You can get the most recent
version of `cmake` from the Kitware GitHub.

```
(shadowfax)% git clone https://github.com/Kitware/CMake.git
```

Note, CMake is now maintained and supported by [Kitware](https://www.kitware.com/). The previous
CMake git url as listed in some tutorials is no longer valid. 

Now, we can build and install CMake with the following. 

```
(shadowfax)% cd CMake/
(shadowfax)% ./bootstrap
(shadowfax)% make
(shadowfax)% sudo make install 
```

You may get an error while bootstrapping if your system does not have an OpenSSL development
library. If you do get that error, you can install the library with 

```
sudo apt-get install libssl-dev
```

Once `ssl-dev` is installed, rerun `bootstrap`.

Since Libtooling requires re-building LLVM, it is good to familiarize yourself with CMake
basics. The CMake generated makefiles are almost unreadable and are not meant to be edited. So you
can't use your makefile expertise to tweak the build system. 


### <a name="building"></a>Building LLVM 

The build commands are run from inside `$LLVM_BUILD` and references `$LLVM_SRC`.

```
(shadowfax)% cd $HOME/llvm
```

We first run `cmake` to generate the Makefiles.

```
(shadowfax)% time cmake -G "Unix Makefiles" -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra"
-DCMAKE_BUILD_TYPE=Release -DLLVM_USE_LINKER=gold  -DCMAKE_INSTALL_PREFIX=$HOME/llvm ~/llvm-project/llvm
```

The above will generate Makefiles for `clang` and several other associated libraries and tools. 
`clang-extra-tools` is the one we need for Libtooling. The others are optional but might be a good
idea to build them anyway. 

Now we just `make` from inside the build directory. We can run make in parallel using the `-j` flag. 

```
(shadowfax)% make -j8
```

[ time on `shadowfax`  1h ]


### <a name="installing"></a>Installing LLVM

Now we want to put the headers, objects and executables in the right locations.

```
(shadowfax)% make install 
```

The above will put everything under `$HOME/llvm`. You want to update your `PATH` to point to this
installation of LLVM. Prepend the new LLVM path to your `PATH` variable in `.bashrc`. 

```
export PATH=$HOME/llvm/bin:$PATH
```

### <a name="hello_world"></a>Hello World!

The source code for out LibTool will reside in `clang-tool-extra` directory. Each LibTool should
have its own subdirectory under `clang-tools-extra`. 

```
cd $LLVM_SRC/clang-tools-extra
mkdir hello-world
```

Now we need to update and create the CMake files so that our tool can be built with the
supporting LibTooling libraries. First, we will edit the CMakeLists.txt in
`llvm-project/clang-tools-extra`. We only need to add one line. 

```
add_subdirectory(hello-world-pass) 
```

Instead of editing the CMake file, you can use the following to append to the file 

```
echo "add_subdirectory(hello-world-pass)" >> CMakeLists.txt
```

Now we will create a new CMakeLists.txt file in `llvm-project/clang-tools-extra/hello-world`. You
can use the following template. This template will work for many of the LibTools you want to write. 

```C
set(LLVM_LINK_COMPONENTS support)

add_clang_executable(NAME-OF-TOOL
  SRC.cpp                                                                              
  )                                                                                           
target_link_libraries(NAME-OF-TOOL                                                        
  PRIVATE                                                                                     
  clangTooling                                                                                
  clangBasic                                                                                  
  clangASTMatchers                                                                            
  )                                                                                           
```

`SRC` should be replaced with the name of the source file (you can have multiple). `NAME-OF-TOOL`
should be replaced with the actual name. The name doesn't have to be the same as the directory name
but it usually is. 
    

Now we are ready to write our first LibTool. 

```C++
/*                                                                                            
 *  The simplest LibTool                                                                      
 */

#include "clang/Frontend/FrontendActions.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"

using namespace std;
using namespace clang;
using namespace clang::driver;
using namespace clang::tooling;
using namespace llvm;

static cl::OptionCategory MyToolCategory("NAME_OF_TOOL options");

int main(int argc, const char **argv) {

  // parse command-line args passed to your code                                              
  CommonOptionsParser op(argc, argv, MyToolCategory);

  // create a new LibTooling instance                                                         
  ClangTool Tool(op.getCompilations(), op.getSourcePathList());

  // run the LibTool                                                                          
  // the tool creates a new FrontEndAction that just checks the syntax of the input file      
  // need the return value to send to LLVM                                                    
  int result = Tool.run(newFrontendActionFactory<NAME_OF_ACTION>().get());

  // send result to LLVM                                                                      
  return result;
}
```

The simplest LibTool requires a `main()` with just three statements: (i) parse the command-line
arguments (ii) create a new LibTooling instance and (iii) run the tool on the input. We need to make two
changes to this basic template. Replace `NAME_OF_TOOL` with the name that we want to give our tool
and replace `NAME_OF_ACTION` with the action we want our tool to perform. You can choose from among
24 actions (as of LLVM 12) pre-defined in `clang/Frontend/FrontendActions.h`. Let's choose the 
`SyntaxOnlyAction` which will simply make sure that the input program is syntactically correct. 

```C
static cl::OptionCategory MyToolCategory("Hello World options");
int result = Tool.run(newFrontendActionFactory<SyntaxOnlyAction>().get());
```

Just so we know that our tool is actually doing something, let's add a Hello World statement after the tool has
finished running. Although it is possible to use C++ I/O routines in LibTools, it is recommended
that we use LLVM I/O instead. 

```C
llvm::outs() << "Hello World!\n";
```

Note, the usage is similar but not identical to C++ I/O. 


### <a name="run"></a>Running the LibTool on C++ Code

Now let's build our tool. 

```
cd $LLVM_BUILD
make 
```

The first time we build our tool, we need to run make without any arguments. This will update the CMake
files we created. For subsequent builds we can specify the name of the tool as argument. 

```
make hello-world
```

Now let's try it out on some real code. We will use one of the NPB codes from Homework 1. 

```
(ada)% p ~/CS7331.git/NPB/CG
(ada)% ~/llvm/bin/hello-world cg.cpp 
```

**What happened**?

The compiler is looking for `npb-CPP.hpp` which is not in the current directory. We can specify the
include path to our LibTool as follows 

```
(base) (ada)% ~/llvm/bin/hello-world cg.cpp -- -I../common
```
















