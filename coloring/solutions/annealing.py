import math
import random
import sys
import time

def read_input(filename):
    with open(filename) as f:
        n, m = map(int, f.readline().split())
        graph = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, f.readline().split())
            graph[u].append(v)
            graph[v].append(u)

    return n, m, graph

def get_coloring(n, graph, perm):
    coloring = [-1] * n
    max_color = 0

    for v in perm:
        used = set()
        for u in graph[v]:
            if coloring[u] != -1:
                used.add(coloring[u])

        color = 0
        while color in used:
            color += 1

        coloring[v] = color
        if color > max_color:
            max_color = color

    return coloring, max_color

def get_neighbour(current_perm, coloring):
    perm = current_perm.copy()

    rand = random.random()

    if rand < 0.4:
        i, j = random.sample(range(n), 2)
        perm[i], perm[j] = perm[j], perm[i]

    elif rand < 0.6:
        i, j = random.sample(range(n), 2)
        vertex = perm.pop(i)
        perm.insert(j, vertex)

    else:
        i, j = sorted(random.sample(range(n), 2))
        random.shuffle(perm[i:j+1])

    return *get_coloring(n, graph, perm), perm


def annealing(n, m, graph, T=1000, time_limit=30):
    current_perm = list(range(n))
    random.shuffle(current_perm)

    current_coloring, current_max_color = get_coloring(n, graph, current_perm)
    best_coloring, best_max_color = current_coloring.copy(), current_max_color

    start_time = time.time()
    no_improve = 0

    while time.time() - start_time < time_limit:
        neighbour_coloring, neighbour_max_color, neighbour_perm = get_neighbour(current_perm, current_coloring)
        delta = neighbour_max_color - current_max_color

        if delta < 0 or random.random() < math.exp(-delta / T):
            current_perm = neighbour_perm
            current_coloring, current_max_color = neighbour_coloring, neighbour_max_color

            if current_max_color < best_max_color:
                best_coloring, best_max_color = current_coloring.copy(), current_max_color
                no_improve = 0
            else:
                no_improve += 1
        else:
            no_improve += 1

        if no_improve > 1000:
            T = 500
            no_improve = 0
        else:
            T *= 0.999
            if T < 1e-3:
                T = 1000

        if no_improve > 2000:
            random.shuffle(current_perm)
            current_coloring, current_max_color = get_coloring(n, graph, current_perm)
            if current_max_color < best_max_color:
                best_coloring, best_max_color = current_coloring.copy(), current_max_color

            T = 1000
            no_improve = 0

    return best_coloring, best_max_color

if __name__ == "__main__":
    filename = sys.argv[1]
    n, m, graph = read_input(filename)

    best_max_color = n + 1
    best_coloring = []

    for i in range(3):
        coloring, max_color = annealing(n, m, graph, time_limit=90)
        if max_color < best_max_color:
            best_max_color = max_color
            best_coloring = coloring

    print(best_max_color + 1)
    print(*best_coloring)