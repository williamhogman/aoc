data = list(map(int, open("ex7.txt").read().strip().split(",")))


def solve(score_fn):
    deltas = {}

    for i in range(max(data)):
        deltas[i] = score_fn(i, data)

    m_key = min(deltas, key=lambda d: deltas[d])
    print(m_key)
    print(deltas[m_key])


def part1_score(i, data):
    return sum(max(i, d) - min(i, d) for d in data)


from functools import cache


@cache
def cost(i, d):
    v = max(i, d) - min(i, d)
    return v * (v + 1) // 2


def part2_score(i, data):
    """
    As it turns out, crab submarine engines don't burn fuel at a constant rate. Instead, each change of 1 step in horizontal position costs 1 more unit of fuel than the last: the first step costs 1, the second step costs 2, the third step costs 3, and so on.
    """
    return sum(cost(i, d) for d in data)


def part1():
    solve(part1_score)


def part2():
    solve(part2_score)


part2()
