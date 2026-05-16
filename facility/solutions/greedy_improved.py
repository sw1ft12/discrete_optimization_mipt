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

def dist_matrix(N, M, stores, customers):
    dist = [[0.0] * M for _ in range(N)]
    for i in range(N):
        _, _, fx, fy = stores[i]
        row = dist[i]
        for j in range(M):
            _, cx, cy = customers[j]
            row[j] = math.hypot(fx - cx, fy - cy)
    return dist

def get_near(N, M, dist, K=30):
    K = min(K, N)
    near = []
    for j in range(M):
        idx = list(range(N))
        idx.sort(key=lambda i: dist[i][j])
        near.append(idx[:K])
    return near

def greedy(N, M, stores, customers, open_bias=0.05):
    dist = dist_matrix(N, M, stores, customers)
    near = get_near(N, M, dist, K=50)

    cap = [stores[i][1] for i in range(N)]
    opened = [False] * N
    assign = [-1] * M
    total = 0.0

    order = list(range(M))
    order.sort(key=lambda j: -customers[j][0])

    for j in order:
        demand = customers[j][0]
        best_i, best_val = -1, float("inf")

        for i in near[j]:
            if cap[i] < demand:
                continue
            val = dist[i][j] + (open_bias * stores[i][0] if not opened[i] else 0.0)
            if val < best_val:
                best_val, best_i = val, i

        if best_i == -1:
            for i in range(N):
                if cap[i] >= demand:
                    best_i = i
                    break

        assign[j] = best_i
        cap[best_i] -= demand
        opened[best_i] = True

    for i in range(N):
        if opened[i]:
            total += stores[i][0]
    for j in range(M):
        total += dist[assign[j]][j]

    opened_list = [i for i in range(N) if opened[i]]
    return total, opened_list, assign


if __name__ == "__main__":
    N, M, stores, customers = read_input(sys.argv[1])

    best_cost = float("inf")
    best_opened = []
    best_assign = []

    biases = [i * 0.1 for i in range(21)]

    for bias in biases:
        cost, opened, assign = greedy(
            N, M, stores, customers,
            open_bias=bias
        )
        if cost < best_cost:
            best_cost, best_opened, best_assign = cost, opened, assign

    print(int(best_cost))
    print(*best_opened)
    print(*best_assign)