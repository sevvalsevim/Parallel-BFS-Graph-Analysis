import matplotlib.pyplot as plt

# Your data
processors = [1, 2, 4]
times = [0.8098, 0.7521, 0.8034]

# Speedup calculation: T1 / Tn
t1 = times[0]
speedup = [t1 / tn for tn in times]

plt.figure(figsize=(10, 5))

# Execution Time Graph
plt.subplot(1, 2, 1)
plt.plot(processors, times, marker='o', color='teal', linewidth=2)
plt.title('Execution Time vs Processors')
plt.xlabel('Number of Processors')
plt.ylabel('Time (seconds)')
plt.xticks(processors)
plt.grid(True, linestyle='--')

# Speedup Graph
plt.subplot(1, 2, 2)
plt.plot(processors, speedup, marker='s', color='crimson', label='Actual Speedup')
plt.plot(processors, processors, color='gray', linestyle=':', label='Ideal Speedup')
plt.title('Speedup Analysis')
plt.xlabel('Number of Processors')
plt.ylabel('Speedup Ratio')
plt.legend()
plt.xticks(processors)
plt.grid(True, linestyle='--')

plt.tight_layout()
plt.savefig('performance_results.png')
plt.show()