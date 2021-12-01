/*
***** --- Day 8: Handheld Halting --- *****
Your flight to the major airline hub reaches cruising altitude without
incident. While you consider checking the in-flight menu for one of those
drinks that come with a little umbrella, you are interrupted by the kid
sitting next to you.
Their handheld_game_console won't turn on! They ask if you can take a look.
You narrow the problem down to a strange infinite loop in the boot code
(your puzzle input) of the device. You should be able to fix it, but first
you need to be able to run the code in isolation.
The boot code is represented as a text file with one instruction per line
of text. Each instruction consists of an operation (acc, jmp, or nop) and
an argument (a signed number like +4 or -20).
    * acc increases or decreases a single global value called the
      accumulator by the value given in the argument. For example, acc +7
      would increase the accumulator by 7. The accumulator starts at 0.
      After an acc instruction, the instruction immediately below it is
      executed next.
    * jmp jumps to a new instruction relative to itself. The next
      instruction to execute is found using the argument as an offset from
      the jmp instruction; for example, jmp +2 would skip the next
      instruction, jmp +1 would continue to the instruction immediately
      below it, and jmp -20 would cause the instruction 20 lines above to
      be executed next.
    * nop stands for No OPeration - it does nothing. The instruction
      immediately below it is executed next.
For example, consider the following program:
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
These instructions are visited in this order:
nop +0  | 1
acc +1  | 2, 8(!)
jmp +4  | 3
acc +3  | 6
jmp -3  | 7
acc -99 |
acc +1  | 4
jmp -4  | 5
acc +6  |
First, the nop +0 does nothing. Then, the accumulator is increased from 0
to 1 (acc +1) and jmp +4 sets the next instruction to the other acc +1 near
the bottom. After it increases the accumulator from 1 to 2, jmp -
4 executes, setting the next instruction to the only acc +3. It sets the
accumulator to 5, and jmp -3 causes the program to continue back at the
first acc +1.
This is an infinite loop: with this sequence of jumps, the program will run
forever. The moment the program tries to run any instruction a second time,
you know it will never terminate.
Immediately before the program would run an instruction a second time, the
value in the accumulator is 5.
Run your copy of the boot code. Immediately before any instruction is
executed a second time, what value is in the accumulator?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
 */
use rpds::HashTrieSet;
use std::iter::FromIterator;
use std::rc::Rc;

pub enum Instr {
    Nop(i16),
    Acc(i16),
    Jmp(i16),
}

impl Instr {
    fn flip(self) -> Instr {
	match self {
	    Instr::Nop(x) => Instr::Jmp(x),
	    Instr::Jmp(x) => Instr::Nop(x),
	    _ => self
	}
    }
}


#[derive(Clone)]
pub struct Machine {
    ic: u16,
    pub acc: i16,
    instrs: Rc<Vec<Instr>>,
    visited: HashTrieSet<u16>
}

impl PartialEq for Machine {
    fn eq(&self, other: &Self) -> bool {
        self.ic == other.ic
	    && self.acc == other.acc
	    && self.visited == other.visited
	    && Rc::ptr_eq(&self.instrs, &other.instrs)
    }
}

#[derive(PartialEq)]
enum MachineStatus {
    Eof,
    Running,
    CycleDetected,
    Forked(Box<Machine>)
}

impl Machine {
    fn new(v: Vec<Instr>) -> Machine {
	Machine{ ic: 0, acc: 0, instrs: Rc::new(v), visited: HashTrieSet::new() }
    }
    #[inline]
    fn run_one(&mut self) -> MachineStatus {
	if self.ic >= self.instrs.len() as u16 {
	    return MachineStatus::Eof
	}
	if self.visited.contains(&self.ic) {
	    return MachineStatus::CycleDetected
	}
	self.visited.insert_mut(self.ic);
	match self.instrs[self.ic as usize] {
	    Instr::Nop(_) => self.ic += 1,
	    Instr::Acc(x) => { self.acc += x; self.ic += 1; },
	    Instr::Jmp(x) => self.ic = self.ic.wrapping_add(x as u16),
	}
	MachineStatus::Running
    }
    fn run_many(&mut self) -> MachineStatus {
	loop {
	    match self.run_one() {
		MachineStatus::Running => continue,
		x => return x
	    }
	}
    }

    fn run_one_forking(&mut self) -> MachineStatus {
	if self.ic >= self.instrs.len() as u16 {
	    return MachineStatus::Eof
	}
	if self.visited.contains(&self.ic) {
	    return MachineStatus::CycleDetected
	}
	self.visited.insert_mut(self.ic);
	match self.instrs[self.ic as usize] {
	    Instr::Acc(x) => { self.acc += x; self.ic += 1; },
	    Instr::Nop(x) => {
		let mut forked = self.clone();
		forked.ic = self.ic.wrapping_add(x as u16); // jmp on fork
		self.ic += 1; // nop on self
	    }
	    Instr::Jmp(x) => {
		let mut forked = self.clone();
		self.ic = self.ic.wrapping_add(x as u16);
		forked.ic += 1;
	    }
	}
	MachineStatus::Running
    }

    fn run_many_forking(&mut self) -> i16 {
	loop {
	    match self.run_one_forking() {
		MachineStatus::CycleDetected => unreachable!(),
		MachineStatus::Running => continue,
		MachineStatus::Forked(mut m2) => {
		    println!("forked!");
		    if m2.run_many() == MachineStatus::Eof {
			return m2.acc;
		    }
		},
		MachineStatus::Eof => { return self.acc },
	    }
	}

    }
}



#[aoc_generator(day8)]
pub fn input_generator(input: &str) -> Machine {
    Machine::new(input
        .lines()
        .map(|l| {
	    let mut splitter = l.splitn(2, ' ');
	    let operator = splitter.next().unwrap();
	    let operand: i16 = splitter.next().unwrap().parse().unwrap();
	    match operator {
		"nop" => Instr::Nop(operand),
		"acc" => Instr::Acc(operand),
		"jmp" => Instr::Jmp(operand),
		_ => unreachable!()
	    }
	}).collect())
}


#[aoc(day8, part1)]
pub fn part1(input: &Machine) -> i16 {
    let mut input = input.clone();
    if input.run_many() == MachineStatus::CycleDetected {
	return input.acc;
    }
    unreachable!()
}

#[aoc(day8, part2)]
pub fn part2(input: &Machine) -> i16 {
    input.clone().run_many_forking()
}
