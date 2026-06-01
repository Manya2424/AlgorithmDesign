import matplotlib.pyplot as plt
import numpy as np
import time


def is_safe(board, row, col, n):
 
    for i in range(row):
        if board[i][col] == 1:
            return False

   
    i, j = row-1, col-1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

   
    i, j = row-1, col+1
    while i >= 0 and j < n:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1

    return True



def print_board(board, n):
    print("\nChess Board:")
    print("  " + " ".join(str(i) for i in range(n)))
    for i in range(n):
        row = []
        for j in range(n):
            if board[i][j] == 1:
                row.append("Q")
            else:
                row.append(".")
        print(f"{i} " + " ".join(row))


def visualize_board(board, n, title="N-Queens Solution"):
    grid = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if board[i][j] == 1:
                grid[i][j] = 2 

    plt.figure()
    plt.imshow(grid)

   
    for i in range(n):
        for j in range(n):
            if board[i][j] == 1:
                plt.text(j, i, '♛', ha='center', va='center', fontsize=20)

    plt.title(title)
    plt.xticks(range(n))
    plt.yticks(range(n))
    plt.grid()
    plt.show()



def solve_nqueens(board, row, n, solutions, step_visual=False):
    if row == n:
        solutions.append([row[:] for row in board])
        return

    for col in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = 1

            if step_visual:
                print(f"\nPlaced Queen at ({row}, {col})")
                print_board(board, n)
                time.sleep(0.5)

            solve_nqueens(board, row + 1, n, solutions, step_visual)

           
            board[row][col] = 0

            if step_visual:
                print(f"\nBacktracking from ({row}, {col})")
                print_board(board, n)
                time.sleep(0.5)



def main():
    n = int(input("Enter value of N: "))

    board = [[0]*n for _ in range(n)]
    solutions = []

    print("\n--- Solving N-Queens ---")
    solve_nqueens(board, 0, n, solutions, step_visual=True)

    if not solutions:
        print("\n❌ No solution exists")
        return

    print(f"\n✅ Total Solutions Found: {len(solutions)}")

  
    for idx, sol in enumerate(solutions):
        print(f"\nSolution {idx+1}:")
        print_board(sol, n)

       
        visualize_board(sol, n, f"Solution {idx+1}")



if __name__ == "__main__":
    main()