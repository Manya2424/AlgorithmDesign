import time
import csv
from pathlib import Path
import matplotlib.pyplot as plt

# ---------------------------
# N-ARY SEARCH FUNCTION
# ---------------------------
def n_ary_search(arr, key, degree):
    low = 0
    high = len(arr) - 1

    while low <= high:
        step = (high - low) // degree

        if step == 0:
            break

        points = []
        for i in range(1, degree):
            points.append(low + i * step)

        found_part = False

        for p in points:
            if arr[p] == key:
                return p
            elif key < arr[p]:
                high = p - 1
                found_part = True
                break

        if not found_part:
            low = points[-1] + 1

    return -1


# ---------------------------
# MAIN ANALYSIS
# ---------------------------
size = 100000
arr = list(range(size))
key = size - 1

degrees = [2, 3, 4, 5, 6, 8, 10]
times = []

for d in degrees:
    start = time.time()
    n_ary_search(arr, key, d)
    end = time.time()
    times.append(end - start)

# ---------------------------
# SAVE CSV
# ---------------------------
base_dir = Path(__file__).resolve().parent
csv_path = base_dir / "n_ary_results.csv"

with open(csv_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Degree", "Time"])
    writer.writerows(zip(degrees, times))

# ---------------------------
# GRAPH
# ---------------------------
plt.figure()
plt.plot(degrees, times, marker="o")
plt.xlabel("Degree (N)")
plt.ylabel("Execution Time (seconds)")
plt.title("N-ary Search Runtime Analysis")
plt.grid(True)
plt.show()