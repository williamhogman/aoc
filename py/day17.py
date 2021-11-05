"""
***** --- Day 17: Conway Cubes --- *****
As your flight slowly drifts through the sky, the Elves at the Mythical
Information Bureau at the North Pole contact you. They'd like some help
debugging a malfunctioning experimental energy source aboard one of their
super-secret imaging satellites.
The experimental energy source is based on cutting-edge technology: a set
of Conway Cubes contained in a pocket dimension! When you hear it's having
problems, you can't help but agree to take a look.
The pocket dimension contains an infinite 3-dimensional grid. At every
integer 3-dimensional coordinate (x,y,z), there exists a single cube which
is either active or inactive.
In the initial state of the pocket dimension, almost all cubes start
inactive. The only exception to this is a small flat region of cubes (your
puzzle input); the cubes in this region start in the specified active (#)
or inactive (.) state.
The energy source then proceeds to boot up by executing six cycles.
Each cube only ever considers its neighbors: any of the 26 other cubes
where any of their coordinates differ by at most 1. For example, given the
cube at x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2, the
cube at x=0,y=2,z=3, and so on.
During a cycle, all cubes simultaneously change their state according to
the following rules:
    * If a cube is active and exactly 2 or 3 of its neighbors are also
      active, the cube remains active. Otherwise, the cube becomes
      inactive.
    * If a cube is inactive but exactly 3 of its neighbors are active, the
      cube becomes active. Otherwise, the cube remains inactive.
The engineers responsible for this experimental energy source would like
you to simulate the pocket dimension and determine what the configuration
of cubes should be at the end of the six-cycle boot process.
For example, consider the following initial state:
.#.
..#
###
Even though the pocket dimension is 3-dimensional, this initial state
represents a small 2-dimensional slice of it. (In particular, this initial
state defines a 3x3x1 region of the 3-dimensional space.)
Simulating a few cycles from this initial state produces the following
configurations, where the result of each cycle is shown layer-by-layer at
each given z coordinate:
Before any cycles:

z=0
.#.
..#
###


After 1 cycle:

z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.


After 2 cycles:

z=-2
.....
.....
..#..
.....
.....

z=-1
..#..
.#..#
....#
.#...
.....

z=0
##...
##...
#....
....#
.###.

z=1
..#..
.#..#
....#
.#...
.....

z=2
.....
.....
..#..
.....
.....


After 3 cycles:

z=-2
.......
.......
..##...
..###..
.......
.......
.......

z=-1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=0
...#...
.......
#......
.......
.....##
.##.#..
...#...

z=1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=2
.......
.......
..##...
..###..
.......
.......
.......
After the full six-cycle boot process completes, 112 cubes are left in the
active state.
Starting with your given initial configuration, simulate six cycles. How
many cubes are left in the active state after the sixth cycle?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *

e = Exercise(17, parser={"field_sep": ""})

@e.transformer()
def xform(xs):
    inp = [
        ".##.##..",
        "..###.##",
        ".##....#",
        "###..##.",
        "#.###.##",
        ".#.#..#.",
        ".......#",
        ".#..#..#",
    ]
    res = []
    for j, row in enumerate(inp):
        for k, col in enumerate(row):
            if col == "#":
                res.append((j, k))
    return res

import itertools

_n_memo = {}


def neighbors_of(coords):
    if (m := _n_memo.get(coords)) is not None:
        return m
    ns = neighbors_of_inner(coords)
    r = []
    for c in ns:
        r.append(c)
        yield c
    _n_memo[coords] = r

def neighbors_of_inner(coords):
    for ds in itertools.product([-1, 0, 1], repeat=len(coords)):
        if all(x == 0 for x in ds):
            continue
        res = tuple([a + b for (a, b) in zip(coords, ds)])
        yield res

assert len(list(neighbors_of((0,0,0,0)))) == 80

def get_changeable(gamestate):
    used = set()
    for k in gamestate:
        if k not in used:
            yield k
            used.add(k)
        for x in neighbors_of(k):
            if x not in used:
                yield x
                used.add(x)


def consider_cell(gamestate, coord):
    active_around = 0
    for n in neighbors_of(coord):
        state = gamestate.get(n, False)
        if state:
            active_around += 1
    return active_around

def print_map(gamestate):
    dims = max(len(k) for k in gamestate) - 3
    for lower in set(k[:dims] for k in gamestate.keys()):
        print(lower)
        for j in range(-7, 14):
            line = ""
            for k in range(-7, 14):
                if not gamestate.get(lower + (j, k), False):
                    line += "."
                else:
                    line += "#"
            print(line)

def do_round(gamestate):
    new = dict()
    for coord in get_changeable(gamestate):
        v = gamestate.get(coord, False)
        res = consider_cell(gamestate, coord)
        if v:
            if res in [2, 3]:
                new[coord] = True
        else:
            if res == 3:
                new[coord] = True
    return new

def run_game(gamestate):
    for game_round in range(6):
        gamestate = do_round(gamestate)
    return sum(gamestate.values())

@e.part1()
def part1(xs):
    return run_game({(0, x, y): True for x, y in xs})


@e.part2()
def part2(xs):
    return run_game({(0, 0, x, y): True for x, y in xs})

e()
