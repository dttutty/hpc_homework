#!/bin/bash


#!/bin/bash

mkdir -p test_1/O0
mkdir -p test_1/O3
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { perf stat -e L1-icache-load-misses,L1-icache-loads,cache-misses,cache-references,L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses,instructions,stalled-cycles-frontend,stalled-cycles-backend,branches,branch-misses,page-faults,cpu-migrations  ../../O0.out $i 100; } > test_1/O0/$i.txt  2>&1
done
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { perf stat -e L1-icache-load-misses,L1-icache-loads,cache-misses,cache-references,L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses,instructions,stalled-cycles-frontend,stalled-cycles-backend,branches,branch-misses,page-faults,cpu-migrations  ../../O3.out $i 100; }  > test_1/O3/$i.txt  2>&1
done



#!/bin/bash

mkdir -p test_2/O0
mkdir -p test_2/O3
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { perf stat -e L1-icache-load-misses,L1-icache-loads,cache-misses,cache-references,L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses,instructions,stalled-cycles-frontend,stalled-cycles-backend,branches,branch-misses,page-faults,cpu-migrations  ../../O0.out $i 100; } > test_2/O0/$i.txt  2>&1
done
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { perf stat -e L1-icache-load-misses,L1-icache-loads,cache-misses,cache-references,L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses,instructions,stalled-cycles-frontend,stalled-cycles-backend,branches,branch-misses,page-faults,cpu-migrations  ../../O3.out $i 100; }  > test_2/O3/$i.txt  2>&1
done

#!/bin/bash

mkdir -p test_3/O0
mkdir -p test_3/O3
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { perf stat -e L1-icache-load-misses,L1-icache-loads,cache-misses,cache-references,L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses,instructions,stalled-cycles-frontend,stalled-cycles-backend,branches,branch-misses,page-faults,cpu-migrations  ../../O0.out $i 100; } > test_3/O0/$i.txt  2>&1
done
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { perf stat -e L1-icache-load-misses,L1-icache-loads,cache-misses,cache-references,L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses,instructions,stalled-cycles-frontend,stalled-cycles-backend,branches,branch-misses,page-faults,cpu-migrations  ../../O3.out $i 100; }  > test_3/O3/$i.txt  2>&1
done

#!/bin/bash

mkdir -p test_4/O0
mkdir -p test_4/O3
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { perf stat -e L1-icache-load-misses,L1-icache-loads,cache-misses,cache-references,L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses,instructions,stalled-cycles-frontend,stalled-cycles-backend,branches,branch-misses,page-faults,cpu-migrations  ../../O0.out $i 100; } > test_4/O0/$i.txt  2>&1
done
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { perf stat -e L1-icache-load-misses,L1-icache-loads,cache-misses,cache-references,L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses,instructions,stalled-cycles-frontend,stalled-cycles-backend,branches,branch-misses,page-faults,cpu-migrations  ../../O3.out $i 100; }  > test_4/O3/$i.txt  2>&1
done



mkdir -p test_5/O0
mkdir -p test_5/O3
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { perf stat -e L1-icache-load-misses,L1-icache-loads,cache-misses,cache-references,L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses,instructions,stalled-cycles-frontend,stalled-cycles-backend,branches,branch-misses,page-faults,cpu-migrations  ../../O0.out $i 100; } > test_5/O0/$i.txt  2>&1
done
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { perf stat -e L1-icache-load-misses,L1-icache-loads,cache-misses,cache-references,L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses,instructions,stalled-cycles-frontend,stalled-cycles-backend,branches,branch-misses,page-faults,cpu-migrations  ../../O3.out $i 100; }  > test_5/O3/$i.txt  2>&1
done


