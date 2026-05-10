import random

def read_input():
    n, W = map(int, input().split())
    costs = []
    weights = []

    for i in range(n):
        c, w = map(int, input().split())
        costs.append(c)
        weights.append(w)

    return n, W, costs, weights


def knapsack_greedy_density(n, W, costs, weights):
    items = [(i, costs[i], weights[i], costs[i] / weights[i])
             for i in range(n)]
    items.sort(key=lambda x: -x[3])

    total_weight = 0
    total_cost = 0
    taken = [0] * n

    for i, c, w, _ in items:
        if total_weight + w <= W:
            taken[i] = 1
            total_weight += w
            total_cost += c

    return total_cost, [i for i in range(n) if taken[i]]


def knapsack_greedy_cost(n, W, costs, weights):
    items = [(i, costs[i], weights[i]) for i in range(n)]
    items.sort(key=lambda x: -x[1])

    total_weight = 0
    total_cost = 0
    taken = [0] * n

    for i, c, w in items:
        if total_weight + w <= W:
            taken[i] = 1
            total_weight += w
            total_cost += c

    return total_cost, [i for i in range(n) if taken[i]]

def knapsack_greedy_light(n, W, costs, weights):
    items = [(i, costs[i], weights[i]) for i in range(n)]
    items.sort(key=lambda x: x[2])

    total_weight = 0
    total_cost = 0
    taken = [0] * n

    for i, c, w in items:
        if total_weight + w <= W:
            taken[i] = 1
            total_weight += w
            total_cost += c

    return total_cost, [i for i in range(n) if taken[i]]

def random_shuffle(n, W, costs, weights, best_cost):
    best_taken = []

    for _ in range(100):
        idxs = list(range(n))
        random.shuffle(idxs)
        total_weight = 0
        total_cost = 0
        taken = [0] * n
        for i in idxs:
            if total_weight + weights[i] <= W:
                taken[i] = 1
                total_weight += weights[i]
                total_cost += costs[i]
        if total_cost > best_cost:
            best_cost = total_cost
            best_taken = [i for i in range(n) if taken[i]]

    return best_cost, best_taken


def knapsack_greedy_all(n, W, costs, weights):
    best_cost = 0
    best_taken = []

    cost1, taken1 = knapsack_greedy_density(n, W, costs, weights)
    if cost1 > best_cost:
        best_cost = cost1
        best_taken = taken1

    cost2, taken2 = knapsack_greedy_cost(n, W, costs, weights)
    if cost2 > best_cost:
        best_cost = cost2
        best_taken = taken2

    cost3, taken3 = knapsack_greedy_light(n, W, costs, weights)
    if cost3 > best_cost:
        best_cost = cost3
        best_taken = taken3

    cost4, taken4 = random_shuffle(n, W, costs, weights, best_cost)
    if cost4 > best_cost:
        best_cost = cost4
        best_taken = taken4

    return best_cost, best_taken


if __name__ == "__main__":
    n, W, costs, weights = read_input()
    cost, taken = knapsack_greedy_all(n, W, costs, weights)

    print(cost)
    print(*taken)
