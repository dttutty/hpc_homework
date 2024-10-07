SHELL=/bin/sh
# 指定使用的 shell 程序为 /bin/sh。这个 shell 会被用来执行 makefile 中的命令。

BENCHMARK=cg
BENCHMARKU=CG
# 定义两个变量 BENCHMARK 和 BENCHMARKU，分别赋值为 'cg' 和 'CG'。这些变量可以用来指定不同的目标。

include ../config/make.def
# 包含另一个名为 make.def 的文件，其中定义了一些通用的编译选项或变量。这个文件位于上一级目录的 config 文件夹中。

OBJS = cg.o ${COMMON}/c_print_results.o  \
       ${COMMON}/c_${RAND}.o ${COMMON}/c_timers.o ${COMMON}/c_wtime.o
# 定义一个变量 OBJS，它列出了所有需要编译和链接的对象文件。
# cg.o 是当前目录中的文件，其他对象文件位于 ${COMMON} 目录下，并包含 c_print_results.o, c_timers.o, c_wtime.o 等。
# ${RAND} 是一个变量，用于动态替换为具体的文件名。

include ../sys/make.common
# 包含另一个 makefile 片段 make.common，它位于上一级目录的 sys 文件夹中。这通常是为了在不同的 makefile 之间复用一些公共的规则和变量。

${PROGRAM}: config ${OBJS}
	${CLINK} ${CLINKFLAGS} -o ${PROGRAM} ${OBJS} ${C_LIB}
# 定义了一个目标 ${PROGRAM}，依赖于 config 文件和所有的对象文件 ${OBJS}。
# 执行命令：用链接器 ${CLINK} 和选项 ${CLINKFLAGS}，将所有对象文件 ${OBJS} 链接成可执行文件 ${PROGRAM}，并链接必要的库 ${C_LIB}。

cg.o:		cg.cpp  npbparams.hpp
	${CCOMPILE} cg.cpp
# 定义目标 cg.o，它依赖于 cg.cpp 和 npbparams.hpp。
# 使用编译器 ${CCOMPILE} 编译 cg.cpp，生成 cg.o。

clean:
	- rm -f *.o *~ 
	- rm -f npbparams.hpp core
# 定义 clean 目标。这个目标用来清理生成的文件。不会自动执行，需要手动执行 `make clean`。
# 它删除所有 .o 文件、备份文件（*~）、npbparams.hpp 和 core dump 文件。
