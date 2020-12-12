"""
***** --- Day 12: Rain Risk --- *****
Your ferry made decent progress toward the island, but the storm came in
faster than anyone expected. The ferry needs to take evasive actions!
Unfortunately, the ship's navigation computer seems to be malfunctioning;
rather than giving a route directly to safety, it produced extremely
circuitous instructions. When the captain uses the PA_system to ask if
anyone can help, you quickly volunteer.
The navigation instructions (your puzzle input) consists of a sequence of
single-character actions paired with integer input values. After staring at
them for a few minutes, you work out what they probably mean:
    * Action N means to move north by the given value.
    * Action S means to move south by the given value.
    * Action E means to move east by the given value.
    * Action W means to move west by the given value.
    * Action L means to turn left the given number of degrees.
    * Action R means to turn right the given number of degrees.
    * Action F means to move forward by the given value in the direction
      the ship is currently facing.
The ship starts by facing east. Only the L and R actions change the
direction the ship is facing. (That is, if the ship is facing east and the
next instruction is N10, the ship would move north 10 units, but would
still move east if the following action were F.)
For example:
F10
N3
F7
R90
F11
These instructions would be handled as follows:
    * F10 would move the ship 10 units east (because the ship starts by
      facing east) to east 10, north 0.
    * N3 would move the ship 3 units north to east 10, north 3.
    * F7 would move the ship another 7 units east (because the ship is
      still facing east) to east 17, north 3.
    * R90 would cause the ship to turn right by 90 degrees and face south;
      it remains at east 17, north 3.
    * F11 would move the ship 11 units south to east 17, south 8.
At the end of these instructions, the ship's Manhattan_distance (sum of the
absolute values of its east/west position and its north/south position)
from its starting position is 17 + 8 = 25.
Figure out where the navigation instructions lead. What is the Manhattan
distance between that location and the ship's starting position?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *

e = Exercise(12, parser={ "field_sep": "(\d+$)"})

@e.transformer(map=True)
def xform(x):
    return (x[0], x[1])


def add_heading(coords, heading, amount):
    new_x = coords[0] + (heading[0] * amount)
    new_y = coords[1] + (heading[1] * amount)
    return new_x, new_y


def deg_to_heading(heading):
    if heading < 0:
        heading = 360 - ((-heading) % 360)
    else:
        heading = heading % 360
    if heading == 0:
        return (0, 1)
    elif heading == 90:
        return (1, 0)
    elif heading == 180:
        return (0, -1)
    elif heading == 270:
        return (-1, 0)
    else:
        raise RuntimeError("bad heading")

@e.part1()
def part1(xs):
    heading = 0
    coords = (0, 0)
    for (instr, d) in xs.t:
        heading_c = deg_to_heading(heading)
        if instr == "F":
            coords = add_heading(coords, heading_c, d)
        elif instr == "B":
            coords = add_heading(coords, heading_c, -d)
        elif instr == "N":
            coords = add_heading(coords, (-1, 0), d)
        elif instr == "S":
            coords = add_heading(coords, (1, 0), d)
        elif instr == "E":
            coords = add_heading(coords, (0, 1), d)
        elif instr == "W":
            coords = add_heading(coords, (0, -1), d)
        elif instr == "L":
            heading += -d
        elif instr == "R":
            heading += d

    print(coords)

    return abs(coords[0]) + abs(coords[1])



def rotate_around(rel, rot):
    if rot < 0:
        rot = 360 - ((-rot) % 360)
    else:
        rot = rot % 360
    if rot == 0:
        return rel
    elif rot == 90:
        return rel[1], -rel[0]
    elif rot == 180:
        return -rel[0], -rel[1]
    elif rot == 270:
        return -rel[1], rel[0]
    else:
        raise RuntimeError("rhee")

@e.part2()
def part1(xs):
    coords = (0, 0)
    coords_wp = (-1, 10)
    for (instr, d) in xs.t:
        if instr == "F":
            coords = add_heading(coords, coords_wp, d)
        elif instr == "N":
            coords_wp = add_heading(coords_wp, (-1, 0), d)
        elif instr == "S":
            coords_wp = add_heading(coords_wp, (1, 0), d)
        elif instr == "E":
            coords_wp = add_heading(coords_wp, (0, 1), d)
        elif instr == "W":
            coords_wp = add_heading(coords_wp, (0, -1), d)
        elif instr == "L":
            coords_wp = rotate_around(coords_wp, -d)
        elif instr == "R":
            coords_wp = rotate_around(coords_wp, d)

    print(coords)
    return abs(coords[0]) + abs(coords[1])

e()
