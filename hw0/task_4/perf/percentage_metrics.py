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
    for sub_dir in sub_dirs_O0:
        with open(os.path.join(root_dir,sub_dir,f"{n}.txt"), 'r') as file:
            content = file.read()
            flops = 2 * n**2

            icache_hit_percentages_o0[i].append(float(re.search(r'L1-icache-load-misses\s+#\s+([\d\.]+)% of all L1-icache hits', content).group(1)) if re.search(r'L1-icache-load-misses\s+#\s+([\d\.]+)% of all L1-icache hits', content) else None)
            cache_ref_percentages_o0[i].append(float(re.search(r'cache-misses\s+#\s+([\d\.]+)\s*% of all cache refs', content).group(1)) if re.search(r'cache-misses\s+#\s+([\d\.]+)\s*% of all cache refs', content) else None)
            dcache_hit_percentages_o0[i].append(float(re.search(r'L1-dcache-load-misses\s+#\s+([\d\.]+)% of all L1-dcache hits', content).group(1)) if re.search(r'L1-dcache-load-misses\s+#\s+([\d\.]+)% of all L1-dcache hits', content) else None)
            branch_miss_percentages_o0[i].append(float(re.search(r'branch-misses\s+#\s+([\d\.]+)% of all branches', content).group(1)) if re.search(r'branch-misses\s+#\s+([\d\.]+)% of all branches', content) else None)
            instructions_counts_o0[i].append(int(re.search(r'([\d,]+)\s+instructions', content).group(1).replace(',', '')) if re.search(r'([\d,]+)\s+instructions', content) else None)
            page_faults_counts_o0[i].append(int(re.search(r'([\d,]+)\s+page-faults', content).group(1).replace(',', '')) if re.search(r'([\d,]+)\s+page-faults', content) else None)
            cpu_migrations_counts_o0[i].append(int(re.search(r'([\d,]+)\s+cpu-migrations', content).group(1).replace(',', '')) if re.search(r'([\d,]+)\s+cpu-migrations', content) else None)
            
    for sub_dir in sub_dirs_O3:
        with open(os.path.join(root_dir,sub_dir,f"{n}.txt"), 'r') as file:
            content = file.read()
            flops = 2 * n**2
            
            icache_hit_percentages_o3[i].append(float(re.search(r'L1-icache-load-misses\s+#\s+([\d\.]+)% of all L1-icache hits', content).group(1)) if re.search(r'L1-icache-load-misses\s+#\s+([\d\.]+)% of all L1-icache hits', content) else None)
            cache_ref_percentages_o3[i].append(float(re.search(r'cache-misses\s+#\s+([\d\.]+)\s*% of all cache refs', content).group(1)) if re.search(r'cache-misses\s+#\s+([\d\.]+)\s*% of all cache refs', content) else None)
            dcache_hit_percentages_o3[i].append(float(re.search(r'L1-dcache-load-misses\s+#\s+([\d\.]+)% of all L1-dcache hits', content).group(1)) if re.search(r'L1-dcache-load-misses\s+#\s+([\d\.]+)% of all L1-dcache hits', content) else None)
            branch_miss_percentages_o3[i].append(float(re.search(r'branch-misses\s+#\s+([\d\.]+)% of all branches', content).group(1)) if re.search(r'branch-misses\s+#\s+([\d\.]+)% of all branches', content) else None)
            instructions_counts_o3[i].append(int(re.search(r'([\d,]+)\s+instructions', content).group(1).replace(',', '')) if re.search(r'([\d,]+)\s+instructions', content) else None)
            page_faults_counts_o3[i].append(int(re.search(r'([\d,]+)\s+page-faults', content).group(1).replace(',', '')) if re.search(r'([\d,]+)\s+page-faults', content) else None)
            cpu_migrations_counts_o3[i].append(int(re.search(r'([\d,]+)\s+cpu-migrations', content).group(1).replace(',', '')) if re.search(r'([\d,]+)\s+cpu-migrations', content) else None)
            





icache_hit_percentages_o0 = np.mean(icache_hit_percentages_o0, axis=1)
cache_ref_percentages_o0 = np.mean(cache_ref_percentages_o0, axis=1)
dcache_hit_percentages_o0 = np.mean(dcache_hit_percentages_o0, axis=1)
branch_miss_percentages_o0 = np.mean(branch_miss_percentages_o0, axis=1)

# instructions_counts_o0 = np.mean(instructions_counts_o0, axis=1)
# page_faults_counts_o0 = np.mean(page_faults_counts_o0, axis=1)
# cpu_migrations_counts_o0 = np.mean(cpu_migrations_counts_o0, axis=1)


icache_hit_percentages_o3 = np.mean(icache_hit_percentages_o3, axis=1)
cache_ref_percentages_o3 = np.mean(cache_ref_percentages_o3, axis=1)
dcache_hit_percentages_o3 = np.mean(dcache_hit_percentages_o3, axis=1)
branch_miss_percentages_o3 = np.mean(branch_miss_percentages_o3, axis=1)

# instructions_counts_o3 = np.mean(instructions_counts_o3, axis=1)
# page_faults_counts_o3 = np.mean(page_faults_counts_o3, axis=1)
# cpu_migrations_counts_o3 = np.mean(cpu_migrations_counts_o3, axis=1)


n_values = np.arange(500, 10001, 500)

plt.figure(figsize=(7, 7)) 
# 绘制L1指令缓存未命中率
plt.plot(n_values, icache_hit_percentages_o0, marker='o', linestyle='-', color='green', label='L1-icache miss rate (%): O0', markersize=4, linewidth=1)
# 绘制缓存引用未命中率
plt.plot(n_values, cache_ref_percentages_o0, marker='o', linestyle='-', color='purple', label='Cache miss rate (%): O0', markersize=4, linewidth=1)
# 绘制L1数据缓存未命中率
plt.plot(n_values, dcache_hit_percentages_o0, marker='o', linestyle='-', color='orange', label='L1-dcache miss rate (%): O0', markersize=4, linewidth=1)
# 绘制分支未命中百分比
plt.plot(n_values, branch_miss_percentages_o0, marker='o', linestyle='-', color='magenta', label='Branch miss rate (%): O0', markersize=4, linewidth=1)

#plot o3 related metrics
# 绘制L1指令缓存未命中率
plt.plot(n_values, icache_hit_percentages_o3, marker='o', linestyle='--', color='green', label='L1-icache miss rate (%): O3', markersize=4, linewidth=1)
# 绘制缓存引用未命中率
plt.plot(n_values, cache_ref_percentages_o3, marker='o', linestyle='--', color='purple', label='Cache miss rate (%): O3', markersize=4, linewidth=1)
# 绘制L1数据缓存未命中率
plt.plot(n_values, dcache_hit_percentages_o3, marker='o', linestyle='--', color='orange', label='L1-dcache miss rate (%): O3', markersize=4, linewidth=1)
# 绘制分支未命中百分比
plt.plot(n_values, branch_miss_percentages_o3, marker='o', linestyle='--', color='magenta', label='Branch miss rate (%): O3', markersize=4, linewidth=1)


# 设置坐标轴标签和标题
plt.xlabel('N')
plt.ylabel('percentage(%)')
plt.title('')

# 添加网格线
plt.grid(True, linestyle='--', alpha=0.7)

# 显示图例
plt.legend()

# 显示图形
plt.savefig(os.path.join(root_dir,f"percentage_metrics.png"))
# name = r"$\bar{x}$"