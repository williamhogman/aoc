"""
***** --- Day 14: Docking Data --- *****
As your ferry approaches the sea port, the captain asks for your help
again. The computer system that runs this port isn't compatible with the
docking program on the ferry, so the docking parameters aren't being
correctly initialized in the docking program's memory.
After a brief inspection, you discover that the sea port's computer system
uses a strange bitmask system in its initialization program. Although you
don't have the correct decoder chip handy, you can emulate it in software!
The initialization program (your puzzle input) can either update the
bitmask or write a value to memory. Values and memory addresses are both
36-bit unsigned integers. For example, ignoring bitmasks for a moment, a
line like mem[8] = 11 would write the value 11 to memory address 8.
The bitmask is always given as a string of 36 bits, written with the most
significant bit (representing 2^35) on the left and the least significant
bit (2^0, that is, the 1s bit) on the right. The current bitmask is applied
to values immediately before they are written to memory: a 0 or 1
overwrites the corresponding bit in the value, while an X leaves the bit in
the value unchanged.
For example, consider the following program:
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
This program starts by specifying a bitmask (mask = ....). The mask it
specifies will overwrite two bits in every written value: the 2s bit is
overwritten with 0, and the 64s bit is overwritten with 1.
The program then attempts to write the value 11 to memory address 8. By
expanding everything out to individual bits, the mask is applied as
follows:
value:  000000000000000000000000000000001011  (decimal 11)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001001001  (decimal 73)
So, because of the mask, the value 73 is written to memory address 8
instead. Then, the program tries to write 101 to address 7:
value:  000000000000000000000000000001100101  (decimal 101)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001100101  (decimal 101)
This time, the mask has no effect, as the bits it overwrote were already
the values the mask tried to set. Finally, the program tries to write 0 to
address 8:
value:  000000000000000000000000000000000000  (decimal 0)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001000000  (decimal 64)
64 is written to address 8 instead, overwriting the value that was there
previously.
To initialize your ferry's docking program, you need the sum of all values
left in memory after the initialization program completes. (The entire 36-
bit address space begins initialized to the value 0 at every address.) In
the above example, only two values in memory are not zero - 101 (at address
7) and 64 (at address 8) - producing a sum of 165.
Execute the initialization program. What is the sum of all values left in
memory after it completes?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *

e = Exercise(14)

def set_bit(value, bit):
    return value | (1<<bit)

def make_mask(sets):
    m = 0
    for s in sets:
        m = set_bit(m, s)
    return m

lower36 = (2^36)-1

def parse_mask(mask):
    mask_falses = int(mask.replace("X", "1"), 2)
    mask_trues = int(mask.replace("X", "0"), 2)
    return (mask_trues, mask_falses, mask)

def apply_mask(mask, value):
    (trues, falses, _) = mask
    return (value | trues) & falses

print(apply_mask(parse_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"), 11))
assert apply_mask(parse_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"), 11) == 73


@e.transformer(map=True)
def xform(xs):
    var = xs[0]
    val = xs[2]
    if var == "mask":
        return "mask", parse_mask(val)
    else:
         return (int(var[4: -1]), val)




@e.part1()
def part1(xs):
    mask = None
    memory = dict()
    for operation, operand in xs.t:
        if operation == "mask":
            mask = operand
        else:
            memory[operation] = apply_mask(mask, operand)

    return sum(memory.values())


def find_candidates(pattern, i=0):
    if i == len(pattern):
        yield pattern
        return

    if pattern[i] == 'X':
        for ch in "01":
             # replace '?' with 0 and 1
            pattern[i] = ch

            yield from find_candidates(pattern, i + 1)

            # backtrack
            pattern[i] = 'X'

    else:
        # if the current character is 0 or 1, ignore it and
        # recur for the remaining pattern
        yield from find_candidates(pattern, i + 1)

def apply_mask2(mask, val):
    (trues, falses, xs) = mask
    xs = list(xs.replace("1", "0"))
    val |= trues
    for c in find_candidates(xs):
        yield val ^ int("".join(c), 2)


assert set(apply_mask2(parse_mask("000000000000000000000000000000X1001X"), 42)) == set([26, 27, 58, 59])

@e.part2()
def part2(xs):
    mask = None
    memory = dict()
    for operation, operand in xs.t:
        if operation == "mask":
            mask = operand
        else:
            for addr in apply_mask2(mask, operation):
                memory[addr] = operand

    return sum(memory.values())



e()
