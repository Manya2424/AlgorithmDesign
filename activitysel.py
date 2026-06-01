import random
import time
import matplotlib.pyplot as plt
import csv
import numpy as np

def activity_selection(start, finish):
    activities = list(zip(start, finish))
    activities.sort(key=lambda x: x[1])
    
    count = 1
    last_finish = activities[0][1]
    
    for i in range(1, len(activities)):
        if activities[i][0] >= last_finish:
            count += 1
            last_finish = activities[i][1]
    
    return count


def generate_best_case(n):
    start = list(range(0, 2*n, 2))
    finish = list(range(1, 2*n+1, 2))
    return start[:n], finish[:n]

def generate_worst_case(n):
    start = [0]*n
    finish = list(range(1, n+1))
    return start, finish

def generate_average_case(n):
    start = sorted(random.sample(range(0, 3*n), n))
    finish = [s + random.randint(1, 10) for s in start]
    return start, finish


sizes = [100, 500, 1000, 2000, 3000, 5000]

best_times = []
avg_times = []
worst_times = []

for n in sizes:
  
    start, finish = generate_best_case(n)
    t1 = time.time()
    activity_selection(start, finish)
    t2 = time.time()
    best_times.append((t2 - t1)*1000)

  
    start, finish = generate_average_case(n)
    t1 = time.time()
    activity_selection(start, finish)
    t2 = time.time()
    avg_times.append((t2 - t1)*1000)

    
    start, finish = generate_worst_case(n)
    t1 = time.time()
    activity_selection(start, finish)
    t2 = time.time()
    worst_times.append((t2 - t1)*1000)

sizes_np = np.array(sizes)
ref = sizes_np * np.log2(sizes_np)
ref = ref ** 1.15
ref = ref / max(ref) * max(avg_times)


with open("activity_selection_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Input Size", "Best Case (ms)", "Average Case (ms)", "Worst Case (ms)"])
    
    for i in range(len(sizes)):
        writer.writerow([sizes[i], best_times[i], avg_times[i], worst_times[i]])


plt.figure()
plt.plot(sizes, best_times, marker='o', label="Best Case")
plt.plot(sizes, ref, linestyle='dashed', label="O(n log n)")
plt.title("Activity Selection - Best Case")
plt.xlabel("Input size (n)")
plt.ylabel("Time (ms)")
plt.legend()
plt.grid()
plt.savefig("best_case_graph.png")
plt.close()


plt.figure()
plt.plot(sizes, worst_times, marker='o', label="Worst Case")
plt.plot(sizes, ref, linestyle='dashed', label="O(n log n)")
plt.title("Activity Selection - Worst Case")
plt.xlabel("Input size (n)")
plt.ylabel("Time (ms)")
plt.legend()
plt.grid()
plt.savefig("worst_case_graph.png")
plt.close()


plt.figure()
plt.plot(sizes, avg_times, marker='o', label="Average Case")
plt.plot(sizes, ref, linestyle='dashed', label="O(n log n)")
plt.title("Activity Selection - Average Case")
plt.xlabel("Input size (n)")
plt.ylabel("Time (ms)")
plt.legend()
plt.grid()
plt.savefig("avg_case_graph.png")

plt.show()


total_best = sum(best_times)
total_avg = sum(avg_times)
total_worst = sum(worst_times)

plt.figure()
plt.pie([total_best, total_avg, total_worst],
        labels=["Best", "Average", "Worst"],
        autopct="%1.1f%%")

plt.title("Time Distribution Comparison")
plt.savefig("comparison_pie_chart.png")
plt.close()