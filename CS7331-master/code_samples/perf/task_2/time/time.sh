#!/bin/bash
arg1=$1
arg2=$2
for i in {1..10}
do
    mkdir -p time_result/${arg1}_${arg2}
    (time ./a.out $arg1 $arg2;) > time_result/${arg1}_${arg2}/$i.txt 2>&1
done