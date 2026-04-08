import math
import sys


def read_input(filename):
    with open(filename) as f:
        n = int(f.readline())
        coords = []
        for _ in range(n):
            line = f.readline().strip()
            parts = line.split()
            x = float(parts[0])
            y = float(parts[1])
            coords.append((x, y))
    return n, coords

def dist(i, j, coords):
    dx = coords[i][0] - coords[j][0]
    dy = coords[i][1] - coords[j][1]
    return math.hypot(dx, dy)

def total_distance(tour, coords):
    n = len(tour)
    total_dist = 0
    for i in range(n):
        total_dist += dist(tour[i], tour[(i + 1) % n], coords)
    return total_dist


def main():
    output_lines = sys.stdin.read().strip().split('\n')

    if len(output_lines) < 2:
        print("ERROR: Invalid output format", file=sys.stderr)
        sys.exit(1)

    try:
        reported_cost = float(output_lines[0].strip())
        tour = list(map(int, output_lines[1].strip().split()))
    except ValueError as e:
        print(f"ERROR: Cannot parse output: {e}", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) != 2:
        print("ERROR: Usage: python3 checker.py <test_file>", file=sys.stderr)
        sys.exit(1)

    n, coords = read_input(sys.argv[1])

    if n != len(tour):
        print(f"ERROR: Wrong length: expected {n}, got {len(tour)}", file=sys.stderr)
        sys.exit(1)

    if n != len(set(tour)):
        print("ERROR: Duplicate vertices", file=sys.stderr)
        sys.exit(1)

    if any(i < 0 or i >= n for i in tour):
        print("ERROR: Index out of range", file=sys.stderr)
        sys.exit(1)

    actual_cost = total_distance(tour, coords)

    if abs(actual_cost - reported_cost) > 0.01:
        print(f"WARNING: Cost mismatch: reported={reported_cost:.2f}, actual={actual_cost:.2f}", file=sys.stderr)

    print(f"{actual_cost:.2f}")

    sys.exit(0)


if __name__ == "__main__":
    main()