import os
import re
import numpy as np

dir = 'HW0/perf/task_2/time/100_1'
txt_files = [f for f in os.listdir(dir) if f.endswith('.txt')]

real_times = []
user_times = []
sys_times = []

time_pattern = re.compile(r'(\d+)m(\d+\.\d+)s')

def convert_to_seconds(time_str):
    match = time_pattern.match(time_str)
    if match:
        minutes = int(match.group(1))
        seconds = float(match.group(2))
        return minutes * 60 + seconds
    return None

for txt_file in txt_files:
    with open(os.path.join(dir,txt_file), 'r') as file:
        for line in file:
            if line.startswith('real'):
                real_time = convert_to_seconds(line.split()[1])
                real_times.append(real_time)
            elif line.startswith('user'):
                user_time = convert_to_seconds(line.split()[1])
                user_times.append(user_time)
            elif line.startswith('sys'):
                sys_time = convert_to_seconds(line.split()[1])
                sys_times.append(sys_time)

real_mean = np.mean(real_times)*1000
real_std = np.std(real_times)*1000

user_mean = np.mean(user_times)*1000
user_std = np.std(user_times)*1000

sys_mean = np.mean(sys_times)*1000
sys_std = np.std(sys_times)*1000

name = r"$\bar{x}$"
print(f"Real time: {name}={real_mean:.1f}, $\sigma$={real_std:.1f}")
print(f"User time: {name}= {user_mean:.1f}, $\sigma$={user_std:.1f}")
print(f"Sys time: {name}= {sys_mean:.1f}, $\sigma$={sys_std:.1f}")
