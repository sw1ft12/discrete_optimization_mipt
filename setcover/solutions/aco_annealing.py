import math
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

    return chosen_sets, total_cost

def get_coverage(sets, sol):
    covered = set()
    for s in sol:
        covered.update(sets[s])
    return covered

def remove_extra(n, sets, costs, sol):
    sol.sort(key=lambda x: -costs[x])
    changed = True
    while changed:
        changed = False
        for i in range(len(sol)):
            new_cover = get_coverage(sets, sol[:i] + sol[i + 1:])
            if len(new_cover) >= n:
                del sol[i]
                changed = True
                break

    return sol, sum(costs[s] for s in sol)

def repair(n, m, sol, sets, costs):
    uncovered = set(range(n)) - get_coverage(sets, sol)
    if uncovered:
        additions = []
        for i in range(m):
            if i in sol:
                continue
            gain = len(sets[i] & uncovered)
            if gain > 0:
                additions.append((costs[i] / gain, gain, i))
        additions.sort()
        idx = 0
        while uncovered:
            sol.append(additions[idx][2])
            uncovered -= sets[additions[idx][2]]
            idx += 1
    return remove_extra(n, sets, costs, sol)

def get_neighbour(n, m, sets, costs, sol, k_opt=2):
    current_sol = list(sol)
    l = len(current_sol)

    rand = random.random()

    if rand < 0.3 and l < m:
        cands = [i for i in range(m) if i not in current_sol]
        to_add = random.choice(cands)
        current_sol.append(to_add)
    elif rand < 0.5 and l > 1:
        to_remove = random.randint(0, l - 1)
        del current_sol[to_remove]
    elif rand < 0.7 and 0 < l < m:
        pos = random.randint(0, l - 1)
        to_remove = current_sol[pos]
        cands = [i for i in range(m) if i != to_remove]
        to_add = random.choice(cands)
        current_sol[pos] = to_add
    elif l >= k_opt and m - l >= k_opt:
        to_remove = sorted(random.sample(range(l), k_opt), reverse=True)
        for idx in to_remove:
            del current_sol[idx]
        cands = [i for i in range(m) if i not in current_sol]
        to_add = random.sample(cands, k_opt)
        for add in to_add:
            current_sol.append(add)

    return repair(n, m, current_sol, sets, costs)

def annealing(sets, costs, sol, cost, T=1000, time_limit=30, k_opt=2):
    current_sol, current_cost = list(sol), cost
    best_sol, best_cost = current_sol, current_cost

    start = time.time()
    no_improve = 0

    while time.time() - start < time_limit:
        neighbour_sol, neighbour_cost = get_neighbour(n, m, sets, costs, current_sol, k_opt)
        delta = neighbour_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / T):
            current_sol, current_cost = neighbour_sol, neighbour_cost
            if current_cost < best_cost:
                best_sol, best_cost = current_sol, current_cost
                no_improve = 0
            else:
                no_improve += 1
        else:
            no_improve += 1

        if no_improve > 1000:
            current_sol = list(best_sol)
            T = 500
            no_improve = 0

        T *= 0.999
        if T < 1e-3:
            T = 1000

    return best_sol, best_cost


def aco(n, m, sets, costs, time_limit=90, ants=25, rho=0.98, alpha=2.0, beta=5.0):
    elem_to_sets = [[] for _ in range(n)]
    for j, s in enumerate(sets):
        for e in s:
            elem_to_sets[e].append(j)

    greedy_sol, greedy_cost = greedy(n, m, sets, costs)

    tau_max = 1.0 / ((1 - rho) * greedy_cost)
    tau_min =  tau_max / (2 * m)

    pheromone = [tau_max] * m

    best_sol, best_cost = greedy_sol, greedy_cost
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

    no_improve = 0

    while time.time() - start < time_limit:
        for _ in range(ants):
            sol, cost = run_ant()
            sol, cost = annealing(sets, costs, sol, cost, time_limit=1)
            if cost < best_cost:
                best_sol, best_cost = sol, cost
            else:
                no_improve += 1

        for i in range(m):
            pheromone[i] *= rho

        for j in best_sol:
            pheromone[j] += 1.0 / best_cost

        for i in range(m):
            pheromone[i] = max(tau_min, min(tau_max, pheromone[i]))

    return annealing(sets, costs, best_sol, best_cost, time_limit=30)

if __name__ == "__main__":
    filename = sys.argv[1]
    n, m, costs, sets = read_input(filename)

    best_sol, best_cost = [], float("inf")
    for i in range(2):
        sol, cost = aco(n, m, sets, costs, time_limit=100)
        if cost < best_cost:
            best_sol = sol
            best_cost = cost

    print(best_cost)
    print(*best_sol)