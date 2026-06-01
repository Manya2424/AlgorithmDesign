import matplotlib.pyplot as plt


def initialize_table(m, n):
    return [[0 for _ in range(n + 1)] for _ in range(m + 1)]


def print_step(i, j, char_x, char_y, table, match):
    if match:
        print(f"Comparing {char_x} and {char_y} -> Match")
        print(f"L[{i}][{j}] = 1 + L[{i-1}][{j-1}] = 1 + {table[i-1][j-1]} = {table[i][j]}")
    else:
        top = table[i - 1][j]
        left = table[i][j - 1]
        print(f"Comparing {char_x} and {char_y} -> Not equal")
        print(f"L[{i}][{j}] = max(L[{i-1}][{j}], L[{i}][{j-1}]) = max({top}, {left}) = {table[i][j]}")
    print()


def build_lcs_table(X, Y):
    m = len(X)
    n = len(Y)
    L = initialize_table(m, n)

    print("\n--- Step-by-step DP table filling ---\n")

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                L[i][j] = 1 + L[i - 1][j - 1]
                print_step(i, j, X[i - 1], Y[j - 1], L, True)
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
                print_step(i, j, X[i - 1], Y[j - 1], L, False)

    return L


def print_dp_table(X, Y, L):
    print("\n--- Final DP Table ---\n")

    header = [" "] + ["0"] + list(Y)
    print("{:>4}".format(""), end="")
    for ch in header[1:]:
        print("{:>4}".format(ch), end="")
    print()

    row_labels = ["0"] + list(X)
    for i in range(len(L)):
        print("{:>4}".format(row_labels[i]), end="")
        for j in range(len(L[0])):
            print("{:>4}".format(L[i][j]), end="")
        print()


def backtrack_lcs(X, Y, L):
    i = len(X)
    j = len(Y)
    lcs_chars = []
    path = [(i, j)]

    print("\n--- Backtracking to find LCS ---\n")

    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            print(f"Match found: {X[i - 1]} -> include in LCS")
            print("Move diagonally\n")
            lcs_chars.append(X[i - 1])
            i -= 1
            j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            print(f"No match at X[{i - 1}]={X[i - 1]} and Y[{j - 1}]={Y[j - 1]}")
            print("Move up\n")
            i -= 1
        else:
            print(f"No match at X[{i - 1}]={X[i - 1]} and Y[{j - 1}]={Y[j - 1]}")
            print("Move left\n")
            j -= 1

        path.append((i, j))

    lcs_chars.reverse()
    return "".join(lcs_chars), path


def visualize_dp_table(X, Y, L, path):
    fig, ax = plt.subplots(figsize=(max(8, len(Y) + 3), max(6, len(X) + 3)))
    ax.axis('off')

    rows = ["0"] + list(X)
    cols = ["0"] + list(Y)

    table_text = []
    table_text.append([" "] + cols)
    for i in range(len(L)):
        table_text.append([rows[i]] + [str(val) for val in L[i]])

    cell_colours = [["white" for _ in range(len(cols) + 1)] for _ in range(len(rows) + 1)]

    for r in range(1, len(rows) + 1):
        cell_colours[r][0] = "#d9ead3"
    for c in range(1, len(cols) + 1):
        cell_colours[0][c] = "#cfe2f3"

    for (i, j) in path:
        cell_colours[i + 1][j + 1] = "#ffe599"

    table = ax.table(
        cellText=table_text,
        cellColours=cell_colours,
        cellLoc='center',
        loc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)

    plt.title("LCS Dynamic Programming Table (Highlighted Backtracking Path)", fontsize=14)
    plt.tight_layout()
    plt.show()


def solve_lcs():
    X = input("Enter first string: ").strip()
    Y = input("Enter second string: ").strip()

    L = build_lcs_table(X, Y)
    print_dp_table(X, Y, L)

    lcs_string, path = backtrack_lcs(X, Y, L)

    print("--- Final Output ---\n")
    print(f"Length of LCS: {L[len(X)][len(Y)]}")
    print(f"LCS: {lcs_string}")

    choice = input("\nDo you want to visualize the DP table? (y/n): ").strip().lower()
    if choice == 'y':
        visualize_dp_table(X, Y, L, path)


if __name__ == "__main__":
    solve_lcs()