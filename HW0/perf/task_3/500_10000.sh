#!/bin/bash
command = "time"
mkdir -p task_3/time/test_1
mkdir -p task_3/time/test_2
mkdir -p task_3/time/test_3
mkdir -p task_3/time/test_4
mkdir -p task_3/time/test_5
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { time ./a.out $i 100; } > task_3/time/test_1/N=$i.txt  2>&1
done
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { time ./a.out $i 100; }  > task_3/time/test_2/N=$i.txt  2>&1
done
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { time ./a.out $i 100; }   > task_3/time/test_3/N=$i.txt  2>&1
done
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { time ./a.out $i 100; }  > task_3/time/test_4/N=$i.txt  2>&1
done
for i in $(seq 500 500 10000)
do
    echo "正在处理 i=$i..."  # 显示当前处理的 i 值
    { time ./a.out $i 100; }  > task_3/time/test_5/N=$i.txt  2>&1
done
