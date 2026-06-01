import time
import random
import csv
from pathlib import Path
import matplotlib.pyplot as plt


def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + right


sizes = [1000, 5000, 7000, 8000, 10000, 20000, 40000]
quick_times = []

for size in sizes:
    arr = random.sample(range(size), size)

    start = time.time()
    quick_sort(arr)
    end = time.time()

    quick_times.append(end - start)

# ---------------------------
# SAVE CSV
# ---------------------------
base_dir = Path(__file__).resolve().parent
csv_path = base_dir / "quick_sort_results.csv"

with open(csv_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Input Size", "Time"])
    writer.writerows(zip(sizes, quick_times))

# ---------------------------
# GRAPH
# ---------------------------
plt.figure()
plt.plot(sizes, quick_times, marker="o")
plt.xlabel("Input Size")
plt.ylabel("Execution Time (seconds)")
plt.title("Quick Sort Runtime Analysis")
plt.grid(True)
plt.show()