import matplotlib.pyplot as plt
import pandas as pd

def knapsack(weights, values, capacity):
    n = len(weights)
   
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

  
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w],
                               values[i-1] + dp[i-1][w - weights[i-1]])
            else:
                dp[i][w] = dp[i-1][w]

    return dp


def visualize(dp, test_case_num):
    df = pd.DataFrame(dp)
    
    print(f"\nDP Table for Test Case {test_case_num}:")
    print(df)

   
    plt.figure()
    plt.imshow(df, aspect='auto')
    plt.title(f"Knapsack DP Table (Test Case {test_case_num})")
    plt.xlabel("Capacity")
    plt.ylabel("Items")
    plt.colorbar()
    plt.show()



t = 3  
for tc in range(1, t + 1):
    print(f"\n--- Test Case {tc} ---")
    
    n = int(input("Enter number of items: "))
    
    weights = list(map(int, input("Enter weights: ").split()))
    values = list(map(int, input("Enter values: ").split()))
    
    capacity = int(input("Enter capacity: "))

    dp = knapsack(weights, values, capacity)

    print(f"Maximum Value: {dp[n][capacity]}")

    visualize(dp, tc)