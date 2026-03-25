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

    return total_colors, color


if __name__ == "__main__":
    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    colors_count, coloring = dSatur(n, graph)
    print(colors_count)

    print(*coloring, sep=' ')