import os
import re
import numpy as np


dir = '/home/Students/sqp17/hpc_homework/CS7331-master/code_samples/perf/gettimeofday_result/100_1'

# 获取当前目录下的所有txt文件
txt_files = [f for f in os.listdir(dir) if f.endswith('.txt')]

# 定义存储 execution time 的列表
matrix_times = []
total_times = []

# 正则表达式匹配时间的模式
matrix_pattern = re.compile(r'matrix_vector_mult execution time: ([\d.]+) ms')
total_pattern = re.compile(r'total execution time: ([\d.]+) ms')

# 读取每个文件并提取 matrix_vector_mult 和 total 的时间
for txt_file in txt_files:
    with open(os.path.join(dir,txt_file), 'r') as file:
        content = file.read()
        matrix_match = matrix_pattern.search(content)
        total_match = total_pattern.search(content)
        
        if matrix_match:
            matrix_times.append(float(matrix_match.group(1)))
        
        if total_match:
            total_times.append(float(total_match.group(1)))

# 计算均值和方差
matrix_mean = np.mean(matrix_times)
matrix_std = np.std(matrix_times)

total_mean = np.mean(total_times)
total_std = np.std(total_times)

# 打印结果
name = r"$\bar{x}$"

print(f"Matrix_vector_mult time: {name}={matrix_mean:.4f}, $\sigma$={matrix_std:.4f}")
print(f"Total execution time: {name}={total_mean:.4f}, $\sigma$={total_std:.4f}")
