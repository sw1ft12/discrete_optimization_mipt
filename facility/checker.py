import math
import sys
import numpy as np

def read_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    first = lines[0].split()
    N, M = int(first[0]), int(first[1])

    stores = []
    for i in range(1, N+1):
        parts = list(map(float, lines[i].split()))
        s = parts[0]
        cap = parts[1]
        x, y = parts[2], parts[3]
        stores.append((s, cap, x, y))

    customers = []
    for j in range(N+1, N+M+1):
        parts = list(map(float, lines[j].split()))
        d = parts[0]
        x, y = parts[1], parts[2]
        customers.append((d, x, y))

    return N, M, stores, customers

def read_solution():
    output_lines = sys.stdin.read().strip().split('\n')

    cost = float(output_lines[0].strip())
    opened = list(map(int, output_lines[1].strip().split()))
    assignments = list(map(int, output_lines[2].strip().split()))

    return Solution(cost, opened, assignments)


class Solution:
    def __init__(self, cost, opened, assignments):
        self.cost = cost
        self.opened = opened
        self.assignments = assignments


def distance(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)


def check_solution(N, M, stores, customers, solution):
    opened = solution.opened
    assignments = solution.assignments

    if len(assignments) != M:
        return False, 0, f'Wrong number of assignments: expected {M}, got {len(assignments)}'

    for i in opened:
        if i < 0 or i >= N:
            return False, 0, f'Invalid store index: {i}'

    for j, i in enumerate(assignments):
        if i < 0 or i >= N:
            return False, 0, f'Invalid assignment for customer {j}: store {i}'

    open_set = set(opened)
    for j, i in enumerate(assignments):
        if i not in open_set:
            return False, 0, f'Customer {j} assigned to closed store {i}'

    remaining_capacity = {i: stores[i][1] for i in opened}
    for j, i in enumerate(assignments):
        demand = customers[j][0]
        if remaining_capacity[i] < demand - 1e-6:
            return False, 0, f'Capacity exceeded at store {i}: need {demand}, have {remaining_capacity[i]}'
        remaining_capacity[i] -= demand

    total_cost = sum(stores[i][0] for i in opened)

    for j, i in enumerate(assignments):
        dist = distance(
            stores[i][2], stores[i][3],
            customers[j][1], customers[j][2]
        )
        total_cost += dist

    if abs(total_cost - solution.cost) > 1e9:
        return False, 0, f'cost {solution.cost} is not equal expected cost {total_cost}'

    return True, total_cost, None


def main():
    solution = read_solution()
    N, M, stores, customers = read_input(sys.argv[1])
    flag, cost, err = check_solution(N, M, stores, customers, solution)
    if not flag:
        print(err)
        sys.exit(1)

    print(cost)


if __name__ == "__main__":
    main()