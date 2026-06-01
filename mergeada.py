import random
import time
import csv
import matplotlib.pyplot as plt
import sys


sys.setrecursionlimit(200000)

def merge(arr, left, mid, right):
    left_part = arr[left:mid+1]
    right_part = arr[mid+1:right+1]

    i = j = 0
    k = left

    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1

    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1

    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1



def merge_sort(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        merge(arr, left, mid, right)


sizes = list(range(50000, 100001, 10000)) 
iterations = 5   
results = []

for size in sizes:
    total_time = 0

    for _ in range(iterations):
        arr = [random.randint(1, 1000000) for _ in range(size)]

        start = time.perf_counter_ns()
        merge_sort(arr, 0, len(arr) - 1)
        end = time.perf_counter_ns()

        total_time += (end - start)

    avg_time = total_time / iterations
    results.append((size, avg_time))

    print(f"Size: {size}, Average Time: {avg_time:.2f} ns")



with open("merge_sort_results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Array Size", "Average Time (ns)"])
    writer.writerows(results)

print("\nCSV file generated successfully!")



sizes_plot = [r[0] for r in results]
times_plot = [r[1] for r in results]

plt.figure()
plt.plot(sizes_plot, times_plot)
plt.xlabel("Array Size")
plt.ylabel("Average Time (ns)")
plt.title("Merge Sort Time Complexity")
plt.show()