#!/bin/sh

prog=$1
i=500
while [ $i -le 4000 ]; do 
#	L1=`perf stat -e L1-dcache-loads,L1-dcache-load-misses ./$prog $i 2>&1 | grep hits | awk '{print $4}'`
	LLC=`perf stat -e LLC-loads,LLC-load-misses ./$prog $i 2>&1 | grep hits | awk '{print $4}'` 
	echo "$i\t$LLC"
  i=$(($i+500))
done
