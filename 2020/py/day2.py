from fastcore.all import L, Self
from util import Exercise

e = Exercise(2)

@e.part1(map=True, reduce="count")
def part1(xs):
    return xs[1] >= sum(1 for c in xs[3] if xs[2] == c) >= xs[0]


@e.part2(map=True, reduce="count")
def part2(xs):
    l = [c == xs[2] for c in xs[3]]
    a = l[xs[0] - 1] if xs[0] - 1 < len(l) else False
    b = l[xs[1] - 1] if xs[1] - 1 < len(l) else False
    return a != b

e()
