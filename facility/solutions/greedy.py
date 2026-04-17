import sys
import math


def read_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    first = lines[0].split()
    N, M = int(first[0]), int(first[1])

    stores = []
    for i in range(1, N+1):
        parts = list(map(float, lines[i].split()))
        s = parts[0]
        cap = parts[1]
        x, y = parts[2], parts[3]
        stores.append((s, cap, x, y))

    customers = []
    for j in range(N+1, N+M+1):
        parts = list(map(float, lines[j].split()))
        d = parts[0]
        x, y = parts[1], parts[2]
        customers.append((d, x, y))

    return N, M, stores, customers

def distance(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)

def greedy(N, M, stores, customers):
    opened = list(range(N))
    remaining_capacity = [stores[i][1] for i in opened]

    assignments = [-1] * M
    total_cost = sum(stores[i][0] for i in opened)

    customers_order = sorted(range(M), key=lambda j: -customers[j][0])

    for j in customers_order:
        demand, cx, cy = customers[j]
        best_store = -1
        best_dist = float('inf')

        for i in opened:
            if remaining_capacity[i] >= demand:
                dist = distance(stores[i][2], stores[i][3], cx, cy)
                if dist < best_dist - 1e-9:
                    best_dist = dist
                    best_store = i

        assignments[j] = best_store
        remaining_capacity[best_store] -= demand
        total_cost += distance(stores[best_store][2], stores[best_store][3], cx, cy)

    return total_cost, opened, assignments

if __name__ == "__main__":
    filename = sys.argv[1]
    N, M, stores, customers = read_input(filename)
    cost, opened, assignments = greedy(N, M, stores, customers)
    print(f"{cost:.0f}")
    print(*opened)
    print(*assignments)