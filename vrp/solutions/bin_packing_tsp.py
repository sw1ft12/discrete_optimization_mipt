import sys
import math

def read_input(filename):
    with open(filename) as f:
        n, v, c = map(int, f.readline().split())
        data = []
        for _ in range(n):
            d, x, y = map(float, f.readline().split())
            data.append((d, x, y))
    return n, v, c, data


def dist(x, y):
    return math.hypot(x[0] - y[0], x[1] - y[1])

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

def tsp_nn(route, data):
    unvisited = set(route)
    path = []

    current = (0,0)

    while unvisited:
        best_neighbour = None
        best_dist = float("inf")

        for i in unvisited:
            neighbour = (data[i][1], data[i][2])
            d = dist(current, neighbour)

            if d < best_dist:
                best_dist = d
                best_neighbour = i

        path.append(best_neighbour)
        current = (data[best_neighbour][1], data[best_neighbour][2])
        unvisited.remove(best_neighbour)

    return path


def routes_dist(routes, data):
    start = (0, 0)
    total = 0
    for r in routes:
        prev = start
        for i in r:
            next = (data[i][1], data[i][2])
            total += dist(prev, next)
            prev = next

        total += dist(prev, start)

    return total


def solve(n, v, c, data):
    best_routes = []
    best_cost = float("inf")

    routes = bin_packing(n, v, c, data)

    curr_routes = []
    for r in routes:
        curr_routes.append(tsp_nn(r, data))

    cost = routes_dist(curr_routes, data)
    if cost < best_cost:
        best_cost = cost
        best_routes = curr_routes

    return best_routes, best_cost

if __name__ == "__main__":
    filename = sys.argv[1]
    n, v, c, data = read_input(filename)

    routes, total_dist = solve(n, v, c, data)

    print(math.ceil(total_dist))
    for r in routes:
        print(*r)
