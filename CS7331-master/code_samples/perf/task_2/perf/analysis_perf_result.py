import os
import re
import numpy as np

# 定义目录路径
directory = 'CS7331-master/code_samples/perf/perf_result/100_1'

# 用于存储各个文件的结果
time_elapsed = []
user_time = []
sys_time = []

# 遍历文件并提取所需的数据
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        with open(os.path.join(directory, filename), 'r') as file:
            content = file.read()

            # 使用正则表达式提取时间数据
            elapsed_match = re.search(r"(\d+\.\d+) seconds time elapsed", content)
            user_match = re.search(r"(\d+\.\d+) seconds user", content)
            sys_match = re.search(r"(\d+\.\d+) seconds sys", content)

            if elapsed_match and user_match and sys_match:
                time_elapsed.append(float(elapsed_match.group(1)))
                user_time.append(float(user_match.group(1)))
                sys_time.append(float(sys_match.group(1)))

# 计算平均值和标准差
elapsed_mean = np.mean(time_elapsed)*1000
elapsed_std = np.std(time_elapsed)*1000

user_mean = np.mean(user_time)*1000
user_std = np.std(user_time)*1000

sys_mean = np.mean(sys_time)*1000
sys_std = np.std(sys_time)*1000

# 输出结果
name = r"$\bar{x}$"
print("Time Elapsed - {:s}={:.7f}, $\sigma$={:.7f}".format(name,elapsed_mean, elapsed_std))
print("User Time - {:s}={:.7f}, $\sigma$={:.7f}".format(name, user_mean, user_std))
print("Sys Time - {:s}={:.7f}, $\sigma$={:.7f}".format(name, sys_mean, sys_std))
