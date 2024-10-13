import matplotlib.pyplot as plt


threads = []
mops = []
no_parallel_mops = 0

class_type = 'A'
file_path = class_type + ".log"

plt.figure(figsize=(10, 6))

with open(file_path, 'r') as file:
    lines = file.readlines()
    for line in lines[1:]:
        parts = line.split()
        if parts[0] == 'conf_rolled_0':
            no_parallel_mops = float(parts[3])
        else:
            threads.append(int(parts[1]))
            mops.append(float(parts[3]))
            
# sort the      
plt.figure(figsize=(10, 6))
sorted_data = sorted(zip(threads, mops))
threads_sorted, mops_sorted = zip(*sorted_data)

plt.plot(threads_sorted, mops_sorted, marker='o', linestyle='-', color='b')

plt.axhline(y=no_parallel_mops, color='r', linestyle='--')
plt.text(48, no_parallel_mops, 'No parallel', color='r', va='center')

plt.title('Mop/s vs Threads')
plt.xlabel('Threads')
plt.ylabel('Mop/s')

plt.grid(True)
plt.savefig(class_type + ".png")
