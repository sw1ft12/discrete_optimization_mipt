import sys
import math
import random
import time

def read_input(filename):
    with open(filename) as f:
        n, v, c = map(int, f.readline().split())
        data = []
        for _ in range(n):
            d, x, y = map(float, f.readline().split())
            data.append((d, x, y))
    return n, v, c, data

def dist(i, j, coords):
    dx = coords[i][0] - coords[j][0]
    dy = coords[i][1] - coords[j][1]
    return math.hypot(dx, dy)

def tour_dist(tour, coords):
    n = len(tour)
    s = 0.0
    for i in range(n):
        s += dist(tour[i], tour[(i + 1) % n], coords)
    return s

def nn_tour(n, coords, start=0):
    unused = set(range(n))
    unused.remove(start)
    tour = [start]
    cur = start
    while unused:
        nxt = min(unused, key=lambda j: dist(cur, j, coords))
        tour.append(nxt)
        unused.remove(nxt)
        cur = nxt
    return tour

def get_cands(n, coords, K=25):
    cand = []
    for i in range(n):
        neigh = list(range(n))
        neigh.remove(i)
        neigh.sort(key=lambda j: dist(i, j, coords))
        cand.append(neigh[:min(K, n - 1)])
    return cand


def two_opt_delta(tour, i, j, coords):
    n = len(tour)
    a = tour[(i - 1) % n]
    b = tour[i]
    c = tour[j]
    d = tour[(j + 1) % n]
    return dist(a, c, coords) + dist(b, d, coords) - dist(a, b, coords) - dist(c, d, coords)


def two_opt(tour, coords, max_tries=4000):
    n = len(tour)
    for _ in range(max_tries):
        i, j = sorted(random.sample(range(n), 2))
        if i == 0:
            continue
        dlt = two_opt_delta(tour, i, j, coords)
        if dlt < 0:
            tour[i:j + 1] = reversed(tour[i:j + 1])
            return dlt
    return 0.0


def aco(
        n,
        coords,
        time_limit=90.0,
        ants=30,
        alpha=1.0,
        beta=3.0,
        global_rho=0.1,
        local_rho=0.1,
        K=25,
):
    cands = get_cands(n, coords, K=K)

    nn = nn_tour(n, coords, start=0)
    nn_len = tour_dist(nn, coords)

    tau = 1.0 / (n * nn_len)
    pheromone = [[tau] * n for _ in range(n)]

    best_tour = nn[:]
    best_cost = nn_len

    start_time = time.time()
    it = 0
    no_improve = 0

    def h(i, j):
        d = dist(i, j, coords)
        return 1.0 / d if d > 0 else 0.0

    def choose_next(cur, visited):
        candidates = [j for j in cands[cur] if not visited[j]]
        if not candidates:
            candidates = [j for j in range(n) if not visited[j]]

        if random.random() < 0.9:
            best_j = None
            best_val = -1.0
            for j in candidates:
                val = (pheromone[cur][j] ** alpha) * (h(cur, j) ** beta)
                if val > best_val:
                    best_val = val
                    best_j = j
            return best_j
        else:
            vals = []
            s = 0.0
            for j in candidates:
                v = (pheromone[cur][j] ** alpha) * (h(cur, j) ** beta)
                vals.append((j, v))
                s += v

            r = random.random() * s
            acc = 0.0
            for j, v in vals:
                acc += v
                if acc >= r:
                    return j
            return vals[-1][0]

    def local_pheromone_update(i, j):
        t = pheromone[i][j]
        t = (1.0 - local_rho) * t + local_rho * tau
        pheromone[i][j] = t
        pheromone[j][i] = t

    def global_pheromone_update(best_tour, best_cost):
        for i in range(n):
            row = pheromone[i]
            for j in range(n):
                row[j] *= (1.0 - global_rho)

        d = global_rho * (1.0 / best_cost)
        for i in range(n):
            a = best_tour[i]
            b = best_tour[(i + 1) % n]
            pheromone[a][b] += d
            pheromone[b][a] += d

    def run_ant(start):
        visited = [False] * n
        tour = [start]
        visited[start] = True
        cur = start

        while len(tour) < n:
            nxt = choose_next(cur, visited)
            tour.append(nxt)
            visited[nxt] = True

            local_pheromone_update(cur, nxt)

            cur = nxt

        local_pheromone_update(tour[-1], tour[0])

        return tour, tour_dist(tour, coords)

    while time.time() - start_time < time_limit:
        it += 1

        iter_best_tour = None
        iter_best_cost = float("inf")

        for a in range(ants):
            tour, tour_cost = run_ant(0)

            if random.random() < 0.25:
                dlt = two_opt(tour, coords, max_tries=1500)
                if dlt < 0:
                    tour_cost += dlt

            if tour_cost < iter_best_cost:
                iter_best_cost = tour_cost
                iter_best_tour = tour

        if iter_best_cost < best_cost:
            best_cost = iter_best_cost
            best_tour = iter_best_tour[:]
            no_improve = 0
        else:
            no_improve += 1

        if it % 10 == 0:
            for _ in range(20):
                dlt = two_opt(best_tour, coords, max_tries=3000)
                if dlt < 0:
                    best_cost += dlt
                else:
                    break

        global_pheromone_update(best_tour, best_cost)

        if no_improve > 80:
            for i in range(n):
                for j in range(n):
                    pheromone[i][j] = tau
            no_improve = 0

    for _ in range(100):
        dlt = two_opt(best_tour, coords, max_tries=5000)
        if dlt < 0:
            best_cost += dlt
        else:
            break

    return best_tour, best_cost

def bin_packing(n, v, c, data):
    clients = list(range(n))

    clients.sort(key=lambda i: -data[i][0])

    routes = []
    loads = []

    for i in clients:
        demand = data[i][0]
        placed = False

        for j in range(len(routes)):
            if loads[j] + demand <= c:
                routes[j].append(i)
                loads[j] += demand
                placed = True
                break

        if not placed:
            routes.append([i])
            loads.append(demand)

    return routes


def vrp(n, v, c, data):
    packed = bin_packing(n, v, c, data)

    routes = []
    total_dist = 0

    for r in packed:
        coords = [(0.0, 0.0)] + [(data[i][1], data[i][2]) for i in r]
        m = len(coords)

        tour, cost = aco(
            m,
            coords,
            time_limit=1,
            ants=30,
            beta=3.0,
            global_rho=0.05,
            local_rho=0.05,
            K=30
        )

        route = [r[i-1] for i in tour if i > 0]
        routes.append(route)
        total_dist += cost

    return routes, total_dist

if __name__ == "__main__":
    filename = sys.argv[1]
    n, v, c, data = read_input(filename)
    routes, total = vrp(n, v, c, data)

    print(math.ceil(total))
    for r in routes:
        print(*r)