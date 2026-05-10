import sys

def knapsack_dp(n, capacity, items):
    dp = [0] * (capacity + 1)
    taken = [[False] * (capacity + 1) for _ in range(n)]

    for i in range(n):
        cost, weight = items[i]
        for j in range(capacity, weight - 1, -1):
            if dp[j - weight] + cost > dp[j]:
                dp[j] = dp[j - weight] + cost
                taken[i][j] = True

    result = []
    remaining = capacity
    for i in range(n - 1, -1, -1):
        if taken[i][remaining]:
            result.append(i)
            remaining -= items[i][1]

    return dp[capacity], result

def main():
    first_line = sys.stdin.readline().strip()
    while first_line and first_line.startswith('#'):
        first_line = sys.stdin.readline().strip()

    n, capacity = map(int, first_line.split())

    items = []
    for _ in range(n):
        line = sys.stdin.readline().strip()
        while line and line.startswith('#'):
            line = sys.stdin.readline().strip()
        if not line:
            continue
        cost, weight = map(int, line.split())
        items.append((cost, weight))

    max_cost, taken_items = knapsack_dp(n, capacity, items)

    print(max_cost)

    print(*taken_items, sep=" ")


if __name__ == "__main__":
    main()