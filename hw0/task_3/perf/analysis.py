import os
import re
import numpy as np
import matplotlib.pyplot as plt

root_dir = '/home/Students/sqp17/hpc_homework/CS7331-master/code_samples/perf/task_3/perf'
sub_dirs = ['test_1', 'test_2', 'test_3', 'test_4', 'test_5']

arg_try_times = 20

elapsed_matchs = [ [] for _ in range(arg_try_times)]
user_matchs = [ [] for _ in range(arg_try_times)]
sys_matchs = [ [] for _ in range(arg_try_times)]

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
            elapsed_match = re.search(r"(\d+\.\d+) seconds time elapsed", content)
            elapsed_matchs[i].append(float(elapsed_match.group(1))/flops)
            user_match = re.search(r"(\d+\.\d+) seconds user", content)
            user_matchs[i].append(float(user_match.group(1))/flops)
            sys_match = re.search(r"(\d+\.\d+) seconds sys", content)
            sys_matchs[i].append(float(sys_match.group(1))/flops)

elapsed_matchs = np.mean(elapsed_matchs, axis=1)*1000000

user_matchs = np.mean(user_matchs, axis=1)*1000000

sys_matchs = np.mean(sys_matchs, axis=1)*1000000


n_values = np.arange(500, 10001, 500)

# 使用 errorbar 绘制带有误差线的折线图
plt.plot(n_values, elapsed_matchs, marker='o', linestyle='-', color='red', label='time elapsed', markersize=2, linewidth=0.5)
plt.plot(n_values, user_matchs, marker='o', linestyle='-', color='blue', label='user', markersize=2, linewidth=0.5)
plt.plot(n_values, sys_matchs, marker='o', linestyle='-', color='yellow', label='sys', markersize=2, linewidth=0.5)

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
# name = r"$\bar{x}$"