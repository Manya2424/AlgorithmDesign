import time
import random
import csv
from pathlib import Path
import matplotlib.pyplot as plt


def randomized_quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return randomized_quick_sort(left) + middle + right


sizes = [1000, 4000, 5000, 7000, 8000, 10000, 15000, 20000, 30000, 40000,50000]
random_times = []

for size in sizes:
    arr = random.sample(range(size), size)

    start = time.time()
    randomized_quick_sort(arr)
    end = time.time()

    random_times.append(end - start)

# ---------------------------
# SAVE CSV
# ---------------------------
base_dir = Path(__file__).resolve().parent
csv_path = base_dir / "randomized_quick_sort_results.csv"

with open(csv_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Input Size", "Time"])
    writer.writerows(zip(sizes, random_times))

# ---------------------------
# GRAPH
# ---------------------------
plt.figure()
plt.plot(sizes, random_times, marker="o")
plt.xlabel("Input Size")
plt.ylabel("Execution Time (seconds)")
plt.title("Randomized Quick Sort Runtime Analysis")
plt.grid(True)
plt.show()