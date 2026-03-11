import sys
import argparse


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

    print(lines)

    total_cost = int(lines[0])

    items = []
    for line in lines[1:]:
        for num in line.split():
            try:
                items.append(int(num))
            except ValueError:
                pass

    return total_cost, items


def check_solution(n, capacity, items, solution_cost, solution_items, quiet=False):
    if not quiet:
        print("=" * 60, file=sys.stderr)
        print("ПРОВЕРКА РЕШЕНИЯ ЗАДАЧИ О РЮКЗАКЕ", file=sys.stderr)
        print("=" * 60, file=sys.stderr)

        print(f"\nВходные данные:", file=sys.stderr)
        print(f"  Предметов: {n}", file=sys.stderr)
        print(f"  Вместимость: {capacity}", file=sys.stderr)

    if len(solution_items) != len(set(solution_items)):
        print("❌ Ошибка: Обнаружены дубликаты предметов", file=sys.stderr)
        return False

    total_weight = 0
    total_cost = 0
    for idx in solution_items:
        cost, weight = items[idx]
        total_weight += weight
        total_cost += cost

    if not quiet:
        print(f"\nРешение:", file=sys.stderr)
        print(f"  Заявленная стоимость: {solution_cost}", file=sys.stderr)
        print(f"  Предметы: {solution_items}", file=sys.stderr)
        print(f"\nПроверка:", file=sys.stderr)
        print(f"  Фактическая стоимость: {total_cost}", file=sys.stderr)
        print(f"  Фактический вес: {total_weight}/{capacity}", file=sys.stderr)

    if total_weight > capacity:
        print(f"❌ Ошибка: Превышена вместимость рюкзака!", file=sys.stderr)
        return False

    if total_cost != solution_cost:
        print(f"❌ Ошибка: Несоответствие стоимости!", file=sys.stderr)
        print(f"  Заявлено: {solution_cost}, Фактически: {total_cost}", file=sys.stderr)
        return False

    if not quiet:
        print(f"\n✅ Решение верно!", file=sys.stderr)
        print(f"  Стоимость: {solution_cost}, Вес: {total_weight}/{capacity}", file=sys.stderr)

    return True


def main():
    parser = argparse.ArgumentParser(description='Чекер для задачи о рюкзаке')
    parser.add_argument('test_file', help='Файл с тестовыми данными')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Тихий режим (выводить только стоимость при успехе)')

    args = parser.parse_args()

    n, capacity, items = read_test_file(args.test_file)

    solution_cost, solution_items = read_solution()

    if check_solution(n, capacity, items, solution_cost, solution_items, args.quiet):
        if args.quiet:
            print(solution_cost)
        else:
            print(f"\n✅ Проверка пройдена", file=sys.stderr)
        sys.exit(0)
    else:
        if args.quiet:
            print("FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()