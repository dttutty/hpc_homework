import matplotlib.pyplot as plt
import numpy as np



# Data
categories = ['N=100, n=1', 'N=100, n=10000', 'N=1000, n=1000', 'N=10000, n=1']

real_time_means = [1.6, 338.2, 3273.1, 1138.6]
real_time_stds = [1.8, 4.9, 5.2, 7.4]

user_time_means = [0.9, 337.2, 3268.1, 1006.8]
user_time_stds = [0.3, 5.8, 5.9, 13.9]

sys_time_means = [0.1, 0.8, 4.4, 131.6]
sys_time_stds = [0.3, 1.6, 2.8, 15.6]

x = np.arange(len(categories))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 6))

# Plot bars
rects1 = ax.bar(x - width, real_time_means, width, label='Real time', yerr=real_time_stds, capsize=5)
rects2 = ax.bar(x, user_time_means, width, label='User time', yerr=user_time_stds, capsize=5)
rects3 = ax.bar(x + width, sys_time_means, width, label='Sys time', yerr=sys_time_stds, capsize=5)

# Add text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Configurations')
ax.set_ylabel('Execution time (ms)')
ax.set_title('')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()

# Function to add labels on the bars
def autolabel(rects, means, stds):
    """Attach a text label above each bar in *rects*, displaying mean and std."""
    for rect, mean, std in zip(rects, means, stds):
        height = rect.get_height()
        ax.annotate(f'{mean:.1f}\n±{std:.1f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

# Apply the labels
autolabel(rects1, real_time_means, real_time_stds)
autolabel(rects2, user_time_means, user_time_stds)
autolabel(rects3, sys_time_means, sys_time_stds)

fig.tight_layout()

plt.savefig('plot.png')
