"""
***** --- Day 13: Shuttle Search --- *****
Your ferry can make it safely to a nearby port, but it won't get much
further. When you call to book another ship, you discover that no ships
embark from that port to your vacation island. You'll need to get from the
port to the nearest airport.
Fortunately, a shuttle bus service is available to bring you from the sea
port to the airport! Each bus has an ID number that also indicates how
often the bus leaves for the airport.
Bus schedules are defined based on a timestamp that measures the number of
minutes since some fixed reference point in the past. At timestamp 0, every
bus simultaneously departed from the sea port. After that, each bus travels
to the airport, then various other locations, and finally returns to the
sea port to repeat its journey forever.
The time this loop takes a particular bus is also its ID number: the bus
with ID 5 departs from the sea port at timestamps 0, 5, 10, 15, and so on.
The bus with ID 11 departs at 0, 11, 22, 33, and so on. If you are there
when the bus departs, you can ride that bus to the airport!
Your notes (your puzzle input) consist of two lines. The first line is your
estimate of the earliest timestamp you could depart on a bus. The second
line lists the bus IDs that are in service according to the shuttle
company; entries that show x must be out of service, so you decide to
ignore them.
To save time once you arrive, your goal is to figure out the earliest bus
you can take to the airport. (There will be exactly one such bus.)
For example, suppose you have the following notes:
939
7,13,x,x,59,x,31,19
Here, the earliest timestamp you could depart is 939, and the bus IDs in
service are 7, 13, 59, 31, and 19. Near timestamp 939, these bus IDs depart
at the times marked D:
time   bus 7   bus 13  bus 59  bus 31  bus 19
929      .       .       .       .       .
930      .       .       .       D       .
931      D       .       .       .       D
932      .       .       .       .       .
933      .       .       .       .       .
934      .       .       .       .       .
935      .       .       .       .       .
936      .       D       .       .       .
937      .       .       .       .       .
938      D       .       .       .       .
939      .       .       .       .       .
940      .       .       .       .       .
941      .       .       .       .       .
942      .       .       .       .       .
943      .       .       .       .       .
944      .       .       D       .       .
945      D       .       .       .       .
946      .       .       .       .       .
947      .       .       .       .       .
948      .       .       .       .       .
949      .       D       .       .       .
The earliest bus you could take is bus ID 59. It doesn't depart until
timestamp 944, so you would need to wait 944 - 939 = 5 minutes before it
departs. Multiplying the bus ID by the number of minutes you'd need to wait
gives 295.
What is the ID of the earliest bus you can take to the airport multiplied
by the number of minutes you'll need to wait for that bus?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *

e = Exercise(13)

@e.transformer()
def xform(xs):
    return (xs.t[0], list(xs.t[1]))

@e.part1()
def part1(xs):
    earliest = xs[0][0]
    ids = [x for x in xs[1] if x != 'x']

    mods = [(earliest % x, x) for x in ids]

    i = earliest
    min_waited = 0
    while True:
        for x in ids:
            if i % x == 0:
                return min_waited * x

        i += 1
        min_waited += 1


    m = (100000, 1000000)
    for (a, b) in mods:
        if a < m[0]:
            m = (a, b)



    return m[0] * m[1]

    return min_id * min_arr


def cprod(xs):
    p = 1
    for x in xs:
        p *= x
    return p

def computeGCD(x, y):
   while(y):
       x, y = y, x % y

   return x

def ExtendedEuclideanAlgorithm(a, b):
    """
        Calculates gcd(a,b) and a linear combination such that
        gcd(a,b) = a*x + b*y

        As a side effect:
        If gcd(a,b) = 1 = a*x + b*y
        Then x is multiplicative inverse of a modulo b.
    """
    aO, bO = a, b

    x = lasty = 0
    y = lastx = 1
    while b != 0:
        q = a / b
        a, b = b, a % b
        x, lastx = lastx - q * x, x
        y, lasty = lasty - q * y, y

    return {"x": lastx, "y": lasty, "gcd": aO * lastx + bO * lasty}


def solveLinearCongruenceEquations(things):
    """
    Solve a system of linear congruences.

    >>> solveLinearCongruenceEquations([4, 12, 14], [19, 37, 43])
    {'congruence class': 22804, 'modulo': 30229}
    """
    x = 0
    M = reduce(lambda x, y: x * y, modulos)

    for mi, resti in zip(modulos, rests):
        Mi = M / mi
        s = ExtendedEuclideanAlgorithm(Mi, mi)["x"]
        e = s * Mi
        x += resti * e
    return {"congruence class": ((x % M) + M) % M, "modulo": M}


@e.part2()
def part2(xs):
    ids = xs[1]
    ds = [(x - i, x) for (i, x) in enumerate(ids) if x != "x"]

    Ns = [d[1] for d in ds]
    As = [d[0] for d in ds]
    print(Ns)
    print(As)

    return chinese_remainder(Ns, As)



def chinese_remainder(n, a):
    sum = 0
    prod = cprod(n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod



def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


e()
