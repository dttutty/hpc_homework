#!/bin/bash


prog=$1
block=$2

[ "$prog" ] || { echo "No program specified. Exiting ..."; exit 0; }
[ -x $prog ] || { echo "Could not find exectutable $prog. Exiting ..."; exit 0; }

[ "$block" ] || { block=0; echo "**Warning** no block size specified; running code without block sizes"; }


lb=500     # input lower bound 
ub=4000    # input upper bound 
step=500   # step size 

i=$lb
echo -e "input\tLLC miss rate\tGFLOPs/s"

while [ $i -le $ub ]; do 
	if [ $block -eq 0 ]; then
	  perf stat -e LLC-loads,LLC-load-misses,fp_comp_ops_exe.sse_scalar_single ./$prog $i &> tmp.out
	else
	  perf stat -e LLC-loads,LLC-load-misses,fp_comp_ops_exe.sse_scalar_single ./$prog $i $block &> tmp.out
	fi
  LLC=`cat tmp.out | grep hits | awk '{print $4}'` 
	flops=`cat tmp.out | grep fp_ | awk '{print $1}' | sed 's/,//g'`
	secs=`cat tmp.out | grep elapsed | awk '{print $1}'`
  GFLOPs=`echo $flops $secs | awk '{printf "%3.2f", ($1/1e+09)/$2}'`
	
	echo -e "$i\t$LLC\t\t$GFLOPs"
	i=$(($i+$step))
done

rm -rf tmp.out
