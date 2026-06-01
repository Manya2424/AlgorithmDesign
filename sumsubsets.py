import matplotlib.pyplot as plt
import networkx as nx


def subset_sum(arr, target, index, current_sum, subset, all_subsets, steps, path):
    
    steps.append((index, current_sum, subset.copy()))

   
    if current_sum == target:
        all_subsets.append(subset.copy())
        return

    
    if current_sum > target or index >= len(arr):
        return

    
    subset.append(arr[index])
    subset_sum(arr, target, index + 1, current_sum + arr[index], subset, all_subsets, steps, path + f" -> {arr[index]}")

    
    subset.pop()

   
    subset_sum(arr, target, index + 1, current_sum, subset, all_subsets, steps, path)



def print_matrix(subsets):
    print("\n📊 Subsets Matrix Representation:\n")
    max_len = max(len(s) for s in subsets) if subsets else 0

    for i, subset in enumerate(subsets):
        row = subset + ['-'] * (max_len - len(subset))
        print(f"Subset {i+1}: {row}")



def print_steps(steps):
    print("\n🔄 Backtracking Steps:\n")
    for step in steps:
        print(f"Index: {step[0]}, Sum: {step[1]}, Subset: {step[2]}")


def visualize_tree(steps):
    G = nx.DiGraph()

    for i in range(len(steps)-1):
        G.add_edge(str(steps[i]), str(steps[i+1]))

    pos = nx.spring_layout(G)

    plt.figure()
    nx.draw(G, pos, with_labels=False, node_size=500)
    plt.title("Backtracking Flow (Simplified)")
    plt.show()


def main():
    n = int(input("Enter number of elements: "))
    arr = list(map(int, input("Enter elements: ").split()))
    target = int(input("Enter target sum: "))

    all_subsets = []
    steps = []

    print("\n--- Running Sum of Subsets ---")
    subset_sum(arr, target, 0, 0, [], all_subsets, steps, "")

 
    print_steps(steps)

    
    if not all_subsets:
        print("\n❌ No subset found")
    else:
        print("\n✅ Subsets with required sum:")
        for s in all_subsets:
            print(s)

        print_matrix(all_subsets)

    visualize_tree(steps)



if __name__ == "__main__":
    main()