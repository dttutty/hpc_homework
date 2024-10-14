#!/bin/bash

# nthreads=$(grep -E 'int nthreads = [0-9]+' CG/cg.cpp | sed -E 's/.*int nthreads = ([0-9]+);.*/\1/')
# export OMP_NUM_THREADS=${nthreads}

# get class from the command line

enable_all_parallel() {
    sed -i "/omp_flags_/ s|^[^#]*||" "CG/cg.cpp"
}

disable_all_parallel() {
    sed -i "/omp_flags_/ s|^[[:space:]]*|// &|" "CG/cg.cpp"
}

run() {
    class=$1
    OMP_NUM_THREADS=$2
    flag=$3
    iter=$4
    ls -lah --time-style=+'%H:%M:%S' bin/cg.${class}
    sleep 0.1
    bin/cg.${class} ${OMP_NUM_THREADS} >result/${class}/${iter}/${flag}-${OMP_NUM_THREADS}.log
}

for iter in {0..1}; do
    for class in S W A B C; do
        export OMP_NUM_THREADS=1
        disable_all_parallel
        make cg CLASS=${class} >/dev/null
        run ${class} 1 conf_rolled_0 ${iter}
        for thread in 1 2 $(seq 4 4 150); do
            export OMP_NUM_THREADS=$1
            enable_all_parallel
            make cg CLASS=${class} >/dev/null
            run ${class} $thread conf_rolled_1 ${iter}
        done
    done
done

# python3 analysis.py ${class}
