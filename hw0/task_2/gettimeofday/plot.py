import matplotlib.pyplot as plt
import numpy as np

# Data
categories = ['N=100, n=1', 'N=100, n=10000', 'N=1000, n=1000', 'N=10000, n=1']
matrix_vector_means = [0.0605585, 392.7667616, 3895.9326031, 326.9620180]
matrix_vector_stds = [0.0165303, 5.0062123, 16.7790822, 2.4586872]
main_means = [0.2638577, 392.9192068, 3908.1603289, 1121.0340977]
main_stds = [0.0586828, 5.0025366, 16.9117782, 3.5908434]

x = np.arange(len(categories))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 6))

# Plot bars
rects1 = ax.bar(x - width/2, matrix_vector_means, width, label='Matrix_vector_mult()', yerr=matrix_vector_stds, capsize=5)
rects2 = ax.bar(x + width/2, main_means, width, label='main()', yerr=main_stds, capsize=5)

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
autolabel(rects1, matrix_vector_means, matrix_vector_stds)
autolabel(rects2, main_means, main_stds)

fig.tight_layout()

plt.savefig('hw0_code/task_2/gettimeofday/plot.png')