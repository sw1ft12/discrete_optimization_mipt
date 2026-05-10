import heapq

def read_input():
    n, W = map(int, input().split())
    costs = []
    weights = []

    for i in range(n):
        c, w = map(int, input().split())
        costs.append(c)
        weights.append(w)

    return n, W, costs, weights


class Node:
    def __init__(self, level, value, weight, bound, taken_items=None):
        self.level = level
        self.cost = value
        self.weight = weight
        self.ub = bound
        self.taken_items = taken_items if taken_items is not None else []

    def __lt__(self, other):
        return self.ub > other.ub


def get_upper_bound_greedy(node, n, W, items):
    if node.weight >= W:
        return 0

    ub = node.cost
    j = node.level + 1
    total_weight = node.weight

    while j < n and total_weight + items[j][1] <= W:
        total_weight += items[j][1]
        ub += items[j][0]
        j += 1

    if j < n:
        ub += (W - total_weight) * items[j][0] / items[j][1]

    return ub


def branch_and_bound(n, W, costs, weights):
    items = list(zip(costs, weights, range(n)))

    items.sort(key=lambda x: x[0] / x[1], reverse=True)

    queue = []
    root = Node(-1, 0, 0, 0, [])
    root.ub = get_upper_bound_greedy(root, n, W, items)
    heapq.heappush(queue, root)

    max_total_cost = 0
    best_taken_items = []

    while queue:
        node = heapq.heappop(queue)

        if node.ub <= max_total_cost:
            continue

        level = node.level + 1
        if level >= n:
            continue

        new_weight = node.weight + items[level][1]
        new_cost = node.cost + items[level][0]
        new_taken = node.taken_items + [items[level][2]]

        if new_weight <= W:
            if new_cost > max_total_cost:
                max_total_cost = new_cost
                best_taken_items = new_taken.copy()

            node0 = Node(level, new_cost, new_weight, 0, new_taken)
            node0.ub = get_upper_bound_greedy(node0, n, W, items)

            if node0.ub > max_total_cost:
                heapq.heappush(queue, node0)

        node1 = Node(level, node.cost, node.weight, 0, node.taken_items.copy())
        node1.ub = get_upper_bound_greedy(node1, n, W, items)

        if node1.ub > max_total_cost:
            heapq.heappush(queue, node1)

    return max_total_cost, best_taken_items


if __name__ == "__main__":
    n, W, costs, weights = read_input()
    max_cost, taken_items = branch_and_bound(n, W, costs, weights)

    print(max_cost)
    print(*taken_items)