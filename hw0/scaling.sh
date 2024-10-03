#!/bin/bash

EXEC_STR="$1"
threads="1 2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 42 44 46"

perf stat -e r538010 ./${EXEC_STR} 1 &> tmp.prof
flops=`cat tmp.prof | grep r538010  | awk '{print $1}' | sed 's/,//g'`
gigaflops=`echo $flops | awk '{printf "%3.2f", ($1/1e+09)}'`
ms=`cat tmp.prof | grep "elapsed"  | awk '{printf "%3.2f", $1 * 1e+03}'`
secs=`cat tmp.prof | grep "elapsed"  | awk '{printf $1}'`

for i in $threads; do
	time=`./${EXEC_STR} $i | grep ms | awk '{print $4}'`	
	if [ $i -eq 1 ]; then
			baseline=$time
	fi
	speedup=`echo "scale=2; $baseline/$time" | bc -q 2> /dev/null`  
	proximity_to_linear=`echo "scale=2; (1 - ($i - $speedup)/$i) * 100" | bc -q 2> /dev/null`

	FLOPS=`echo $flops $time | awk '{printf "%3.2f", ($1/1e+09)/($2/1e+03)}'`
	echo $i $time $speedup ${proximity_to_linear} ${FLOPS} #  ${gigaflops} ${ms}

done
