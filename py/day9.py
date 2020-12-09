"""
***** --- Day 9: Encoding Error --- *****
With your neighbor happily enjoying their video game, you turn your
attention to an open data port on the little screen in the seat in front of
you.
Though the port is non-standard, you manage to connect it to your computer
through the clever use of several paperclips. Upon connection, the port
outputs a series of numbers (your puzzle input).
The data appears to be encrypted with the eXchange-Masking Addition System
(XMAS) which, conveniently for you, is an old cypher with an important
weakness.
XMAS starts by transmitting a preamble of 25 numbers. After that, each
number you receive should be the sum of any two of the 25 immediately
previous numbers. The two numbers will have different values, and there
might be more than one such pair.
For example, suppose your preamble consists of the numbers 1 through 25 in
a random order. To be valid, the next number must be the sum of two of
those numbers:
    * 26 would be a valid next number, as it could be 1 plus 25 (or many
      other pairs, like 2 and 24).
    * 49 would be a valid next number, as it is the sum of 24 and 25.
    * 100 would not be valid; no two of the previous 25 numbers sum to 100.
    * 50 would also not be valid; although 25 appears in the previous 25
      numbers, the two numbers in the pair must be different.
Suppose the 26th number is 45, and the first number (no longer an option,
as it is more than 25 numbers ago) was 20. Now, for the next number to be
valid, there needs to be some pair of numbers among 1-19, 21-25, or 45 that
add up to it:
    * 26 would still be a valid next number, as 1 and 25 are still within
      the previous 25 numbers.
    * 65 would not be valid, as no two of the available numbers sum to it.
    * 64 and 66 would both be valid, as they are the result of 19+45 and
      21+45 respectively.
Here is a larger example which only considers the previous 5 numbers (and
has a preamble of length 5):
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
In this example, after the 5-number preamble, almost every number is the
sum of two of the previous 5 numbers; the only number that does not follow
this rule is 127.
The first step of attacking the weakness in the XMAS data is to find the
first number in the list (after the preamble) which is not the sum of two
of the 25 numbers before it. What is the first number that does not have
this property?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *

e = Exercise(9)

def get_chunks(xs, size=25):
    for i in range(size, len(xs) - 1):
        yield xs[i-size:i], xs[i]

import itertools
def any_two_sum_to(xs, target):
    for (a, b) in itertools.combinations(xs, 2):
        if (a + b) == target:
            return True
    return False


@e.part1()
def part1(xs):
    nos = xs.t.map(lambda x: x[0])
    chunks = get_chunks(nos)
    for preamble, no in chunks:
        assert len(preamble) == 25
        if not any_two_sum_to(preamble, no):
            return no
    return None

def example():
    data = [
        35,
        20,
        15,
        25,
        47,
        40,
        62,
        55,
        65,
        95,
        102,
        117,
        150,
        182,
        127,
        219,
        299,
        277,
        309,
        576,
    ]
    for preamble, no in get_chunks(data, 5):
        if not any_two_sum_to(preamble, no):
            return no
    return None

# inc 217430975
@e.part2()
def part2(xs):
    nos = xs.t.map(lambda x: x[0])
    target = 217430975
    i = 0
    j = 0

    for i in range(len(nos)):
        current = nos[i]
        r_min = nos[i]
        r_max = nos[i]
        if current >= target:
            continue
        j = i + 1
        while current < target:
            r_min = min(r_min, nos[j])
            r_max = max(r_max, nos[j])
            current += nos[j]
            j += 1
        if current == target:
            return r_min + r_max

    return None


assert not any_two_sum_to([95,
                       102,
                       117,
                       150,
                       182], 127)
assert example() == 127
assert 3 not in ([0, 1, 2, 3, 4, 5][1: 3])
e()
