import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import networkx as nx

INF = float('inf')


def generate_graph(n, density='medium', seed=None):
    if seed is not None:
        random.seed(seed)

    matrix = [[INF]*n for _ in range(n)]

    for i in range(n):
        matrix[i][i] = 0

    max_edges = n*(n-1)

    if density == 'sparse':
        edges = int(1.5 * n)
    elif density == 'medium':
        edges = int(0.3 * max_edges)
    else:
        edges = int(0.7 * max_edges)

    count = 0
    while count < edges:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and matrix[u][v] == INF:
            matrix[u][v] = random.randint(1, 20)
            count += 1

    return matrix, edges


def floyd_warshall(dist):
    n = len(dist)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

def visualize_graph(matrix, title="Graph"):
    G = nx.DiGraph()

    n = len(matrix)

    for i in range(n):
        for j in range(n):
            if matrix[i][j] != INF and i != j:
                G.add_edge(i, j, weight=matrix[i][j])

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(6, 5))

    nx.draw(G, pos, with_labels=True,
            node_color='lightblue',
            node_size=600,
            edge_color='gray')

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title(title)
    plt.savefig("outputs/floyd_graph.png", dpi=150)
    plt.show()


def run_experiment(n, density, seed, visualize=False, runs=3):
    matrix, edges = generate_graph(n, density, seed)

    if visualize:
        visualize_graph(matrix, title=f"{density.capitalize()} Graph ({n} nodes)")

    times = []

    for _ in range(runs):
        dist = [row[:] for row in matrix]

        start = time.perf_counter()
        floyd_warshall(dist)
        end = time.perf_counter()

        times.append(end - start)

    return {
        "Nodes": n,
        "Edges": edges,
        "Density": density,
        "Avg_Time": sum(times) / len(times)
    }


def plot_results(df):
    os.makedirs("outputs", exist_ok=True)

    colors = {'sparse': 'blue', 'medium': 'orange', 'dense': 'green'}

    for density in ['sparse', 'medium', 'dense']:
        plt.figure(figsize=(6, 4))

        grp = df[df["Density"] == density]
        grp = grp.groupby("Nodes").mean(numeric_only=True).reset_index()

        plt.plot(grp["Nodes"], grp["Avg_Time"],
                 marker='o', linewidth=2,
                 color=colors[density],
                 label="Measured")

   
        nodes = np.array(grp["Nodes"])
        ref = nodes ** 3
        ref = ref / ref.max() * grp["Avg_Time"].max()

        plt.plot(nodes, ref, '--', color='black',
                 label='O(V³)')

        plt.title(f"{density.capitalize()} Graphs — Floyd Warshall")
        plt.xlabel("Nodes (V)")
        plt.ylabel("Execution Time (s)")
        plt.legend()
        plt.grid(True, alpha=0.3)

        save_path = f"outputs/floyd_{density}.png"
        plt.savefig(save_path, dpi=150)
        print(f"[Saved → {save_path}]")

        plt.show()





def main():
    print("\n═══════════════════════════════════════")
    print("   FLOYD-WARSHALL - PERFORMANCE ANALYSIS")
    print("═══════════════════════════════════════")

    results = []
    node_sizes = list(range(10, 110, 10))

    first = True

    for n in node_sizes:
        results.append(run_experiment(n, "sparse", n, visualize=first))
        first = False

        results.append(run_experiment(n, "medium", n+1))
        results.append(run_experiment(n, "dense", n+2))

    df = pd.DataFrame(results)

    os.makedirs("outputs", exist_ok=True)
    df.to_csv("outputs/floyd_results.csv", index=False)

    print("\nResults saved → outputs/floyd_results.csv")

    plot_results(df)

    print("\nDone.\n")

if __name__ == "__main__":
    main()