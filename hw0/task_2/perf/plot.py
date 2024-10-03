import matplotlib.pyplot as plt
import numpy as np


# Data
categories = ['N=100, n=1', 'N=100, n=10000', 'N=1000, n=1000', 'N=10000, n=1']

# time elapsed
time_elapsed_means = [0.9090013, 398.4850314, 3912.7837895, 1154.6938224]
time_elapsed_stds = [0.1550954, 8.0070536, 13.9054069, 15.5785001]

# user
user_means = [0.9106000, 394.1294000, 3903.2827000, 999.5430000]
user_stds = [0.3217832, 5.0185379, 14.0676060, 30.5616751]

# sys
sys_means = [0.0565000, 0.3978000, 3.5968000, 154.2028000]
sys_stds = [0.1695000, 1.1934000, 4.1711241, 28.5064551]


x = np.arange(len(categories))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 6))

# Plot bars
rects1 = ax.bar(x - width, time_elapsed_means, width, label='time elapsed', yerr=time_elapsed_stds, capsize=5)
rects2 = ax.bar(x, user_means, width, label='user', yerr=user_stds, capsize=5)
rects3 = ax.bar(x + width, sys_means, width, label='sys', yerr=sys_stds, capsize=5)

# Add text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Configurations')
ax.set_ylabel('Execution time (ms)')
ax.set_title('Execution time comparison')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()

# Function to add labels on the bars
def autolabel(rects, means, stds):
    """Attach a text label above each bar in *rects*, displaying mean and std."""
    for rect, mean, std in zip(rects, means, stds):
        height = rect.get_height()
        ax.annotate(f'{mean:.3f}\n±{std:.3f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

# Apply the labels
autolabel(rects1, time_elapsed_means, time_elapsed_stds)
autolabel(rects2, user_means, user_stds)
autolabel(rects3, sys_means, sys_stds)

fig.tight_layout()

plt.savefig('hw0_code/task_2/perf/plot.png')