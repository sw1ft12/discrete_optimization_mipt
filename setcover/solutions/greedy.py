import sys

def read_input(filename):
    with open(filename) as f:
        n, m = map(int, f.readline().split())
        costs = []
        sets = []
        for _ in range(m):
            data = list(map(int, f.readline().split()))
            costs.append(data[0])
            sets.append(set(data[1:]))
    return n, m, costs, sets


def greedy(n, m, sets, costs):
    uncovered = set(range(n))
    chosen_sets = set()
    covered = [False] * n

    total_cost = 0

    while uncovered:
        best_set = -1
        best_set_cost = 1
        new_elements_covered = 0

        for i in range(m):
            if i in chosen_sets:
                continue

            new_elements = 0
            for elem in sets[i]:
                if not covered[elem]:
                    new_elements += 1

            if new_elements > 0:
                if best_set == -1 or costs[i] * new_elements_covered < best_set_cost * new_elements:
                    new_elements_covered = new_elements
                    best_set_cost = costs[i]
                    best_set = i

        if best_set == -1:
            break

        chosen_sets.add(best_set)
        total_cost += costs[best_set]

        for elem in sets[best_set]:
            if not covered[elem]:
                covered[elem] = True
                uncovered.remove(elem)

    return total_cost, chosen_sets


if __name__ == "__main__":
    filename = sys.argv[1]
    n, m, costs, sets = read_input(filename)
    best_cost, best_solution = greedy(n, m, sets, costs)

    print(best_cost)
    print(*best_solution)