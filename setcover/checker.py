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


def read_solution():
    output_lines = sys.stdin.read().strip().split('\n')

    cost = float(output_lines[0].strip())
    sets = list(map(int, output_lines[1].strip().split()))

    return cost, sets

def check():
    n, m, costs, sets = read_input(sys.argv[1])

    cost, chosen_sets = read_solution()

    covered = [False] * n
    expected_cost = 0
    for i in chosen_sets:
        expected_cost += costs[i]
        for j in sets[i]:
            covered[j] = True

    if expected_cost != cost:
        print("cost is not equal expected cost:", )
        return False, 0

    for i in range(n):
        if not covered[i]:
            print("not all elements are covered")
            return False, 0
    return True, expected_cost


if __name__ == "__main__":
    flag, cost = check()
    if not flag:
        sys.exit(1)

    print(cost)
