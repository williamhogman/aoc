import itertools
import re

nums = re.compile("\d+")


def line_acceptable(line, part2=True):
    x1, y1 = line[0]
    x2, y2 = line[1]

    if x1 == x2:
        return True
    if y1 == y2:
        return True

    # is diagonal
    if abs(x1 - x2) == abs(y1 - y2):
        return part2

    return False


def parse_row(row):
    # format: 432,708 -> 432,160
    n = nums.findall(row)
    assert len(n) == 4

    return ((int(n[0]), int(n[1])), (int(n[2]), int(n[3])))


data = [parse_row(x) for x in open("ex5.txt")]


import collections


def points_on_line(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    for i in range(max(abs(x1 - x2), abs(y1 - y2))):
        dx = i if x1 < x2 else -i
        dy = i if y1 < y2 else -i
        yield (x1 + dx, y1 + dy)

    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            yield (x1, y)
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            yield (x, y1)
    elif abs(x1 - x2) == abs(y1 - y2):
        dx = 1 if x1 < x2 else -1
        dy = 1 if y1 < y2 else -1
        for x, y in zip(range(x1, x2 + dx, dx), range(y1, y2 + dy, dy)):
            yield (x, y)
    else:
        assert False


assert list(points_on_line((1, 1), (1, 3))) == [(1, 1), (1, 2), (1, 3)]
assert list(points_on_line((1, 1), (1, 3))) == [(1, 1), (1, 2), (1, 3)]
assert list(points_on_line((9, 7), (7, 9))) == [(9, 7), (8, 8), (7, 9)]


def make_grid(lines):
    c = collections.Counter()
    to_add = itertools.chain.from_iterable(points_on_line(*line) for line in lines)
    c.update(to_add)
    return c


def count_points_occuring_twice(c):
    return sum(1 for k in c if c[k] >= 2)


def solve(part):
    acceptable_lines = [line for line in data if line_acceptable(line, part2=part == 2)]
    c = make_grid(acceptable_lines)
    return count_points_occuring_twice(c)


def main():
    print(solve(1))
    print(solve(2))


main()
