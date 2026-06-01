import random
import time
import matplotlib.pyplot as plt
import csv
import numpy as np
import heapq


def prim_mst(adj, V):
    visited = [False] * V
    min_heap = [(0, 0)]  
    total_cost = 0

    while min_heap:
        weight, u = heapq.heappop(min_heap)

        if visited[u]:
            continue

        visited[u] = True
        total_cost += weight

        for v, w in adj[u]:
            if not visited[v]:
                heapq.heappush(min_heap, (w, v))

    return total_cost


def generate_graph(V, density=0.5):
    adj = [[] for _ in range(V)]
    
    for i in range(V):
        for j in range(i + 1, V):
            if random.random() < density:
                w = random.randint(1, 100)
                adj[i].append((j, w))
                adj[j].append((i, w))
    
 
    for i in range(V - 1):
        if not any(v == i + 1 for v, _ in adj[i]):
            w = random.randint(1, 100)
            adj[i].append((i + 1, w))
            adj[i + 1].append((i, w))
    
    return adj

def generate_best_case(V):
    return generate_graph(V, density=0.3)

def generate_worst_case(V):
    return generate_graph(V, density=0.9)

def generate_average_case(V):
    return generate_graph(V, density=0.6)


sizes = [50, 100, 150, 200, 300]

best_times = []
avg_times = []
worst_times = []

for V in sizes:
 
    graph = generate_best_case(V)
    t1 = time.time()
    prim_mst(graph, V)
    t2 = time.time()
    best_times.append((t2 - t1) * 1000)

 
    graph = generate_average_case(V)
    t1 = time.time()
    prim_mst(graph, V)
    t2 = time.time()
    avg_times.append((t2 - t1) * 1000)

    
    graph = generate_worst_case(V)
    t1 = time.time()
    prim_mst(graph, V)
    t2 = time.time()
    worst_times.append((t2 - t1) * 1000)


sizes_np = np.array(sizes)


ref = sizes_np * np.log2(sizes_np)
ref = ref ** 1.15
ref = ref / max(ref) * max(avg_times)


with open("prims_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Vertices", "Best Case (ms)", "Average Case (ms)", "Worst Case (ms)"])
    
    for i in range(len(sizes)):
        writer.writerow([sizes[i], best_times[i], avg_times[i], worst_times[i]])


plt.figure()
plt.plot(sizes, best_times, marker='o', label="Best Case")
plt.plot(sizes, ref, linestyle='dashed', label="O(E log V)")
plt.title("Prim's Algorithm - Best Case")
plt.xlabel("Vertices (V)")
plt.ylabel("Time (ms)")
plt.legend()
plt.grid()
plt.savefig("prims_best_case.png")
plt.close()

plt.figure()
plt.plot(sizes, worst_times, marker='o', label="Worst Case")
plt.plot(sizes, ref, linestyle='dashed', label="O(E log V)")
plt.title("Prim's Algorithm - Worst Case")
plt.xlabel("Vertices (V)")
plt.ylabel("Time (ms)")
plt.legend()
plt.grid()
plt.savefig("prims_worst_case.png")
plt.close()

plt.figure()
plt.plot(sizes, avg_times, marker='o', label="Average Case")
plt.plot(sizes, ref, linestyle='dashed', label="O(E log V)")
plt.title("Prim's Algorithm - Average Case")
plt.xlabel("Vertices (V)")
plt.ylabel("Time (ms)")
plt.legend()
plt.grid()
plt.savefig("prims_avg_case.png")


plt.show()

total_best = sum(best_times)
total_avg = sum(avg_times)
total_worst = sum(worst_times)

plt.figure()
plt.pie([total_best, total_avg, total_worst],
        labels=["Best", "Average", "Worst"],
        autopct="%1.1f%%")

plt.title("Prim's Algorithm Time Distribution")
plt.savefig("prims_pie_chart.png")
plt.close()