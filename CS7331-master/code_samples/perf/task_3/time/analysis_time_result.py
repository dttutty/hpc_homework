import os
import re
import numpy as np
import matplotlib.pyplot as plt

root_dir = '/home/Students/sqp17/hpc_homework/CS7331-master/code_samples/perf/task_3/time'
sub_dirs = ['test_1', 'test_2', 'test_3', 'test_4', 'test_5']

arg_try_times = 20

real_times = [ [] for _ in range(arg_try_times)]
user_times = [ [] for _ in range(arg_try_times)]
sys_times = [ [] for _ in range(arg_try_times)]

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
    flops = 2 * n**2
    for sub_dir in sub_dirs:
        with open(os.path.join(root_dir,sub_dir,f"N={n}.txt"), 'r') as file:
            for line in file:
                if line.startswith('real'):
                    real_time = convert_to_seconds(line.split()[1])
                    real_times[i].append(real_time)
                elif line.startswith('user'):
                    user_time = convert_to_seconds(line.split()[1])
                    user_times[i].append(user_time)
                elif line.startswith('sys'):
                    sys_time = convert_to_seconds(line.split()[1])
                    sys_times[i].append(sys_time)

real_mean = np.mean(real_times, axis=1)*1000
user_mean = np.mean(user_times, axis=1)*1000
sys_mean = np.mean(sys_times, axis=1)*1000


n_values = np.arange(500, 10001, 500)

# 使用 errorbar 绘制带有误差线的折线图
plt.plot(n_values, real_mean, marker='o', linestyle='-', color='red', label='real', markersize=2, linewidth=0.5)
plt.plot(n_values, user_mean, marker='o', linestyle='-', color='blue', label='user', markersize=2, linewidth=0.5)
plt.plot(n_values, sys_mean, marker='o', linestyle='-', color='yellow', label='sys', markersize=2, linewidth=0.5)

# 设置坐标轴标签和标题
plt.xlabel('N')
plt.ylabel('Time Duration (ms)')
plt.title('measured by `time` command')

# 添加网格线
plt.grid(True, linestyle='--', alpha=0.7)

# 显示图例
plt.legend()

# 显示图形
plt.savefig(os.path.join(root_dir,f"time_result.png"))
# name = r"$\bar{x}$"
