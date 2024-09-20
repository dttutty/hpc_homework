#!/bin/bash
arg1=$1
arg2=$2
for i in {1..10}
do
    mkdir -p gettimeofday_result/${arg1}_${arg2}
    (./a.out $arg1 $arg2;) > gettimeofday_result/${arg1}_${arg2}/$i.txt
done