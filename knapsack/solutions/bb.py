import heapq

class Node:
    def __init__(self, level, value, weight, bound, taken_items=None):
        self.level = level
        self.cost = value
        self.weight = weight
        self.lb = bound
        self.taken_items = taken_items if taken_items is not None else []

    def __lt__(self, other):
        return self.lb > other.lb


def get_lower_bound_greedy(node, n, W, items):
    if node.weight >= W:
        return 0

    lb = node.cost
    j = node.level + 1
    total_weight = node.weight

    while j < n and total_weight + items[j][1] <= W:
        total_weight += items[j][1]
        lb += items[j][0]
        j += 1

    if j < n:
        lb += (W - total_weight) * items[j][0] / items[j][1]

    return lb


def branch_and_bound(n, W, values, weights):
    items = list(zip(values, weights, range(n)))

    items.sort(key=lambda x: x[0] / x[1], reverse=True)

    queue = []
    root = Node(-1, 0, 0, 0, [])
    root.lb = get_lower_bound_greedy(root, n, W, items)
    heapq.heappush(queue, root)

    max_total_cost = 0
    best_taken_items = []

    while queue:
        node = heapq.heappop(queue)

        if node.lb <= max_total_cost:
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
            node0.lb = get_lower_bound_greedy(node0, n, W, items)

            if node0.lb > max_total_cost:
                heapq.heappush(queue, node0)

        node1 = Node(level, node.cost, node.weight, 0, node.taken_items.copy())
        node1.lb = get_lower_bound_greedy(node1, n, W, items)

        if node1.lb > max_total_cost:
            heapq.heappush(queue, node1)

    return max_total_cost, best_taken_items


if __name__ == "__main__":
    n, W = map(int, input().split())
    values = []
    weights = []

    for i in range(n):
        c, w = map(int, input().split())
        values.append(c)
        weights.append(w)

    max_cost, taken_items = branch_and_bound(n, W, values, weights)

    print(max_cost)

    print(*taken_items, sep=" ")