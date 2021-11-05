"""
***** --- Day 24: Lobby Layout --- *****
Your raft makes it to the tropical island; it turns out that the small crab
was an excellent navigator. You make your way to the resort.
As you enter the lobby, you discover a small problem: the floor is being
renovated. You can't even reach the check-in desk until they've finished
installing the new tile floor.
The tiles are all hexagonal; they need to be arranged in a hex_grid with a
very specific color pattern. Not in the mood to wait, you offer to help
figure out the pattern.
The tiles are all white on one side and black on the other. They start with
the white side facing up. The lobby is large enough to fit whatever pattern
might need to appear there.
A member of the renovation crew gives you a list of the tiles that need to
be flipped over (your puzzle input). Each line in the list identifies a
single tile that needs to be flipped by giving a series of steps starting
from a reference tile in the very center of the room. (Every line starts
from the same reference tile.)
Because the tiles are hexagonal, every tile has six neighbors: east,
southeast, southwest, west, northwest, and northeast. These directions are
given in your list, respectively, as e, se, sw, w, nw, and ne. A tile is
identified by a series of these directions with no delimiters; for example,
esenee identifies the tile you land on if you start at the reference tile
and then move one tile east, one tile southeast, one tile northeast, and
one tile east.
Each time a tile is identified, it flips from white to black or from black
to white. Tiles might be flipped more than once. For example, a line like
esew flips a tile immediately adjacent to the reference tile, and a line
like nwwswee flips the reference tile itself.
Here is a larger example:
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
In the above example, 10 tiles are flipped once (to black), and 5 more are
flipped twice (to black, then back to white). After all of these
instructions have been followed, a total of 10 tiles are black.
Go through the renovation crew's list and determine which tiles they need
to flip. After all of the instructions have been followed, how many tiles
are left with the black side up?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *
import re

e = Exercise(24)


dirs = {
    'nw': (1, 0, -1),
    'ne': (1, -1, 0),
    'e': (0, -1, 1),
    'se': (-1, 0, 1),
    'sw': (-1, 1, 0),
    'w': (0, 1, -1),
}

R = re.compile("e|se|sw|w|nw|ne")
@e.transformer(map=True)
def xform(row):
    row[0]
    l = list(R.findall(row[0]))

    return l

import collections



def add(a, b):
    return tuple(map(sum, zip(a,b)))

def walk(path):
    c = (0, 0, 0)
    for d in path:
        c = add(c, dirs[d])
    return c

assert walk(["nw", "w","sw", "e", "e"]) == (0, 0, 0)



@e.part1()
def part1(xs):
    blacks = build_state(xs)
    return sum(1 for k in blacks if blacks[k])

NEIGHBORS = list(dirs.values())
def neighbors(coord):
    for d in NEIGHBORS:
        yield add(coord, d)

def build_state(xs):
    blacks = collections.defaultdict(lambda: False)
    for r in xs.t:
        c = walk(r)
        blacks[c] = not blacks[c]
    return blacks

def consider_cell(blacks, coord):
    occ = 0
    for n in neighbors(coord):
        if blacks[n]:
            occ += 1

    if blacks[coord]:
        return occ == 0 or occ > 2
    else:
        return occ == 2

import itertools
@e.part2()
def part2(xs):
    blacks = build_state(xs)
    to_consider = set(blacks.keys())
    for i in range(100):
        print(i)
        to_consider.update(itertools.chain.from_iterable(neighbors(c) for c in blacks.keys()))
        updates = set()
        for c in to_consider:
            if consider_cell(blacks, c):
                updates.add(c)
        for c in updates:
            blacks[c] = not blacks[c]
        to_consider = updates


    return sum(1 for k in blacks if blacks[k])



e()
