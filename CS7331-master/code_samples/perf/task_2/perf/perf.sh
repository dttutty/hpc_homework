#!/bin/bash
arg1=$1
arg2=$2
for i in {1..10}
do
    mkdir -p perf_result/${arg1}_${arg2}
    perf stat ./a.out $arg1 $arg2 > perf_result/${arg1}_${arg2}/$i.txt 2>&1
done