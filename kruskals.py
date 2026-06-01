import random
import time
import matplotlib.pyplot as plt
import csv
import numpy as np


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX != rootY:
            if self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            elif self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1
            return True
        return False


def kruskal(V, edges):
    edges.sort(key=lambda x: x[2])  
    dsu = DSU(V)
    total_cost = 0

    for u, v, w in edges:
        if dsu.union(u, v):
            total_cost += w

    return total_cost

def generate_graph(V, density=0.5):
    edges = []

    for i in range(V):
        for j in range(i + 1, V):
            if random.random() < density:
                w = random.randint(1, 100)
                edges.append((i, j, w))

   
    for i in range(V - 1):
        edges.append((i, i + 1, random.randint(1, 100)))

    return edges

def generate_best_case(V):
    return generate_graph(V, density=0.3)

def generate_average_case(V):
    return generate_graph(V, density=0.6)

def generate_worst_case(V):
    return generate_graph(V, density=0.9)


sizes = [50, 100, 150, 200, 300]

best_times = []
avg_times = []
worst_times = []

for V in sizes:

    edges = generate_best_case(V)
    t1 = time.time()
    kruskal(V, edges)
    t2 = time.time()
    best_times.append((t2 - t1) * 1000)


    edges = generate_average_case(V)
    t1 = time.time()
    kruskal(V, edges)
    t2 = time.time()
    avg_times.append((t2 - t1) * 1000)

  
    edges = generate_worst_case(V)
    t1 = time.time()
    kruskal(V, edges)
    t2 = time.time()
    worst_times.append((t2 - t1) * 1000)

sizes_np = np.array(sizes)

ref = sizes_np * np.log2(sizes_np)
ref = ref ** 1.15
ref = ref / max(ref) * max(avg_times)

with open("kruskal_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Vertices", "Best Case (ms)", "Average Case (ms)", "Worst Case (ms)"])
    
    for i in range(len(sizes)):
        writer.writerow([sizes[i], best_times[i], avg_times[i], worst_times[i]])


plt.figure()
plt.plot(sizes, best_times, marker='o', label="Best Case")
plt.plot(sizes, ref, linestyle='dashed', label="O(E log V)")
plt.title("Kruskal's Algorithm - Best Case")
plt.xlabel("Vertices (V)")
plt.ylabel("Time (ms)")
plt.legend()
plt.grid()
plt.savefig("kruskal_best_case.png")
plt.close()


plt.figure()
plt.plot(sizes, worst_times, marker='o', label="Worst Case")
plt.plot(sizes, ref, linestyle='dashed', label="O(E log V)")
plt.title("Kruskal's Algorithm - Worst Case")
plt.xlabel("Vertices (V)")
plt.ylabel("Time (ms)")
plt.legend()
plt.grid()
plt.savefig("kruskal_worst_case.png")
plt.close()

plt.figure()
plt.plot(sizes, avg_times, marker='o', label="Average Case")
plt.plot(sizes, ref, linestyle='dashed', label="O(E log V)")
plt.title("Kruskal's Algorithm - Average Case")
plt.xlabel("Vertices (V)")
plt.ylabel("Time (ms)")
plt.legend()
plt.grid()
plt.savefig("kruskal_avg_case.png")


plt.show()


total_best = sum(best_times)
total_avg = sum(avg_times)
total_worst = sum(worst_times)

plt.figure()
plt.pie([total_best, total_avg, total_worst],
        labels=["Best", "Average", "Worst"],
        autopct="%1.1f%%")

plt.title("Kruskal's Algorithm Time Distribution")
plt.savefig("kruskal_pie_chart.png")
plt.close()