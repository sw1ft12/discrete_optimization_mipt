import sys
import math

def read_input(filename):
    with open(filename) as f:
        n = int(f.readline())
        coords = []
        for _ in range(n):
            line = f.readline().strip()
            parts = line.split()
            x = float(parts[0])
            y = float(parts[1])
            coords.append((x, y))
    return n, coords

def dist(i, j, coords):
    dx = coords[i][0] - coords[j][0]
    dy = coords[i][1] - coords[j][1]
    return math.hypot(dx, dy)

def total_distance(tour, coords):
    n = len(tour)
    total_dist = 0
    for i in range(n):
        total_dist += dist(tour[i], tour[(i + 1) % n], coords)
    return total_dist

def nn_backtracking(coords, m=10, k=3, max_depth=5):
    n = len(coords)
    best_tour = []
    best_cost = float('inf')

    def backtrack(tour, visited, depth):
        nonlocal best_tour, best_cost

        if len(tour) == n:
            cost = total_distance(tour, coords)
            if cost < best_cost:
                best_cost = cost
                best_tour = tour.copy()
            return

        last = tour[-1]
        closest_neighbours = []
        for i in range(n):
            if not visited[i]:
                closest_neighbours.append((dist(last, i, coords), i))

        closest_neighbours.sort()

        if depth >= max_depth:
            best = closest_neighbours[0][1]
            tour.append(best)
            visited[best] = True
            backtrack(tour, visited, depth + 1)
            visited[best] = False
            tour.pop()
            return

        for d, i in closest_neighbours[:min(k, len(closest_neighbours))]:
            tour.append(i)
            visited[i] = True
            backtrack(tour, visited, depth + 1)
            visited[i] = False
            tour.pop()

    for start in range(min(m, n)):
        tour = [start]
        used = [False] * n
        used[start] = True
        backtrack(tour, used, 0)

    return best_tour, best_cost

def main():
    n, coords = read_input(sys.argv[1])

    tour, cost = [], float("inf")

    if n < 60:
        tour, cost = nn_backtracking(coords, 10, 5, 7)
    elif n < 150:
        tour, cost = nn_backtracking(coords,10, 5, 5)
    elif n < 500:
        tour, cost = nn_backtracking(coords, 10, 3, 5)
    elif n < 5000:
        tour, cost = nn_backtracking(coords, 5, 5, 2)
    else:
        tour, cost = nn_backtracking(coords, 1, 1, 1)

    print(int(cost))
    print(*tour)


if __name__ == "__main__":
    main()