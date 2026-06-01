import networkx as nx
import matplotlib.pyplot as plt


COLOR_MAP = {
    1: "\033[91m●\033[0m",  # Red
    2: "\033[92m●\033[0m",  # Green
    3: "\033[94m●\033[0m",  # Blue
    4: "\033[93m●\033[0m",  # Yellow
    5: "\033[95m●\033[0m",  # Purple
    0: "○"
}


def is_safe(v, graph, colors, c):
    for i in range(len(graph)):
        if graph[v][i] == 1 and colors[i] == c:
            return False
    return True



def solve_coloring(graph, m, colors, v, steps):
    if v == len(graph):
        return True

    for c in range(1, m + 1):
        if is_safe(v, graph, colors, c):
            colors[v] = c
            steps.append((v, c, colors.copy()))

            if solve_coloring(graph, m, colors, v + 1, steps):
                return True

          
            colors[v] = 0
            steps.append((v, "BACKTRACK", colors.copy()))

    return False



def find_chromatic_number(graph):
    n = len(graph)

    for m in range(1, n + 1):
        colors = [0] * n
        steps = []

        if solve_coloring(graph, m, colors, 0, steps):
            return m, colors, steps

    return None, None, None



def print_colored_output(colors):
    print("\n🎨 Vertex Coloring:")
    for i, c in enumerate(colors):
        print(f"Vertex {i} → {COLOR_MAP[c]} (Color {c})")



def draw_graph(graph, colors=None, title="Graph"):
    G = nx.Graph()
    n = len(graph)

    for i in range(n):
        G.add_node(i)

    for i in range(n):
        for j in range(n):
            if graph[i][j] == 1:
                G.add_edge(i, j)

    pos = nx.spring_layout(G)

    if colors:
        color_list = []
        color_dict = {
            1: "red",
            2: "green",
            3: "blue",
            4: "yellow",
            5: "purple"
        }
        for c in colors:
            color_list.append(color_dict.get(c, "gray"))
    else:
        color_list = "lightgray"

    plt.figure()
    nx.draw(G, pos, with_labels=True, node_color=color_list, node_size=800)
    plt.title(title)
    plt.show()



def print_steps(steps):
    print("\n🔄 Dry Run (Backtracking Steps):\n")
    for step in steps:
        v, c, state = step
        print(f"Vertex {v} → {c}, State: {state}")



def run_test_case(graph, name):
    print(f"\n================ {name} ================")

    print("\n📌 Input Graph (Adjacency Matrix):")
    for row in graph:
        print(row)

    draw_graph(graph, title=f"{name} - Before Coloring")

    chromatic, colors, steps = find_chromatic_number(graph)

    print(f"\n✅ Chromatic Number = {chromatic}")

    print_steps(steps)

    print_colored_output(colors)

    draw_graph(graph, colors, title=f"{name} - After Coloring")


def main():

   
    graph1 = [
        [0,1,0,1],
        [1,0,1,0],
        [0,1,0,1],
        [1,0,1,0]
    ]

    
    graph2 = [
        [0,1,1,1],
        [1,0,1,1],
        [1,1,0,1],
        [1,1,1,0]
    ]

    
    graph3 = [
        [0,1,1,0],
        [1,0,0,1],
        [1,0,0,0],
        [0,1,0,0]
    ]

    run_test_case(graph1, "Test Case 1 (Cycle Graph)")
    run_test_case(graph2, "Test Case 2 (Complete Graph)")
    run_test_case(graph3, "Test Case 3 (Tree Graph)")


if __name__ == "__main__":
    main()