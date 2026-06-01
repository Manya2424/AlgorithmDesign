import random
import time
import csv
import matplotlib.pyplot as plt

# -------- Min-Max using IF --------
def min_max_if(arr):
    min_val = arr[0]
    max_val = arr[0]
    iterations = 0

    for i in range(1, len(arr)):
        iterations += 1
        if arr[i] < min_val:
            min_val = arr[i]
        if arr[i] > max_val:
            max_val = arr[i]

    return iterations


# -------- Min-Max using IF-ELSE --------
def min_max_if_else(arr):
    min_val = arr[0]
    max_val = arr[0]
    iterations = 0

    for i in range(1, len(arr)):
        iterations += 1
        if arr[i] < min_val:
            min_val = arr[i]
        else:
            if arr[i] > max_val:
                max_val = arr[i]

    return iterations


array_sizes = range(1000, 100001, 5000)
runs = 5

if_results = []
if_else_results = []

# -------- Experiments --------
for size in array_sizes:
    total_time_if = 0
    total_time_if_else = 0

    for _ in range(runs):
        arr = [random.randint(0, 100000) for _ in range(size)]

        # IF
        start = time.time()
        min_max_if(arr)
        end = time.time()
        total_time_if += (end - start)

        # IF-ELSE
        start = time.time()
        min_max_if_else(arr)
        end = time.time()
        total_time_if_else += (end - start)

    avg_if = total_time_if / runs
    avg_if_else = total_time_if_else / runs

    if_results.append([size, avg_if])
    if_else_results.append([size, avg_if_else])

# -------- Save IF Results to CSV --------
with open("min_max_if.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Array Size", "Average Time"])
    writer.writerows(if_results)

# -------- Save IF-ELSE Results to CSV --------
with open("min_max_if_else.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Array Size", "Average Time"])
    writer.writerows(if_else_results)


# -------- Plot Graph: IF --------
sizes_if = [x[0] for x in if_results]
times_if = [x[1] for x in if_results]

plt.figure()
plt.plot(sizes_if, times_if, marker='o')
plt.xlabel("Array Size")
plt.ylabel("Average Time")
plt.title("Min-Max Algorithm (Using IF)")
plt.grid(True)
plt.show()


# -------- Plot Graph: IF-ELSE --------
sizes_else = [x[0] for x in if_else_results]
times_else = [x[1] for x in if_else_results]

plt.figure()
plt.plot(sizes_else, times_else, marker='o')
plt.xlabel("Array Size")
plt.ylabel("Average Time")
plt.title("Min-Max Algorithm (Using IF-ELSE)")
plt.grid(True)
plt.show()