#!/bin/bash

# nthreads=$(grep -E 'int nthreads = [0-9]+' CG/cg.cpp | sed -E 's/.*int nthreads = ([0-9]+);.*/\1/')
# export OMP_NUM_THREADS=${nthreads}

# get thread num from the command line

class=A

enable_all_flag() {
    for VAR in {1..15}; do
    if [ $VAR -eq 5 ] || [ $VAR -eq 3 ]; then
        continue
    fi
        sed -i "/omp_flags_${VAR}_/ s|^[^#]*||" "CG/cg.cpp"
    done
}

disable_all_flag() {
    for VAR in {1..15}; do
    if [ $VAR -eq 5 ] || [ $VAR -eq 3 ]; then
        continue
    fi
    sed -i "/omp_flags_${VAR}_/ s|^[[:space:]]*|// &|" "CG/cg.cpp"
    done
}

make_and_run() {
    class=$1
    OMP_NUM_THREADS=$2
    flag=$3
    make cg CLASS=${class} > /dev/null
    ls -lah --time-style=+'%H:%M:%S' bin/cg.${class}
    sleep 1
    bin/cg.${class} ${OMP_NUM_THREADS} > result/${class}/${flag}-${OMP_NUM_THREADS}.log
}


export OMP_NUM_THREADS=1
disable_all_flag
make_and_run ${class} 1 conf_rolled_0
for thread in 1 2 4 8 12 16 20 24 28 32 36 40 44 48 52 56 60 64 68 72 76 80 84 88 92 96; do
    export OMP_NUM_THREADS=$1
    enable_all_flag
    make_and_run ${class} $thread conf_rolled_1
done

python3 analysis.py ${class}
