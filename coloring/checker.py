import sys

def check_coloring(n, m, edges, colors, total_colors):
    used_colors = set(colors)
    actual_colors = len(used_colors)
    if actual_colors != total_colors:
        return False, actual_colors

    for u, v in edges:
        if colors[u] == colors[v]:
            return False, actual_colors

    return True, actual_colors


def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines if line.strip()]

    if not lines:
        return None, None, None

    n, m = map(int, lines[0].split())
    edges = []

    for i in range(1, min(m + 1, len(lines))):
        u, v = map(int, lines[i].split())
        edges.append((u, v))

    return n, m, edges


def main():

    output_lines = sys.stdin.read().strip().split('\n')
    total_colors = int(output_lines[0].strip())
    colors = list(map(int, output_lines[1].strip().split()))

    input_file = sys.argv[1]

    n, m, edges = parse_input(input_file)

    is_valid, actual_colors = check_coloring(n, m, edges, colors, total_colors)

    if is_valid:
        print(total_colors)
        sys.exit(0)
    else:
        print("Actual colors", actual_colors)
        sys.exit(1)


if __name__ == "__main__":
    main()