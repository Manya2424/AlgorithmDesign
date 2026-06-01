import random
import time
import csv
import matplotlib.pyplot as plt

# Binary Search Function
def binary_search(arr, key):
    low = 0
    high = len(arr) - 1
    iterations = 0

    while low <= high:
        iterations += 1
        mid = (low + high) // 2

        if arr[mid] == key:
            return mid, iterations
        elif arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1

    return -1, iterations


# Input sizes (1000 to 100000 with step 5000)
array_sizes = range(1000, 100001, 5000)
runs = 5  # multiple runs to reduce system noise

results = []

for size in array_sizes:
    total_time = 0
    total_iterations = 0

    for _ in range(runs):
        # Generate random array
        arr = [random.randint(0, 100000) for _ in range(size)]

        # Sort array (sorting time not included)
        arr.sort()

        # Select random key from array (average case)
        key = random.choice(arr)

        start_time = time.time()
        _, iterations = binary_search(arr, key)
        end_time = time.time()

        total_time += (end_time - start_time)
        total_iterations += iterations

    avg_time = total_time / runs
    avg_iterations = total_iterations / runs

    results.append([size, avg_time, avg_iterations])

# Save results to CSV
with open("binary_search_analysis.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Array Size", "Average Execution Time (seconds)", "Average Iterations"])
    writer.writerows(results)

# Data for graph
sizes = [row[0] for row in results]
times = [row[1] for row in results]

# Plot graph
plt.plot(sizes, times, marker='o')
plt.xlabel("Array Size")
plt.ylabel("Average Execution Time (seconds)")
plt.title("Binary Search Runtime Analysis (Average Case)")
plt.grid(True)
plt.show()