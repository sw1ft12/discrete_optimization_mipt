# # import heapq
# # import math
# # import sys
# # from scipy.optimize import linprog as lp
# #
# #
# # class Node:
# #     def __init__(self, level, cost, covered, bound):
# #         self.level = level
# #         self.cost = cost
# #         self.covered = covered
# #         self.lb = bound
# #
# #     def __lt__(self, other):
# #         return self.lb > other.lb
# #
# # def greedy_set_cover(n, m, costs, sets):
# #     uncovered = set(range(n))
# #
# #     chosen_sets = set()
# #
# #     covered = [False] * n
# #
# #     total_cost = 0
# #
# #     while uncovered:
# #         best_set = -1
# #         best_set_cost = 1
# #         new_elements_covered = 0
# #
# #         for i in range(m):
# #             if i in chosen_sets:
# #                 continue
# #
# #             new_elements = 0
# #             for elem in sets[i]:
# #                 if not covered[elem]:
# #                     new_elements += 1
# #
# #             if new_elements > 0:
# #                 if best_set == -1 or costs[i] * new_elements_covered < best_set_cost * new_elements:
# #                     new_elements_covered = new_elements
# #                     best_set_cost = costs[i]
# #                     best_set = i
# #
# #         if best_set == -1:
# #             break
# #
# #         chosen_sets.add(best_set)
# #         total_cost += sets[best_set].cost
# #
# #         for elem in sets[best_set].elements:
# #             if not covered[elem]:
# #                 covered[elem] = True
# #                 uncovered.remove(elem)
# #
# #     return total_cost
# #
# #
# # def branch_and_bound(n, m, costs, sets):
# #     items = list(zip(costs, sets))
# #
# #     items.sort(key=lambda x: x[0] / len(x[1]))
# #
# #     queue = []
# #     root = Node(-1, 0, 0, 0)
# #     root.lb = greedy_set_cover(n, m, costs, sets)
# #     heapq.heappush(queue, root)
# #
# #     max_total_cost = math.inf
# #
# #     while queue:
# #         node = heapq.heappop(queue)
# #
# #         if node.bound <= max_total_cost:
# #             continue
# #
# #         level = node.level + 1
# #         if level >= n:
# #             continue
# #
# #         new_covered = node.covered | sets[level]
# #         new_cost = node.cost + costs[level]
# #
# #         lb = lp()
# #
# #         # if new_weight <= W and new_costs < max_total_cost:
# #         #     max_total_cost = new_value
# #
# #         node0 = Node(level, new_cost, new_covered, 0)
# #         node0.lb = greedy_set_cover(node0, n, W, items)
# #
# #         if node0.lb > max_total_cost:
# #             heapq.heappush(queue, node0)
# #
# #         node1 = Node(level, node.value, node.weight, 0)
# #         node1.lb = get_lower_bound_greedy(node1, n, W, items)
# #
# #         if node1.lb > max_total_cost:
# #             heapq.heappush(queue, node1)
# #
# #     return max_total_cost
# #
# # def main():
# #     input_data = sys.stdin.read().strip().split('\n')
# #
# #     n, m = map(int, input_data[0].split())
# #
# #     costs = []
# #     sets = []
# #
# #     for i in range(1, m + 1):
# #         parts = list(map(int, input_data[i].split()))
# #         costs.append(parts[0])
# #         sets.append(parts[1:])
# #
# #     result = greedy_set_cover(n, sets)
# #     print(result)
# #
# # if __name__ == "__main__":
# #     main()
#
#
# def greedy_bound(uncovered, sets):
#     """
#     Оценка снизу: сколько минимум множеств нужно,
#     чтобы покрыть uncovered (жадная оценка)
#     """
#     uncovered = uncovered.copy()
#     count = 0
#
#     while uncovered:
#         best_cover = set()
#         for s in sets:
#             cover = uncovered & s
#             if len(cover) > len(best_cover):
#                 best_cover = cover
#
#         if not best_cover:
#             return float('inf')  # невозможно покрыть
#
#         uncovered -= best_cover
#         count += 1
#
#     return count
#
#
# def branch_and_bound_setcover(universe, sets):
#     m = len(sets)
#     best_solution = float('inf')
#
#     def backtrack(index, chosen_count, covered):
#         nonlocal best_solution
#
#         # если уже хуже лучшего решения — отсечение
#         if chosen_count >= best_solution:
#             return
#
#         # если всё покрыто
#         if covered == universe:
#             best_solution = chosen_count
#             return
#
#         # если множества закончились
#         if index == m:
#             return
#
#         # оценка снизу
#         uncovered = universe - covered
#         lb = greedy_bound(uncovered, sets[index:])
#         if chosen_count + lb >= best_solution:
#             return
#
#         # 1️⃣ Берём текущее множество
#         backtrack(
#             index + 1,
#             chosen_count + 1,
#             covered | sets[index]
#         )
#
#         # 2️⃣ Не берём текущее множество
#         backtrack(
#             index + 1,
#             chosen_count,
#             covered
#         )
#
#     backtrack(0, 0, set())
#     return best_solution
#
#
# # ===== Ввод =====
# if __name__ == "__main__":
#     n, m = map(int, input().split())
#     universe = set(range(n))
#     sets = []
#
#     for _ in range(m):
#         data = list(map(int, input().split()))
#         k = data[0]
#         subset = set(data[1:])
#         sets.append(subset)
#
#     result = branch_and_bound_setcover(universe, sets)
#
#     if result == float('inf'):
#         print("Нет покрытия")
#     else:
#         print(result)


import numpy as np
from scipy.optimize import linprog


def solve_lp(n, m, costs, sets, fixed):
    c = np.array(costs)

    A = np.zeros((n, m))
    b = -np.ones(n)

    for e in range(n):
        for i in range(m):
            if e in sets[i]:
                A[e, i] = -1

    bounds = []
    for i in range(m):
        if i in fixed:
            bounds.append((fixed[i], fixed[i]))
        else:
            bounds.append((0, 1))

    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

    return res.fun, res.x


def branch_and_bound(n, m, costs, sets):
    ub = 30
    lb = 0
    best_solution = []

    queue = [{}]
    while queue:
        fixed = queue.pop()
        lp_val, x = solve_lp(n, m, costs, sets, fixed)

        if lp_val >= ub or lb >= lp_val:
            continue

        fractional = None
        for i, val in enumerate(x):
            if abs(val - round(val)) > 1e-6:
                fractional = i
                break

        if fractional is None:
            ub = lp_val
            best_solution = x
            continue

        fixed1 = fixed.copy()
        fixed1[fractional] = 1
        queue.append(fixed1)

        fixed0 = fixed.copy()
        fixed0[fractional] = 0
        queue.append(fixed0)

    # def bb(fixed):
    #     nonlocal ub, best_solution
    #
    #     lp_val, x = solve_lp(n, m, costs, sets, fixed)
    #
    #     if x is None:
    #         return
    #
    #     if lp_val >= ub:
    #         return
    #
    #     fractional = None
    #     for i, val in enumerate(x):
    #         if abs(val - round(val)) > 1e-6:
    #             fractional = i
    #             break
    #
    #     if fractional is None:
    #         ub = lp_val
    #         best_solution = x
    #         return
    #
    #     fixed1 = fixed.copy()
    #     fixed1[fractional] = 1
    #     bb(fixed1)
    #
    #     fixed0 = fixed.copy()
    #     fixed0[fractional] = 0
    #     bb(fixed0)

    # bb({})

    return ub, best_solution


if __name__ == "__main__":
    n, m = map(int, input().split())

    costs = []
    sets = []

    for _ in range(m):
        data = list(map(int, input().split()))
        c_i = data[0]
        subset = set(data[1:])
        costs.append(c_i)
        sets.append(subset)

    value, solution = branch_and_bound(n, m, costs, sets)

    print("Минимальная стоимость:", int(round(value)))
    print("Выбранные множества (индексы):")
    for i, v in enumerate(solution):
        if round(v) == 1:
            print(i)