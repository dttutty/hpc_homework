import os
import re
import numpy as np

# 定义目录路径
directory = '/你的/本地/路径/'

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
elapsed_mean = np.mean(time_elapsed)
elapsed_std = np.std(time_elapsed)

user_mean = np.mean(user_time)
user_std = np.std(user_time)

sys_mean = np.mean(sys_time)
sys_std = np.std(sys_time)

# 输出结果
print("Time Elapsed - Mean: {:.6f}, Std: {:.6f}".format(elapsed_mean, elapsed_std))
print("User Time - Mean: {:.6f}, Std: {:.6f}".format(user_mean, user_std))
print("Sys Time - Mean: {:.6f}, Std: {:.6f}".format(sys_mean, sys_std))
