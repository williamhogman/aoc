"""
***** --- Day 11: Seating System --- *****
Your plane lands with plenty of time to spare. The final leg of your
journey is a ferry that goes directly to the tropical island where you can
finally start your vacation. As you reach the waiting area to board the
ferry, you realize you're so early, nobody else has even arrived yet!
By modeling the process people use to choose (or abandon) their seat in the
waiting area, you're pretty sure you can predict the best place to sit. You
make a quick map of the seat layout (your puzzle input).
The seat layout fits neatly on a grid. Each position is either floor (.),
an empty seat (L), or an occupied seat (#). For example, the initial seat
layout might look like this:
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
Now, you just need to model the people who will be arriving shortly.
Fortunately, people are entirely predictable and always follow a simple set
of rules. All decisions are based on the number of occupied seats adjacent
to a given seat (one of the eight positions immediately up, down, left,
right, or diagonal from the seat). The following rules are applied to every
seat simultaneously:
    * If a seat is empty (L) and there are no occupied seats adjacent to
      it, the seat becomes occupied.
    * If a seat is occupied (#) and four or more seats adjacent to it are
      also occupied, the seat becomes empty.
    * Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.
After one round of these rules, every seat in the example layout becomes
occupied:
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
After a second round, the seats with four or more occupied adjacent seats
become empty again:
#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
This process continues for three more rounds:
#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
At this point, something interesting happens: the chaos stabilizes and
further applications of these rules cause no seats to change state! Once
people stop moving around, you count 37 occupied seats.
Simulate your seating area by applying the seating rules repeatedly until
no seats change state. How many seats end up occupied?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *

e = Exercise(11, parser={"field_sep": ""})


adjacent = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    # (0, 0) but thats us
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
]

def get_adj(playfield, i, j):
    for (delta_row, delta_col) in adjacent:
        res = maybe_get(playfield, i + delta_row, j + delta_col)
        if res is not None:
            yield res


def round(playfield):
    did_change = False
    new_playfield = [list(x) for x in playfield]
    for i in range(len(playfield)):
        for j in range(len(playfield[i])):
            cell = playfield[i][j]
            if cell == ".":
                continue

            if cell == "L":
                if all(a != "#" for a in get_adj(playfield, i, j)):
                    new_playfield[i][j] = "#"
                    did_change = True
            elif cell == "#":
                if sum(a == "#" for a in get_adj(playfield, i, j)) >= 4:
                    new_playfield[i][j] = "L"
                    did_change = True

    if did_change:
        return new_playfield

@e.part1()
def part1(xs):
    playfield = [list(x) for x in xs.t]
    while True:
        new_playfield = round(playfield)
        if new_playfield is None:
            break
        playfield = new_playfield

    occ = 0
    for row in playfield:
        for col in row:
            if col == "#":
                occ += 1

    return occ

def round_t(playfield):
    new_playfield = [list(x) for x in playfield]
    changes = {}
    for i in range(len(playfield)):
        for j in range(len(playfield[i])):
            cell = playfield[i][j]
            if cell == ".":
                continue

            if cell == "L":
                if all(a != "#" for a in rays(playfield, i, j)):
                    changes[(i, j)] = "#"
            elif cell == "#":
                if sum(a == "#" for a in rays(playfield, i, j)) >= 5:
                    changes[(i, j)] = "L"
    return changes

def maybe_get(playfield, i, j):
    if i >= 0 and i < len(playfield) and j >= 0 and j < len(playfield[i]):
        return playfield[i][j]
    return None

def rays(playfield, i, j):
    for (delta_row, delta_col) in adjacent:
        res = maybe_get(playfield, i + delta_row, j + delta_col)
        steps = 2
        while res == ".":
            res = maybe_get(playfield, i + (delta_row * steps), j + (delta_col * steps))
            steps += 1
        if res == "L":
            yield "L"
        elif res == "#":
            yield "#"
        else:
            pass




@e.part2()
def part2(xs):
    playfield = [list(x) for x in xs.t]
    while True:
        changes = round_t(playfield)
        if len(changes) == 0:
            break

        for (i, j) in changes:
            playfield[i][j] = changes[(i, j)]
    occ = 0
    for row in playfield:
        for col in row:
            if col == "#":
                occ += 1

    return occ


e()
