"""
***** --- Day 20: Jurassic Jigsaw --- *****
The high-speed train leaves the forest and quickly carries you south. You
can even see a desert in the distance! Since you have some spare time, you
might as well see if there was anything interesting in the image the
Mythical Information Bureau satellite captured.
After decoding the satellite messages, you discover that the data actually
contains many small images created by the satellite's camera array. The
camera array consists of many cameras; rather than produce a single square
image, they produce many smaller square image tiles that need to be
reassembled back into a single image.
Each camera in the camera array returns a single monochrome image tile with
a random unique ID number. The tiles (your puzzle input) arrived in a
random order.
Worse yet, the camera array appears to be malfunctioning: each image tile
has been rotated and flipped to a random orientation. Your first task is to
reassemble the original image by orienting the tiles so they fit together.
To show how the tiles should be reassembled, each tile's image data
includes a border that should line up exactly with its adjacent tiles. All
tiles have this border, and the border lines up exactly when the tiles are
both oriented correctly. Tiles at the edge of the image also have this
border, but the outermost edges won't line up with any other tiles.
For example, suppose you have the following nine tiles:
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
By rotating, flipping, and rearranging them, you can find a square
arrangement that causes all adjacent borders to line up:
#...##.#.. ..###..### #.#.#####.
..#.#..#.# ###...#.#. .#..######
.###....#. ..#....#.. ..#.......
###.##.##. .#.#.#..## ######....
.###.##### ##...#.### ####.#..#.
.##.#....# ##.##.###. .#...#.##.
#...###### ####.#...# #.#####.##
.....#..## #...##..#. ..#.###...
#.####...# ##..#..... ..#.......
#.##...##. ..##.#..#. ..#.###...

#.##...##. ..##.#..#. ..#.###...
##..#.##.. ..#..###.# ##.##....#
##.####... .#.####.#. ..#.###..#
####.#.#.. ...#.##### ###.#..###
.#.####... ...##..##. .######.##
.##..##.#. ....#...## #.#.#.#...
....#..#.# #.#.#.##.# #.###.###.
..#.#..... .#.##.#..# #.###.##..
####.#.... .#..#.##.. .######...
...#.#.#.# ###.##.#.. .##...####

...#.#.#.# ###.##.#.. .##...####
..#.#.###. ..##.##.## #..#.##..#
..####.### ##.#...##. .#.#..#.##
#..#.#..#. ...#.#.#.. .####.###.
.#..####.# #..#.#.#.# ####.###..
.#####..## #####...#. .##....##.
##.##..#.. ..#...#... .####...#.
#.#.###... .##..##... .####.##.#
#...###... ..##...#.. ...#..####
..#.#....# ##.#.#.... ...##.....
For reference, the IDs of the above tiles are:
1951    2311    3079
2729    1427    2473
2971    1489    1171
To check that you've assembled the image correctly, multiply the IDs of the
four corner tiles together. If you do this with the assembled tiles from
the example above, you get 1951 * 3079 * 2971 * 1171 = 20899048083289.
Assemble the tiles into an image. What do you get if you multiply together
the IDs of the four corner tiles?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *
import numpy as np
e = Exercise(20, parser={'field_sep':'$^'})

@e.transformer(map=False)
def xform(xs):
    pieces = {}
    current = []
    for row in xs.t:
        if len(row) == 2 and row == ("", ""):
            continue
        if row[0].startswith("Tile "):
            if len(current) > 0:
                pieces[piece] = np.array(current)
                current = []
            piece = int(row[0][5:-1])

        else:
            current.append([True if x == "#" else False for x in row[0]])
    if len(current) > 0:
        pieces[piece] = np.array(current)
        current = []
    return pieces

import math


def version(arr, n):
    rot = n // 4
    flip = n % 4
    if n == 0:
        return arr
    if rot > 0:
        arr = np.rot90(arr, k=rot)
    if flip == 0:
        return arr
    elif flip == 1:
        return np.flip(arr, 0)
    elif flip == 2:
        return np.flip(arr, 1)
    elif flip == 3:
        return np.flip(arr)

def versions(arr):
    for i in range(16):
        yield version(arr, i)

import itertools
import collections
import math

def share_lr_border(left, right):
    return np.all(left[-1, :] == right[0, :])

def share_tb_border(top, bottom):
    return np.all(top[:, -1] == bottom[:, 0])

class Pairwise:
    def __init__(self, xs):
        self.all = set(xs)
        self.right_of = collections.defaultdict(set)
        self.below = collections.defaultdict(set)
        oriented = itertools.product(xs, range(16))
        for (a, ao), (b, bo) in itertools.product(oriented, repeat=2):
            if a == b:
                continue
            aa = version(xs[a], ao)
            bb = version(xs[b], bo)
            if share_lr_border(aa, bb):
                self.right_of[(a, ao)].add((b, bo))
            if share_tb_border(aa, bb):
                self.below[(a, ao)].add((b, bo))

    def candidates(self, used, above, left):
        cands = {
            (i, o)
            for (i, o) in
            itertools.product(self.all - used, range(16))
        }
        if above is not None:
            cands &= self.below[above]
        if left is None:
            cands &= self.right_of[left]

        return cands




def find_correct_orrientation(xs):
    side = int(math.sqrt(len(xs)))
    pw = Pairwise(xs)
    for start_tile, vsn in itertools.product(xs, range(16)):
        placed = [(start_tile, vsn)]
        used = {start_tile}
        found_all_matches = True
        for i in range(1, len(xs)):
            found_match = False
            above = placed[i - 1][1] if i % side != 0 else None
            left = placed[i - side][1] if i // side != 0 else None
            for k, vsn in pw.candidates(used, above, left):
                placed.append((k, vsn))
                used.add(k)
                found_match = True
                break
            if not found_match:
                found_all_matches = False
                break
        if found_all_matches:
            break
    return [(i, version(xs[i], o)) for (i, o) in placed]


@e.part1()
def part1(xs):
    return 0
    side = int(math.sqrt(len(xs)))
    correct = find_correct_orrientation(xs)
    tilemap = np.array([x[0] for x in correct]).reshape((side, side))
    return np.prod(tilemap[[0,0,-1,-1],[0,-1,0,-1]])


monster = (
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
)
monster = np.array([list(line) for line in monster]) == "#"
monster_size = np.sum(monster)

def count_monsters(img):
    n = 0
    for (i, j) in itertools.product(
            range(img.shape[0] - monster.shape[0] + 1),
            range(img.shape[1] - monster.shape[1] + 1),
    ):
        window = img[i:i +monster.shape[0], j:j+monster.shape[1]]
        if np.all((window & monster) == monster):
            n += 1
    return n



@e.part2()
def part2(xs):
    side = int(math.sqrt(len(xs)))
    correct = find_correct_orrientation(xs)
    chunk_side = correct[0][1].shape[0] - 2 # w/o borders
    img_size = chunk_side * side
    img = np.zeros((img_size, img_size), dtype=bool)
    for ix, (_, tile) in enumerate(correct):
        i, j = divmod(ix, side)
        img[i*chunk_side:i*chunk_side+chunk_side, j*chunk_side:j*chunk_side+chunk_side] = tile[1:-1, 1:-1]

    noise = np.sum(img)

    for oriented in versions(img):
        n = count_monsters(oriented)
        if n > 0:
            return noise - (monster_size * n)


e()
