import random
import time
import sys
import math

def read_input(filename):
    with open(filename) as f:
        n = int(f.readline())
        coords = []
        for _ in range(n):
            x, y = map(float, f.readline().split())
            coords.append((x, y))
    return n, coords

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

def nn_tour(n, start=0):
    unused = set(range(n))
    unused.remove(start)
    tour = [start]
    cur = start
    while unused:
        nxt = min(unused, key=lambda j: dist(cur, j, coords))
        tour.append(nxt)
        unused.remove(nxt)
        cur = nxt
    return tour, tour_dist(tour, coords)

def aco(
        n,
        coords,
        time_limit=90.0,
        ants=30,
        alpha=1.0,
        beta=3.0,
        global_rho=0.05,
        local_rho=0.05,
):
    best_tour, best_cost = nn_tour(n)

    tau = 1.0 / (n * best_cost)
    pheromone = [[tau] * n for _ in range(n)]

    start_time = time.time()
    no_improve = 0

    def h(i, j):
        d = dist(i, j, coords)
        return 1.0 / d if d > 0 else 0.0

    def choose_next(cur, visited):
        cands = [j for j in range(n) if not visited[j]]

        vals = []
        total = 0.0
        for j in cands:
            v = (pheromone[cur][j] ** alpha) * (h(cur, j) ** beta)
            vals.append((j, v))
            total += v

        if total == 0:
            return random.choice(cands)

        r = random.random() * total
        s = 0.0
        for j, v in vals:
            s += v
            if s >= r:
                return j

        return vals[-1][0]

    def local_pheromone_update(i, j):
        t = pheromone[i][j]
        t = (1.0 - local_rho) * t + local_rho * tau
        pheromone[i][j] = t
        pheromone[j][i] = t

    def global_pheromone_update(best_tour, best_cost):
        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= (1.0 - global_rho)

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
        iter_best_tour = []
        iter_best_cost = float("inf")

        starts = [random.randrange(n) for _ in range(ants)]

        for a in range(ants):
            tour, tour_cost = run_ant(starts[a])

            if tour_cost < iter_best_cost:
                iter_best_cost = tour_cost
                iter_best_tour = tour[:]

        if iter_best_cost < best_cost:
            best_cost = iter_best_cost
            best_tour = iter_best_tour[:]
            no_improve = 0
        else:
            no_improve += 1

        global_pheromone_update(best_tour, best_cost)

        if no_improve > 80:
            for i in range(n):
                for j in range(n):
                    pheromone[i][j] = tau
            no_improve = 0

    return best_tour, best_cost


if __name__ == "__main__":
    filename = sys.argv[1]
    n, coords = read_input(filename)

    best_cost = float("inf")
    best_tour = []

    time_limit = 90
    if n > 5000:
        time_limit=5
    elif n > 1000:
        time_limit = 60

    for r in range(3):
        tour, cost = aco(
            n,
            coords,
            time_limit,
            ants=25,
            alpha=1.0,
            beta=3.0,
            global_rho=0.05,
        )
        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    print(int(best_cost))
    print(*best_tour)