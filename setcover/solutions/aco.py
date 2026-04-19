import random, time, sys

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

def aco(n, m, sets, costs, time_limit=90, ants=25, rho=0.98, alpha=2.0, beta=5.0):
    elem_to_sets = [[] for _ in range(n)]
    for j, s in enumerate(sets):
        for e in s:
            elem_to_sets[e].append(j)

    greedy_cost, _ = greedy(n, m, sets, costs)

    tau_max = 1.0 / ((1 - rho) * greedy_cost)
    tau_min =  tau_max / (2 * m)

    pheromone = [tau_max] * m
    best_solution, best_cost = [], float('inf')
    start = time.time()

    def h(covered, col):
        return len(sets[col] - covered) / costs[col]

    def run_ant():
        covered, sol = set(), []
        total_cost = 0

        while len(covered) < n:
            elem = random.choice([e for e in range(n) if e not in covered])
            cands = elem_to_sets[elem]

            if not cands:
                continue

            probs = [pheromone[i]**alpha * (h(covered, i) ** beta) for i in cands]
            total = sum(probs)

            chosen_set = 0
            if total == 0:
                chosen_set = random.choice(cands)
            else:
                r = random.random() * total
                s = 0
                for idx, j in enumerate(cands):
                    s += probs[idx]
                    if s >= r:
                        chosen_set = j
                        break

            total_cost += costs[chosen_set]
            sol.append(chosen_set)
            covered |= sets[chosen_set]

        return sol, total_cost

    while time.time() - start < time_limit:
        for _ in range(ants):
            sol, cost = run_ant()
            if cost < best_cost:
                best_cost, best_solution = cost, sol

        for i in range(m):
            pheromone[i] *= rho

        for j in best_solution:
            pheromone[j] += 1.0 / best_cost

        for i in range(m):
            pheromone[i] = max(tau_min, min(tau_max, pheromone[i]))

    return best_cost, best_solution

if __name__ == "__main__":
    filename = sys.argv[1]
    n, m, costs, sets = read_input(filename)
    best_cost, best_solution = aco(n, m, sets, costs)

    print(best_cost)
    print(*best_solution)
