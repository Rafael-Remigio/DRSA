import matplotlib.pyplot as plt
import sys
import time
import subprocess
import numpy as np

# args
if len(sys.argv) < 4:
    print("Usage: python3 randgen.py <confusion_string_1> <confusion_string_2> ... <num_iterations> <n>")
    sys.exit(1)

# retrieving confusion strings
confusion_strings = sys.argv[1:-2]
num_iterations_values = [int(arg) for arg in sys.argv[-2].split()]
n = int(sys.argv[-1])

print(confusion_strings)

def setup_random_generator(confusion_string, num_iterations):
    start_time = time.time()

    print(f"conf: {confusion_string},  i: {num_iterations}")
    subprocess.run(["python3", "./rsagen.py", "-p", "pass", "-c", confusion_string, "-i", str(num_iterations)])

    end_time = time.time()
    setup_time = end_time - start_time
    print(f"  Time: {setup_time:.5f} s")

    return setup_time


fig, ax = plt.subplots(figsize=(10, 6))

# create graph o sc
for i, num_iterations in enumerate(num_iterations_values):
    setup_times_all_confusions = []
    for conf in confusion_strings:
        setup_time_for_confusion = setup_random_generator(conf, num_iterations)
        setup_times_all_confusions.append(setup_time_for_confusion)

    # average
    mean_times = [np.mean(setup_times_all_confusions[i:i+n]) for i in range(0, len(setup_times_all_confusions), n)]

  
    # Print to the console
    for j, mean_time, conf in zip(range(len(mean_times)), mean_times, confusion_strings):
        idx = j * n + 1
        
        print(f"For Confusion String Length {len(confusion_strings[idx])}, {num_iterations} Iterations:")
        print(f"  Mean Time: {mean_time:.5f} s")


    # Plotar the average
    ax.plot(range(1, len(mean_times)*n + 1, n), mean_times, label=f'{num_iterations} Iterations', marker='o')

# title and label
ax.set_xlabel('Confusion String Length')
ax.set_ylabel('Mean Setup Time (s)')
ax.set_xticks(range(1, len(mean_times)*n + 1, n)) 
ax.xaxis.get_major_formatter().set_scientific(False)
ax.xaxis.get_major_formatter().set_useOffset(False)
ax.set_title('Mean Setup Time vs. Confusion String Length for Different Iterations')


ax.legend()

# save the figure
plt.savefig('results.png')
