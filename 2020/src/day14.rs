/*
***** --- Day 14: Docking Data --- *****
As your ferry approaches the sea port, the captain asks for your help
again. The computer system that runs this port isn't compatible with the
docking program on the ferry, so the docking parameters aren't being
correctly initialized in the docking program's memory.
After a brief inspectxion, you discover that the sea port's computer system
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
 */
use regex::Regex;

type Mask = (u64, u64);

#[derive(Debug, Copy, Clone)]
pub enum Operation {
    SetMask(Mask),
    SetMem(u64, u64),
}

use Operation::*;

fn parse_mask(input: &str) -> Mask {
    let mut mask: Mask = (0, 0);
    for (i, c) in input.bytes().rev().enumerate() {
	match c {
            b'0' => mask.0 &= !(1 << i),
	    b'1' => mask.1 |= 1 << i,
            _ => {}
	}
    }
    mask
}

fn parse(input: &str) -> Operation {
    lazy_static! {
        static ref RE: Regex = Regex::new(r"^(?:(?P<mask>mask)|(?:(?:mem\[)(?P<loc>\d+)(?:\]))) = (?P<val>[\dX]+)").unwrap();
    }
    let caps = RE.captures(input).unwrap();
    let operation = caps.name("mask").or(caps.name("loc")).unwrap().as_str();
    let operand = caps.name("val").unwrap().as_str();
    match operation {
	"mask" => SetMask(parse_mask(operand)),
	_ => SetMem(operation.parse().unwrap(), operand.parse().unwrap())
    }
}

#[aoc_generator(day14)]
pub fn input_generator(input: &str) -> Vec<Operation> {
    input
        .lines()
        .map(parse)
	.collect()
}


use std::collections::HashMap;
use bit_field::BitField;

struct Machine {
    memory: HashMap<u64, u64>,
    mask: Mask,
}

impl Machine {
    fn new() -> Machine {
	Machine { memory: HashMap::new(), mask: (0, 0) }
    }

    fn sum(&self) -> u64 {
	self.memory.values().fold(0, |a, b| a + b)
    }
}

fn apply_mask((zeros, ones): Mask, val: u64) -> u64 {
    (val & zeros) | ones
}

#[aoc(day14, part1)]
pub fn part1(input: &[Operation]) -> u64 {
    let mut m = Machine::new();
    for o in input {
	match o {
	    SetMask(x) => m.mask = *x,
	    SetMem(x, y) => {
		let val = apply_mask(m.mask, *y);
		m.memory.insert(*x, val);
	    }
	}
    }
    m.sum()
}

const LIMIT_36_BITS: u64 = u64::max_value() >> (64 - 36);
#[aoc(day14, part2)]
pub fn part2(input: &[Operation]) -> u64 {
    let mut m = Machine::new();
    for o in input {
	match o {
	    SetMask(x) => m.mask = *x,
	    SetMem(addr, y) => {
		let (and, or) = m.mask;
		let floating_base = or | !and;
		let base_addr = (addr | or) & floating_base;
		let mut floating = floating_base;
		loop {
                    let floating_inverted = (!floating) & LIMIT_36_BITS;
                    let floating_address = base_addr | floating_inverted;
                    m.memory.insert(floating_address, *y);

		    if floating & LIMIT_36_BITS == LIMIT_36_BITS {
                        break;
                    }
                    floating += 1;
                    floating |= floating_base;
		}

	    }
	}
    }
    m.sum()
}
