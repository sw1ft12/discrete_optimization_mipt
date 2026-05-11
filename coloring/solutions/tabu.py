import random
import time
import sys

def read_input(filename):
    with open(filename) as f:
        n, m = map(int, f.readline().split())
        graph = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, f.readline().split())
            graph[u].append(v)
            graph[v].append(u)

    return n, m, graph

def dSatur(n, graph):
    color = [-1] * n
    saturation = [0] * n

    degree = [len(graph[i]) for i in range(n)]

    total_colors = 0

    while True:
        selected = -1
        max_sat = -1
        max_deg = -1

        for u in range(n):
            if color[u] == -1:
                if saturation[u] > max_sat:
                    max_sat = saturation[u]
                    max_deg = degree[u]
                    selected = u
                elif saturation[u] == max_sat and degree[u] > max_deg:
                    max_deg = degree[u]
                    selected = u

        if selected == -1:
            break

        used_colors = set()
        for v in graph[selected]:
            if color[v] != -1:
                used_colors.add(color[v])

        free_color = 0

        while free_color in used_colors:
            free_color += 1

        color[selected] = free_color
        total_colors = max(total_colors, free_color + 1)

        for v in graph[selected]:
            if color[v] == -1:
                neighbor_colors = set()
                for w in graph[v]:
                    if color[w] != -1:
                        neighbor_colors.add(color[w])
                saturation[v] = len(neighbor_colors)

    return color, total_colors

def count_conflicts(n, graph, colors):
    total_conflicts = 0
    conflicts = [0] * n
    for v in range(n):
        cv = colors[v]
        cnt = 0
        for u in graph[v]:
            if colors[u] == cv:
                cnt += 1
        conflicts[v] = cnt
        total_conflicts += cnt

    return total_conflicts, conflicts

def tabu_k_coloring(n, m, graph, ub_coloring, k, time_limit=90, tenure=5):
    coloring = [c % k for c in ub_coloring]

    tabu_until = [[0]*k for _ in range(n)]

    total_conflicts, conflicts = count_conflicts(n, graph, coloring)

    total_conflicts //= 2

    if total_conflicts == 0:
        return True, coloring

    start = time.time()
    it = 1
    best_total_conflicts = total_conflicts
    best_coloring = coloring[:]

    while time.time() - start < time_limit:
        conflict_vertices = [v for v in range(n) if conflicts[v] > 0]
        if not conflict_vertices:
            return True, coloring
        v = random.choice(conflict_vertices)

        old_color = coloring[v]

        new_color = (old_color + 1 + random.randrange(k-1)) % k
        best_conflicts_delta = 10**9

        for col in range(k):
            if col == old_color:
                continue
            if tabu_until[v][col] > it:
                continue

            new_conf = 0
            for u in graph[v]:
                if coloring[u] == col:
                    new_conf += 1

            conflicts_delta = new_conf - conflicts[v]
            if conflicts_delta < best_conflicts_delta:
                best_conflicts_delta = conflicts_delta
                new_color = col

        conflicts[v] = 0
        for u in graph[v]:
            if coloring[u] == old_color:
                conflicts[u] -= 1
                total_conflicts -= 1
            elif coloring[u] == new_color:
                conflicts[u] += 1
                conflicts[v] += 1
                total_conflicts += 1

        coloring[v] = new_color

        tabu_until[v][old_color] = it + tenure + random.randrange(5)

        if total_conflicts < best_total_conflicts:
            best_total_conflicts = total_conflicts
            best_coloring = coloring[:]
            if best_total_conflicts == 0:
                return True, best_coloring

        it += 1

    return (best_total_conflicts == 0), best_coloring

def tabu_search(n, m, graph, time_limit=90):
    best_coloring, best_max_color = dSatur(n, graph)

    k = best_max_color - 1
    start = time.time()

    while time.time() - start < time_limit:
        time_limit_per_try = 10
        ok = False
        best_k_coloring = []

        for _ in range(10):
            ok, coloring = tabu_k_coloring(n, m, graph, best_coloring, k, time_limit_per_try, tenure=10)
            if ok:
                best_k_coloring = coloring
                break
        if ok:
            best_max_color = k
            best_coloring = best_k_coloring
            k -= 1
        else:
            break

    return best_coloring, best_max_color

if __name__ == "__main__":
    filename = sys.argv[1]
    n, m, graph = read_input(filename)

    best_coloring, best_max_color = tabu_search(n, m, graph, time_limit=90)

    print(best_max_color)
    print(*best_coloring)