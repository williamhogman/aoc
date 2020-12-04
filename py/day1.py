from fastcore.all import L, Self
from math import prod
from util import Exercise
from itertools import combinations

e = Exercise(1)

def logic(x, n):
    return L(combinations(x.col(), n)).filter(lambda x: sum(x) == 2020).map(prod)[0]

@e.part1
def part1(x):
    return logic(x, 2)


@e.part2
def part2(x):
    return logic(x, 3)


e()
