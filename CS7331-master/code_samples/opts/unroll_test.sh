#!/bin/bash

# assumes a C source file 
src=$1
basename=`echo $src | awk -F "." '{print $1}'` 

# save the original 
cp $src $src.orig

input_size=10000
reps=10

unroll_factors="1 2 4 8 10  20 50 100 200 400 800 1000"
for uf in ${unroll_factors}; do
	sed "s/UNROLL 1/UNROLL $uf"/ $src.orig > tmp
	mv tmp $src

	# Rpass flag to check if loop is being unrolled
	# prevent clang from vectorizing loop
	clang -O1 -Rpass=unroll -mllvm -vectorize-loops=0 -o ${basename} $src 2> /dev/null

	# if we want to do perf ...
	#	time=`perf stat ./${basename} ${input_size} ${reps} 2>&1 | grep "seconds time" | awk '{print $1}'`;

	# extract exection time of target loop from built-in timer 
	time=`./${basename} ${input_size} ${reps} 2>&1 | grep "Loop" | awk '{print $5}'`;

	echo -e "$uf\t$time"
done 

# restore orginal 
mv $src.orig $src
