import sys
import math
import random
import time

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
    d = [[0.0] * M for _ in range(N)]
    for i in range(N):
        _, _, fx, fy = stores[i]
        for j in range(M):
            _, cx, cy = customers[j]
            d[i][j] = math.hypot(fx - cx, fy - cy)
    return d

def get_near(N, M, dist, K):
    K = min(K, N)
    near = []
    for j in range(M):
        idx = list(range(N))
        idx.sort(key=lambda i: dist[i][j])
        near.append(idx[:K])
    return near

def get_cost(N, M, stores, customers, dist, assign):
    cap = [stores[i][1] for i in range(N)]
    opened = [False] * N
    total = 0.0
    for j in range(M):
        i = assign[j]
        cap[i] -= customers[j][0]
        if cap[i] < 0:
            return float("inf")
        if not opened[i]:
            opened[i] = True
            total += stores[i][0]
        total += dist[i][j]
    return total

def repair(N, M, stores, customers, near, assign):
    cap = [stores[i][1] for i in range(N)]
    for j in range(M):
        cap[assign[j]] -= customers[j][0]

    bad = [j for j in range(M) if cap[assign[j]] < 0]
    if not bad:
        return assign

    for j in bad:
        cap[assign[j]] += customers[j][0]
        assign[j] = -1

    bad.sort(key=lambda j: -customers[j][0])
    for j in bad:
        demand = customers[j][0]
        chosen = -1
        for i in near[j]:
            if cap[i] >= demand:
                chosen = i
                break
        if chosen == -1:
            for i in range(N):
                if cap[i] >= demand:
                    chosen = i
                    break
        assign[j] = chosen
        cap[chosen] -= demand

    return assign

def greedy(N, M, stores, customers, dist, near, open_bias=0.05):
    cap = [stores[i][1] for i in range(N)]
    opened = [False] * N
    assign = [-1] * M

    order = list(range(M))
    order.sort(key=lambda j: (-customers[j][0], random.random()))

    for j in order:
        dj = customers[j][0]
        best_i, best_val = -1, float("inf")
        for i in near[j]:
            if cap[i] < dj:
                continue
            val = dist[i][j] + (open_bias * stores[i][0] if not opened[i] else 0.0)
            if val < best_val:
                best_val, best_i = val, i

        if best_i == -1:
            for i in range(N):
                if cap[i] >= dj:
                    best_i = i
                    break

        assign[j] = best_i
        cap[best_i] -= dj
        opened[best_i] = True

    return assign, get_cost(N, M, stores, customers, dist, assign)

def tournament(pop, costs, k=3):
    best = None
    n = len(pop)
    for _ in range(k):
        idx = random.randrange(n)
        if best is None or costs[idx] < costs[best]:
            best = idx
    return pop[best]

def crossover(a1, a2):
    M = len(a1)
    return [a1[j] if random.random() < 0.5 else a2[j] for j in range(M)]

def mutate(assign, N, p=0.3, moves=2):
    if random.random() > p:
        return assign
    a = assign[:]
    M = len(a)
    for _ in range(moves):
        j = random.randrange(M)
        a[j] = random.randrange(N)
    return a

def genetic(N, M, stores, customers, time_limit=60.0, pop_size=30, elite=3, K_near=30):
    dist = dist_matrix(N, M, stores, customers)
    near = get_near(N, M, dist, K_near)

    pop, costs = [], []
    biases = [0.0, 0.05, 0.15]

    while len(pop) < pop_size:
        a, c = greedy(N, M, stores, customers, dist, near, open_bias=biases[len(pop) % len(biases)])
        pop.append(a)
        costs.append(c)

    best_idx = min(range(len(pop)), key=lambda i: costs[i])
    best_assign = pop[best_idx][:]
    best_cost = costs[best_idx]

    start = time.time()
    deadline = start + time_limit

    while time.time() < deadline:
        n = len(pop)
        order = sorted(range(n), key=lambda i: costs[i])
        e = min(elite, n)

        new_pop = [pop[i] for i in order[:e]]
        new_costs = [costs[i] for i in order[:e]]

        while len(new_pop) < pop_size:
            p1 = tournament(pop, costs)
            p2 = tournament(pop, costs)

            child = crossover(p1, p2)
            child = mutate(child, N)
            child = repair(N, M, stores, customers, near, child)
            c = get_cost(N, M, stores, customers, dist, child)

            new_pop.append(child)
            new_costs.append(c)

        pop, costs = new_pop, new_costs

        cur_idx = min(range(len(pop)), key=lambda i: costs[i])
        if costs[cur_idx] < best_cost:
            best_cost = costs[cur_idx]
            best_assign = pop[cur_idx][:]

    opened = sorted(set(best_assign))
    return best_cost, opened, best_assign

if __name__ == "__main__":
    N, M, stores, customers = read_input(sys.argv[1])

    best_cost = float("inf")
    best_opened = []
    best_assign = []

    for r in range(3):
        cost, opened, assign = genetic(
            N, M, stores, customers,
            time_limit=90,
            pop_size=40,
            elite=5,
            K_near=30,
        )
        if cost < best_cost:
            best_cost = cost
            best_opened = opened
            best_assign = assign

    print(math.ceil(best_cost))
    print(*best_opened)
    print(*best_assign)