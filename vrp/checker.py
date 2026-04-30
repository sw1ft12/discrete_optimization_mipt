import sys
import math

def read_input(filename):
    with open(filename) as f:
        n, v, c = map(int, f.readline().split())
        data = []
        for _ in range(n):
            d, x, y = map(float, f.readline().split())
            data.append((d, x, y))
    return n, v, c, data

def dist(x, y):
    return math.hypot(x[0] - y[0], x[1] - y[1])

def main():
    n, v, с, data = read_input(sys.argv[1])

    lines = sys.stdin.read().strip().splitlines()

    total_dist = float(lines[0])
    lines = lines[1:]

    if len(lines) > v:
        print("number of available couriers exceeded")
        sys.exit(1)

    used = set()
    expected_total_dist = 0

    start = (0, 0)

    for line in lines:
        if not line.strip():
            continue

        route = list(map(int, line.split()))

        for x in route:
            if x in used:
                print("client visited twice")
                sys.exit(1)
            used.add(x)

        load = sum(data[i][0] for i in route)
        if load > с:
            print("capacity exceeded")
            sys.exit(1)

        prev = start
        for i in route:
            next = (data[i][1], data[i][2])
            expected_total_dist += dist(prev, next)
            prev = next

        expected_total_dist += dist(prev, start)

    expected_total_dist = math.ceil(expected_total_dist)

    expected = set(range(n))
    if used != expected:
        print("some clients missing")
        sys.exit(1)

    if abs(expected_total_dist - total_dist) >= 1:
        print("expected dist is not equal dist:", expected_total_dist, total_dist)
        sys.exit(1)

    print(total_dist)


if __name__ == "__main__":
    main()