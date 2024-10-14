import matplotlib.pyplot as plt
import os
import sys
if len(sys.argv) != 2:
    print("Usage: python draw.py <class_type>")
    sys.exit(1)

class_type = sys.argv[1]

plt.figure(figsize=(10, 6))

def draw(class_type='A', conf='U1'):
    no_parallel_mops = 0
    threads = []
    mops_mean = []
    mops_std = []
    file_path = '/home/Students/sqp17/hpc_homework/hw1/NPB/result_log/' + conf + '/' + class_type + ".log"
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            parts = line.split()
            if parts[0] == f'conf_rolled_0':
                no_parallel_mops = float(parts[2])
            else:
                threads.append(int(parts[1]))
                mops_mean.append(float(parts[2]))
                mops_std.append(float(parts[3]))
                
    # sort data
    # change line type according to conf
    short_name_map = {'U1': 'unrolled_by2_1', 'U2': 'unrolled_by2_2', 'U3': 'unrolled_by2_3'}
    short_name = short_name_map.get(conf, 'unrolled_1')
    extra_text_map = {'U1': 'simd', 'U2': 'parallel for simd', 'U3': 'parallel for'}
    extra_text = extra_text_map.get(conf, 'simd')
    color_map = {'U1': 'b', 'U2': 'g', 'U3': 'magenta'}
    color = color_map.get(conf, 'b')
    color_for_std_map = {'U1': 'lightblue', 'U2': 'lightgreen', 'U3': 'lightpink'}
    color_for_std = color_for_std_map.get(conf, 'lightblue')
    sorted_data = sorted(zip(threads, mops_mean, mops_std))
    threads_sorted, mops_mean_sorted, mops_std_sorted = zip(*sorted_data)
    
    plt.errorbar(threads_sorted, mops_mean_sorted, yerr=mops_std_sorted, fmt='o', linestyle='-', label=f'conf_{short_name}: mostly {extra_text}', color=color, ecolor=color_for_std, elinewidth=1, capsize=5)
    for x, y in zip(threads_sorted, mops_mean_sorted):
        plt.plot([x, x], [0, y], linestyle='--', color='gray')
    
    max_index = mops_mean_sorted.index(max(mops_mean_sorted))
    max_threads = threads_sorted[max_index]
    max_mops = mops_mean_sorted[max_index]
    plt.text(max_threads, max_mops, f'{max_threads} threads, {max_mops:.0f} mop/s', color=color, va='bottom', ha='left', rotation=30)
    plt.scatter(max_threads, max_mops, facecolors='white', edgecolors=color, zorder=5)
    

    if conf == 'U3':
        plt.axhline(y=no_parallel_mops, color='gray', linestyle='--')
        plt.text(50, no_parallel_mops, 'No Parallel or SIMD', color='r', va='center')
        plt.text(-15.5, no_parallel_mops, f'{no_parallel_mops:.0f}', color='red', va='center', ha='left')
        
    plt.legend()

for conf in ['U3']:
    draw(class_type, conf)



# plt.title('Mop/s vs Threads')
plt.xlabel('Threads')
plt.ylabel('Mop/s')

plt.grid(True)
plt.savefig(class_type + ".png")
