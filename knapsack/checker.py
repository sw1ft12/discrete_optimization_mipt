import sys

def read_test_file(filename):
    items = []
    with open(filename, 'r') as f:
        first_line = f.readline().strip()
        while first_line and first_line.startswith('#'):
            first_line = f.readline().strip()

        n, capacity = map(int, first_line.split())

        for _ in range(n):
            line = f.readline().strip()
            while line and line.startswith('#'):
                line = f.readline().strip()
            if not line:
                continue
            cost, weight = map(int, line.split())
            items.append((cost, weight))

    return n, capacity, items


def read_solution():
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            lines.append(line)

    if not lines:
        return None, []

    total_cost = int(lines[0])

    items = []
    for line in lines[1:]:
        for num in line.split():
            try:
                items.append(int(num))
            except ValueError:
                pass

    return total_cost, items


def check_solution(n, capacity, items, solution_cost, solution_items):
    if len(solution_items) != len(set(solution_items)):
        return False

    total_weight = 0
    total_cost = 0
    for idx in solution_items:
        cost, weight = items[idx]
        total_weight += weight
        total_cost += cost


    if total_weight > capacity:
        return False

    if total_cost != solution_cost:
        return False

    return True

if __name__ == "__main__":
    filename = sys.argv[1]
    n, capacity, items = read_test_file(filename)
    solution_cost, solution_items = read_solution()

    if not check_solution(n, capacity, items, solution_cost, solution_items):
        sys.exit(1)

    print(solution_cost)