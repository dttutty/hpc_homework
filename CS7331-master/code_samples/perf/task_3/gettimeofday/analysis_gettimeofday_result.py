import os
import re
import numpy as np
import matplotlib.pyplot as plt

root_dir = '/home/Students/sqp17/hpc_homework/CS7331-master/code_samples/perf/task_3/gettimeofday'
sub_dirs = ['test_1', 'test_2', 'test_3', 'test_4', 'test_5']

arg_try_times = 20

matrix_matchs = [ [] for _ in range(arg_try_times)]
total_matchs = [ [] for _ in range(arg_try_times)]

time_pattern = re.compile(r'(\d+)m(\d+\.\d+)s')

def convert_to_seconds(time_str):
    match = time_pattern.match(time_str)
    if match:
        minutes = int(match.group(1))
        seconds = float(match.group(2))
        return minutes * 60 + seconds
    return None

for i in range(arg_try_times):
    n = (i+1) * 500
    for sub_dir in sub_dirs:
        with open(os.path.join(root_dir,sub_dir,f"N={n}.txt"), 'r') as file:
            content = file.read()
            flops = 2 * n**2
            matrix_pattern = re.compile(r'matrix_vector_mult execution time: ([\d.]+) ms')
            matrix_match = matrix_pattern.search(content)
            matrix_matchs[i].append(float(matrix_match.group(1))/flops)
            total_pattern = re.compile(r'total execution time: ([\d.]+) ms')
            total_match = total_pattern.search(content)
            total_matchs[i].append(float(total_match.group(1))/flops)

matrix_matchs = np.mean(matrix_matchs, axis=1)*1000
total_matchs = np.mean(total_matchs, axis=1)*1000

n_values = np.arange(500, 10001, 500)

plt.plot(n_values, matrix_matchs, marker='o', linestyle='-', color='red', label='matrix_vector_mult() execution time', markersize=2, linewidth=0.5)
plt.plot(n_values, total_matchs, marker='o', linestyle='-', color='blue', label='main() execution time', markersize=2, linewidth=0.5)

# 设置坐标轴标签和标题
plt.xlabel('N')
plt.ylabel('Time Duration (us)')
plt.title('measured by `perf` command')

# 添加网格线
plt.grid(True, linestyle='--', alpha=0.7)

# 显示图例
plt.legend()

# 显示图形
plt.savefig(os.path.join(root_dir,f"result_per_flop.png"))