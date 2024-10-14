import matplotlib.pyplot as plt


plt.xlim(left=0)  # x轴从0开始
plt.ylim(bottom=0)  # y轴从0开始

threads = []
mops_mean = []
mops_std = []
no_parallel_mops = 0
import os
import sys
if len(sys.argv) != 2:
    print("Usage: python draw.py <class_type>")
    sys.exit(1)

class_type = sys.argv[1]
file_path = class_type + ".log"

plt.figure(figsize=(10, 6))

with open(file_path, 'r') as file:
    lines = file.readlines()
    for line in lines[1:]:
        parts = line.split()
        if parts[0] == 'conf_rolled_0':
            no_parallel_mops = float(parts[2])
        else:
            threads.append(int(parts[1]))
            mops_mean.append(float(parts[2]))
            mops_std.append(float(parts[3]))
            
# sort data      
plt.figure(figsize=(10, 6))
sorted_data = sorted(zip(threads, mops_mean, mops_std))
threads_sorted, mops_mean_sorted, mops_std_sorted = zip(*sorted_data)


plt.errorbar(threads_sorted, mops_mean_sorted, yerr=mops_std_sorted, fmt='o', linestyle='-', color='b', ecolor='gray', elinewidth=2, capsize=5)
for x, y in zip(threads_sorted, mops_mean_sorted):
    plt.plot([x, x], [0, y], linestyle='--', color='gray')
plt.axhline(y=no_parallel_mops, color='gray', linestyle='--')
plt.text(50, no_parallel_mops, 'No Parallel or SIMD', color='r', va='center')
plt.text(-20, no_parallel_mops, f'{no_parallel_mops:.0f}', color='red', va='center', ha='left')

max_index = mops_mean_sorted.index(max(mops_mean_sorted))
max_threads = threads_sorted[max_index]
max_mops = mops_mean_sorted[max_index]
plt.text(max_threads, max_mops, f'Max Mop/s: {max_mops:.0f}\nThreads: {max_threads} ', color='red', va='bottom', ha='left')
plt.scatter(max_threads, max_mops, color='red', zorder=5)


plt.title('Mop/s vs Threads')
plt.xlabel('Threads')
plt.ylabel('Mop/s')

plt.grid(True)
plt.savefig(class_type + ".png")
