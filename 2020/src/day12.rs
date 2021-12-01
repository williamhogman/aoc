/*
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
 */

use std::ops::{Mul, AddAssign};

pub enum Command {
    S(i16),
    E(i16),
    R(u8),
    F(i16)
}

use Command::*;

#[derive(Copy, Debug, Clone)]
struct VV {
    x: i16,
    y: i16,
}

impl VV {
    const ORIGIN: VV = Self{x: 0, y: 0};
    const EAST: VV = Self {x: 1, y: 0};
    const ONE: VV = Self {x: 1, y: 1};

    fn origin() -> Self {
	Self::ORIGIN.clone()
    }
    fn due_east() -> Self {
	Self::EAST.clone()
    }

    fn new(x: i16, y: i16) -> Self {
	Self{x: x, y: y}
    }

    pub fn rot(&mut self, turns: u8) {
	if turns > 1 {
	    self.x = -self.x;
	    self.y = -self.y;
	}
	if turns % 2 == 1 {
	    let swp = self.x;
	    self.x = self.y;
	    self.y = -swp;
	}
    }
    fn abs(&self) -> i16 {
	self.x.abs() + self.y.abs()
    }
}



impl AddAssign for VV {
    fn add_assign(&mut self, other: Self) {
        *self = Self {
            x: self.x + other.x,
            y: self.y + other.y,
        };
    }
}

impl AddAssign<&Command> for VV {
    fn add_assign(&mut self, other: &Command) {
	match other {
	    E(x) => self.x += x,
	    S(y) => self.y += y,
	    R(r) => self.rot(*r),
	    _ => unreachable!(),
	}
    }
}

impl AddAssign<Command> for VV {
    fn add_assign(&mut self, other: Command) {
	match other {
	    E(x) => self.x += x,
	    S(y) => self.y += y,
	    R(r) => self.rot(r),
	    _ => unreachable!(),
	}
    }
}




impl Mul<i16> for VV {
    type Output = Self;
    fn mul(self, rhs: i16) -> Self::Output {
	return Self{x: self.x * rhs, y: self.y * rhs};
    }
}


#[aoc_generator(day12)]
pub fn input_generator(input: &str) -> Vec<Command> {
    input
        .lines()
        .map(|l| (l.chars().next().unwrap(), l[1..].parse::<i16>().unwrap()))
	.map(|(c, n)| match c {
	    'N' => S(-n),
	    'S' => S(n),
	    'W' => E(-n),
	    'E' => E(n),
	    'L' => R((4 - (n / 90)) as u8),
	    'R' => R((n / 90) as u8),
	    'F' => F(n),
	    'B' => F(-n),
	    _ => unreachable!()
	})
	.collect()
}

struct Frame {
    pub coords: VV,
    pub heading: VV,
}

impl Frame {
    pub fn new(heading: VV) -> Self {
	Self{coords: VV::origin(), heading: heading}
    }

    pub fn modify_coords(&mut self, c: Command) {
	if let F(x) = c {
	    self.coords += self.heading * x;
	} else {
	    self.coords += c;
	}
    }

    pub fn modify_heading(&mut self, c: Command) {
	self.heading += c
    }

    pub fn dist(&self) -> i16 {
	self.coords.abs()
    }
}
