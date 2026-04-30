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

def color(n, graph, perm):
    cols = [-1] * n
    max_col = 0
    for i in perm:
        col = 0
        used = []
        for to in graph[i]:
            if cols[to] != -1:
                used.append(cols[to])

        used.sort()
        for c in used:
            if c == col:
                col += 1

        cols[i] = col
        max_col = max(max_col, col)

    return cols, max_col
#
# def get_neighbour(n, graph):
#     perm = [i for i in range(n)]
#     random.shuffle(perm)
#     return color(n, graph, perm)
#
# def annealing(n, m, graph, T=1000, time_limit=120):
#     current_sol, current_cost = [], float("inf")
#     best_sol, best_cost = current_sol, current_cost
#     start_time = time.time()
#
#     no_improve = 0
#
#     while time.time() - start_time < time_limit:
#         neighbor_sol, neighbor_cost = get_neighbour(n, graph)
#         delta = neighbor_cost - current_cost
#
#         if delta < 0 or random.random() < math.exp(-delta / T):
#             current_sol, current_cost = neighbor_sol, neighbor_cost
#             if current_cost < best_cost:
#                 best_sol, best_cost = current_sol, current_cost
#
#             no_improve = 0
#         else:
#             no_improve += 1
#
#         if no_improve > 1000:
#             T = 500
#             no_improve = 0
#         else:
#             T *= 0.999
#             if T < 1e-3:
#                 T = 1000
#
#     return best_sol, best_cost


def get_neighbour(n, graph, perm, cols):
    new_perm = perm.copy()

    choice = random.choice(['swap', 'insert', 'reverse'])

    if choice == 'swap':
        i, j = random.sample(range(n), 2)
        new_perm[i], new_perm[j] = new_perm[j], new_perm[i]

    elif choice == 'insert':
        i, j = random.sample(range(n), 2)
        vertex = new_perm.pop(i)
        new_perm.insert(j, vertex)

    elif choice == 'reverse':
        i, j = sorted(random.sample(range(n), 2))
        new_perm[i:j+1] = reversed(new_perm[i:j+1])

    conflicts = []
    for v in range(n):
        color_v = cols[v]
        conflict_count = sum(1 for u in graph[v] if cols[u] == color_v)
        if conflict_count > 0:
            conflicts.append((conflict_count, v))

    if conflicts:
        _, worst_vertex = max(conflicts)
        pos = new_perm.index(worst_vertex)
        new_pos = random.randint(0, n-1)
        vertex = new_perm.pop(pos)
        new_perm.insert(new_pos, vertex)

    return color(n, graph, new_perm)

def color_with_conflicts(n, graph, perm):
    cols = [-1] * n
    max_col = 0

    for i in perm:
        # Подсчитываем доступные цвета
        used_colors = set()
        neighbor_colors = set()

        for to in graph[i]:
            if cols[to] != -1:
                neighbor_colors.add(cols[to])

        # Жадный выбор минимального доступного цвета
        col = 0
        while col in neighbor_colors:
            col += 1

        cols[i] = col
        max_col = max(max_col, col)

    return cols, max_col

def annealing(n, m, graph, time_limit=120):
    initial_perm = list(range(n))
    random.shuffle(initial_perm)

    current_sol, current_cost = color(n, graph, initial_perm)
    best_sol, best_cost = current_sol.copy(), current_cost

    start_time = time.time()
    T = 1000
    no_improve = 0

    current_perm = initial_perm

    while time.time() - start_time < time_limit:
        neighbour_sol, neighbour_cost = get_neighbour(n, graph, current_perm, c)

        delta = neighbour_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / T):
            current_perm = neighbour_perm
            current_sol, current_cost = neighbour_sol, neighbour_cost

            if current_cost < best_cost:
                best_sol, best_cost = current_sol.copy(), current_cost
                no_improve = 0
            else:
                no_improve += 1
        else:
            no_improve += 1

        if no_improve > 1000:
            T = 500
            no_improve = 0

    return best_sol, best_cost

if __name__ == "__main__":
    filename = sys.argv[1]
    n, m, graph = read_input(filename)
    best_sol, best_total_colors = [], float("inf")
    for i in range(3):
        sol, total_colors = annealing(n, m, graph, time_limit=90)
        if total_colors < best_total_colors:
            best_sol = sol
            best_total_colors = total_colors

    print(best_total_colors)
    print(*best_sol)