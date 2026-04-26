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

def greedy_start(n, m, sets, costs):
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
            if len(new_cover) == n:
                del sol[i]
                changed = True
                break

    return sol, sum(costs[s] for s in sol)

def repair(n, m, sets, costs, sol):
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

    return repair(n, m, sets, costs, current_sol)

def annealing(n, m, sets, costs, T=1000, time_limit=120, k_opt=2):
    current_sol, current_cost = greedy_start(n, m, sets, costs)
    best_sol, best_cost = current_sol, current_cost
    start_time = time.time()

    no_improve = 0

    while time.time() - start_time < time_limit:
        neighbor_sol, neighbor_cost = get_neighbour(n, m, sets, costs, current_sol, k_opt)
        delta = neighbor_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / T):
            current_sol, current_cost = neighbor_sol, neighbor_cost
            if current_cost < best_cost:
                best_sol, best_cost = current_sol, current_cost

            no_improve = 0
        else:
            no_improve += 1

        if no_improve > 1000:
            T = 500
            no_improve = 0
        else:
            T *= 0.999
            if T < 1e-3:
                T = 1000

    return best_sol, best_cost

if __name__ == "__main__":
    filename = sys.argv[1]
    n, m, costs, sets = read_input(filename)

    best_sol, best_cost = [], float("inf")

    for i in range(3):
        sol, cost = annealing(n, m, sets, costs, time_limit=90, k_opt=3)
        if cost < best_cost:
            best_sol = sol
            best_cost = cost

    print(best_cost)
    print(*best_sol)