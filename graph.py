# title and label
import matplotlib.pyplot as plt

# Sample data (replace this with your actual data)
lengths = [1, 2, 3]  # Three different lengths
iterations = list(range(1, 11))  # 1 to 10 iterations
times = [
    [1.23805, 1.84412, 1.44104, 1.69050, 1.26559, 1.70383, 1.55429, 1.31104, 1.25957, 1.59359],  # Time data for length 10
    [1.82990, 1.93954, 2.81393, 2.82560, 2.77405, 3.30724, 3.49871, 3.41593, 4.20521, 4.27661],  # Time data for length 20
    [128.68336, 198.37125 , 257.25545, 438.67631, 597.44884, 621.93270, 663.06380, 788.25374, 851.78697, 933.38498]  # Time data for length 30
]

# Plotting the data
plt.figure()

for i, length in enumerate(lengths[:-1]):
    plt.plot(iterations, times[i], label=f'Confusion String Length {length}')



plt.xlabel('Number of Iterations')
plt.ylabel('Time to setup PRNG (seconds)')
plt.title('Time taken for iterations on different confusion string lengths')
plt.legend()
plt.grid(True)
plt.xticks(iterations)  # Set x-axis ticks to only the iteration values
plt.show()