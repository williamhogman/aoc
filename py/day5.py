"""
***** --- Day 5: Binary Boarding --- *****
You board your plane only to discover a new problem: you dropped your
boarding pass! You aren't sure which seat is yours, and all of the flight
attendants are busy with the flood of people that suddenly made it through
passport control.
You write a quick program to use your phone's camera to scan all of the
nearby boarding passes (your puzzle input); perhaps you can find your seat
through process of elimination.
Instead of zones_or_groups, this airline uses binary space partitioning to
seat people. A seat might be specified like FBFBBFFRLR, where F means
"front", B means "back", L means "left", and R means "right".
The first 7 characters will either be F or B; these specify exactly one of
the 128 rows on the plane (numbered 0 through 127). Each letter tells you
which half of a region the given seat is in. Start with the whole list of
rows; the first letter indicates whether the seat is in the front (0
through 63) or the back (64 through 127). The next letter indicates which
half of that region the seat is in, and so on until you're left with
exactly one row.
For example, consider just the first seven characters of FBFBBFFRLR:
    * Start by considering the whole range, rows 0 through 127.
    * F means to take the lower half, keeping rows 0 through 63.
    * B means to take the upper half, keeping rows 32 through 63.
    * F means to take the lower half, keeping rows 32 through 47.
    * B means to take the upper half, keeping rows 40 through 47.
    * B keeps rows 44 through 47.
    * F keeps rows 44 through 45.
    * The final F keeps the lower of the two, row 44.
The last three characters will be either L or R; these specify exactly one
of the 8 columns of seats on the plane (numbered 0 through 7). The same
process as above proceeds again, this time with only three steps. L means
to keep the lower half, while R means to keep the upper half.
For example, consider just the last 3 characters of FBFBBFFRLR:
    * Start by considering the whole range, columns 0 through 7.
    * R means to take the upper half, keeping columns 4 through 7.
    * L means to take the lower half, keeping columns 4 through 5.
    * The final R keeps the upper of the two, column 5.
So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.
Every seat also has a unique seat ID: multiply the row by 8, then add the
column. In this example, the seat has ID 44 * 8 + 5 = 357.
Here are some other boarding passes:
    * BFFFBBFRRR: row 70, column 7, seat ID 567.
    * FFFBBBFRRR: row 14, column 7, seat ID 119.
    * BBFFBBFRLL: row 102, column 4, seat ID 820.
As a sanity check, look through your list of boarding passes. What is the
highest seat ID on a boarding pass?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *

e = Exercise(5, parser={ "field_sep": "([RL]{3})(?:$)"})

def mid(a, b):
    return (a + b) // 2

def walk(path, start, end):
    low = start
    high = end
    instr = L(path).map(lambda x: x == "B" or x == "R")
    for i in instr[:-1]:
        if i:
            low = mid(low, high) + 1
        else:
            high = mid(low, high)
    if instr[-1]:
        return high
    else:
        return low

assert walk(list("FBFBBFF"), 0, 127) == 44
assert walk(list("RLR"), 0, 7) == 5
assert walk(list("BFFFBBF"), 0, 127) == 70
assert walk(list("FFFBBBF"), 0, 127) == 14
assert walk(list("BBFFBBF"), 0, 127) == 102

@e.part1(map=True, reduce="max")
def part1(xs):
    xs = L(xs)
    row = walk(list(xs[0]), 0, 127)
    seat = walk(list(xs[1]), 0, 7)
    return row * 8 + seat

@e.part2
def part2(xs):
    seat_ids = xs.map(part1)
    s = set(seat_ids.t)
    for i in range(0, 128 * 8):
        if i not in s and i + 1 in s and i - 1 in s:
            return i

e()
