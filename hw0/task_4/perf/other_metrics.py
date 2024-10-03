import os
import re
import numpy as np
import matplotlib.pyplot as plt

root_dir = 'hw0_code/task_4/perf'
sub_dirs_O0 = ['test_1/O0', 'test_2/O0', 'test_3/O0', 'test_4/O0', 'test_5/O0']
sub_dirs_O3 = ['test_1/O3', 'test_2/O3', 'test_3/O3', 'test_4/O3', 'test_5/O3']

arg_try_times = 20

metrics = ['icache_hit_percentages_o0', 'cache_ref_percentages_o0', 'dcache_hit_percentages_o0', 'branch_miss_percentages_o0', 'instructions_counts_o0', 'page_faults_counts_o0', 
           'cpu_migrations_counts_o0', 'icache_hit_percentages_o3', 'cache_ref_percentages_o3', 'dcache_hit_percentages_o3', 'branch_miss_percentages_o3', 'instructions_counts_o3', 'page_faults_counts_o3', 
           'cpu_migrations_counts_o3']

for metric in metrics:
    globals()[metric] = [[] for _ in range(arg_try_times)]

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
    kflops = flops/1000
    for sub_dir in sub_dirs_O0:
        with open(os.path.join(root_dir,sub_dir,f"{n}.txt"), 'r') as file:
            content = file.read()

            instructions_counts_o0[i].append(int(re.search(r'([\d,]+)\s+instructions', content).group(1).replace(',', ''))/flops if re.search(r'([\d,]+)\s+instructions', content) else None)
            page_faults_counts_o0[i].append(int(re.search(r'([\d,]+)\s+page-faults', content).group(1).replace(',', ''))/kflops if re.search(r'([\d,]+)\s+page-faults', content) else None)
            cpu_migrations_counts_o0[i].append(int(re.search(r'([\d,]+)\s+cpu-migrations', content).group(1).replace(',', '')) if re.search(r'([\d,]+)\s+cpu-migrations', content) else None)
            
    for sub_dir in sub_dirs_O3:
        with open(os.path.join(root_dir,sub_dir,f"{n}.txt"), 'r') as file:
            content = file.read()
            
            instructions_counts_o3[i].append(int(re.search(r'([\d,]+)\s+instructions', content).group(1).replace(',', ''))/flops if re.search(r'([\d,]+)\s+instructions', content) else None)
            page_faults_counts_o3[i].append(int(re.search(r'([\d,]+)\s+page-faults', content).group(1).replace(',', ''))/kflops if re.search(r'([\d,]+)\s+page-faults', content) else None)
            cpu_migrations_counts_o3[i].append(int(re.search(r'([\d,]+)\s+cpu-migrations', content).group(1).replace(',', '')) if re.search(r'([\d,]+)\s+cpu-migrations', content) else None)
            





instructions_counts_o0 = np.mean(instructions_counts_o0, axis=1)
page_faults_counts_o0 = np.mean(page_faults_counts_o0, axis=1)
cpu_migrations_counts_o0 = np.mean(cpu_migrations_counts_o0, axis=1)



instructions_counts_o3 = np.mean(instructions_counts_o3, axis=1)
page_faults_counts_o3 = np.mean(page_faults_counts_o3, axis=1)
cpu_migrations_counts_o3 = np.mean(cpu_migrations_counts_o3, axis=1)


n_values = np.arange(500, 10001, 500)

# 绘制L1指令缓存未命中率
plt.plot(n_values, instructions_counts_o0, marker='o', linestyle='-', color='green', label='Instructions Counts: O0', markersize=4, linewidth=1)

for i, txt in enumerate(instructions_counts_o0):
    plt.text(n_values[i], instructions_counts_o0[i] + 0.05 * max(instructions_counts_o0), f'{txt:.2f}', fontsize=8, ha='center', rotation=90)

#plot o3 related metrics
# 绘制L1指令缓存未命中率
plt.plot(n_values, instructions_counts_o3, marker='o', linestyle='--', color='green', label='Instructions Counts: O3', markersize=4, linewidth=1)

for i, txt in enumerate(instructions_counts_o3):
    plt.text(n_values[i], instructions_counts_o3[i] + 0.05 * max(instructions_counts_o3), f'{txt:.2f}', fontsize=8, ha='center', rotation=90)



# 设置坐标轴标签和标题
plt.xlabel('N')
plt.ylabel('Counts / flops')
plt.title('')

# 添加网格线
plt.grid(True, linestyle='--', alpha=0.7)

# 显示图例
plt.legend()

# 显示图形
plt.savefig(os.path.join(root_dir,f"instructions_counts.png"))
# name = r"$\bar{x}$"