import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict


def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive integer.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")


def build_graph():
    print("\n=== Multi-Stage Graph Input ===")
    stages = get_positive_int("Enter number of stages: ")

    stage_nodes = []
    node_to_stage = {}
    all_nodes = []
    current_node = 1

    for s in range(stages):
        count = get_positive_int(f"Enter number of nodes in stage {s + 1}: ")
        nodes = []
        for _ in range(count):
            nodes.append(current_node)
            node_to_stage[current_node] = s + 1
            all_nodes.append(current_node)
            current_node += 1
        stage_nodes.append(nodes)

    if len(stage_nodes[0]) != 1:
        print("\nNote: For a standard multi-stage shortest path problem, stage 1 should ideally have one source node.")
    if len(stage_nodes[-1]) != 1:
        print("Note: For a standard multi-stage shortest path problem, last stage should ideally have one destination node.")

    graph = defaultdict(list)
    edges = []

    print("\nNodes assigned automatically stage-wise:")
    for idx, nodes in enumerate(stage_nodes, start=1):
        print(f"Stage {idx}: {nodes}")

    print("\n=== Enter edges only between consecutive stages ===")
    for s in range(stages - 1):
        print(f"\nFrom Stage {s + 1} to Stage {s + 2}")
        for u in stage_nodes[s]:
            print(f"\nNode {u} can connect to nodes in Stage {s + 2}: {stage_nodes[s + 1]}")
            edge_count = get_positive_int(f"How many outgoing edges from node {u}? ")
            chosen_targets = set()
            for e in range(edge_count):
                while True:
                    try:
                        v = int(input(f"  Enter destination node for edge {e + 1} from {u}: "))
                        if v not in stage_nodes[s + 1]:
                            print("  Invalid destination. Choose a node from the next stage only.")
                            continue
                        if v in chosen_targets:
                            print("  Edge already entered for this node. Choose another destination.")
                            continue
                        w = int(input(f"  Enter weight for edge {u} -> {v}: "))
                        graph[u].append((v, w))
                        edges.append((u, v, w))
                        chosen_targets.add(v)
                        break
                    except ValueError:
                        print("  Invalid input. Please enter integers only.")

    return stages, stage_nodes, node_to_stage, all_nodes, graph, edges


def validate_graph(stage_nodes, graph):
    for s in range(len(stage_nodes) - 1):
        for u in stage_nodes[s]:
            if len(graph[u]) == 0:
                print(f"Warning: Node {u} has no outgoing edge to the next stage.")



def draw_graph(stage_nodes, edges, optimal_path=None, title="Multi-Stage Graph"):
    G = nx.DiGraph()
    pos = {}

    for s, nodes in enumerate(stage_nodes):
        total = len(nodes)
        for i, node in enumerate(nodes):
            pos[node] = (s, -i + (total - 1) / 2)
            G.add_node(node)

    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    plt.figure(figsize=(12, 7))

    default_edges = list(G.edges())
    path_edges = []
    if optimal_path and len(optimal_path) > 1:
        path_edges = list(zip(optimal_path[:-1], optimal_path[1:]))
        default_edges = [e for e in default_edges if e not in path_edges]

    nx.draw_networkx_nodes(G, pos, node_color="#a8d5ff", node_size=1600, edgecolors="black")
    nx.draw_networkx_labels(G, pos, font_size=11, font_weight="bold")
    nx.draw_networkx_edges(
        G, pos,
        edgelist=default_edges,
        edge_color="gray",
        width=1.8,
        arrows=True,
        arrowsize=20,
        connectionstyle="arc3,rad=0.03"
    )

    if path_edges:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=path_edges,
            edge_color="red",
            width=3.8,
            arrows=True,
            arrowsize=22,
            connectionstyle="arc3,rad=0.03"
        )

    edge_labels = {(u, v): w for u, v, w in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, label_pos=0.55)

    for s, nodes in enumerate(stage_nodes, start=1):
        x = s - 1
        y = max((-i + (len(nodes) - 1) / 2) for i in range(len(nodes))) + 0.8
        plt.text(x, y, f"Stage {s}", fontsize=12, fontweight="bold", ha="center", color="darkgreen")

    plt.title(title, fontsize=14, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.show()



def multi_stage_shortest_path(stage_nodes, graph):
    destination = stage_nodes[-1][0]
    all_nodes = [node for stage in stage_nodes for node in stage]
    INF = float('inf')

    cost = {node: INF for node in all_nodes}
    decision = {node: None for node in all_nodes}
    cost[destination] = 0

    print("\n=== Dynamic Programming Computation ===")
    print(f"Destination node is {destination}, so cost[{destination}] = 0\n")

    for s in range(len(stage_nodes) - 2, -1, -1):
        print(f"--- Processing Stage {s + 1} ---")
        for u in stage_nodes[s]:
            print(f"Processing Node {u}:")
            if not graph[u]:
                print(f"  No outgoing edges from node {u}; cost remains INF\n")
                continue

            min_cost = INF
            best_next = None
            for v, w in graph[u]:
                total_cost = w + cost[v]
                next_cost_str = "INF" if cost[v] == INF else str(cost[v])
                total_cost_str = "INF" if total_cost == INF else str(total_cost)
                print(f"  {u} -> {v} (edge cost {w} + cost[{v}] {next_cost_str} = {total_cost_str})")
                if total_cost < min_cost:
                    min_cost = total_cost
                    best_next = v

            cost[u] = min_cost
            decision[u] = best_next
            chosen = "INF" if min_cost == INF else str(min_cost)
            print(f"  Selected minimum = {chosen}")
            print(f"  decision[{u}] = {best_next}\n")

    source = stage_nodes[0][0]
    path = []
    if cost[source] != INF:
        current = source
        while current is not None:
            path.append(current)
            if current == destination:
                break
            current = decision[current]

    return source, destination, cost, decision, path



def print_results(source, destination, cost, path):
    print("=== Final Output ===")
    if cost[source] == float('inf'):
        print(f"No valid path exists from source node {source} to destination node {destination}.")
    else:
        print(f"Minimum cost from source {source} to destination {destination}: {cost[source]}")
        print("Optimal path:", " -> ".join(map(str, path)))



def main():
    stages, stage_nodes, node_to_stage, all_nodes, graph, edges = build_graph()
    validate_graph(stage_nodes, graph)

    print("\nDisplaying input graph...")
    draw_graph(stage_nodes, edges, title="Multi-Stage Graph Before Dynamic Programming")

    source, destination, cost, decision, path = multi_stage_shortest_path(stage_nodes, graph)
    print_results(source, destination, cost, path)

    if path:
        print("\nDisplaying graph with optimal path highlighted...")
        draw_graph(stage_nodes, edges, optimal_path=path, title="Optimal Path Highlighted in Multi-Stage Graph")


if __name__ == "__main__":
    main()