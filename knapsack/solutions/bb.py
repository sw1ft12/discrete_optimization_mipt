import heapq

class Node:
    def __init__(self, level, value, weight, bound):
        self.level = level
        self.cost = value
        self.weight = weight
        self.lb = bound

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
    items = list(zip(values, weights))

    items.sort(key=lambda x: x[0] / x[1], reverse=True)

    queue = []
    root = Node(-1, 0, 0, 0)
    root.lb = get_lower_bound_greedy(root, n, W, items)
    heapq.heappush(queue, root)

    max_total_cost = 0

    while queue:
        node = heapq.heappop(queue)

        if node.bound <= max_total_cost:
            continue

        level = node.level + 1
        if level >= n:
            continue

        new_weight = node.weight + items[level][1]
        new_value = node.value + items[level][0]

        if new_weight <= W and new_value > max_total_cost:
            max_total_cost = new_value

        node0 = Node(level, new_value, new_weight, 0)
        node0.lb = get_lower_bound_greedy(node0, n, W, items)

        if node0.lb > max_total_cost:
            heapq.heappush(queue, node0)

        node1 = Node(level, node.value, node.weight, 0)
        node1.lb = get_lower_bound_greedy(node1, n, W, items)

        if node1.lb > max_total_cost:
            heapq.heappush(queue, node1)

    return max_total_cost

if __name__ == "__main__":
    n, W = map(int, input().split())
    values = []
    weights = []

    for _ in range(n):
        c, w = map(int, input().split())
        values.append(c)
        weights.append(w)

    print(branch_and_bound(n, W, values, weights))