/*
***** --- Day 6: Custom Customs --- *****
As your flight approaches the regional airport where you'll switch to a
much larger plane, customs_declaration_forms are distributed to the
passengers.
The form asks a series of 26 yes-or-no questions marked a through z. All
you need to do is identify the questions for which anyone in your group
answers "yes". Since your group is just you, this doesn't take very long.
However, the person sitting next to you seems to be experiencing a language
barrier and asks if you can help. For each of the people in their group,
you write down the questions for which they answer "yes", one per line. For
example:
abcx
abcy
abcz
In this group, there are 6 questions to which anyone answered "yes": a, b,
c, x, y, and z. (Duplicate answers to the same question don't count extra;
each question counts at most once.)
Another group asks for your help, then another, and eventually you've
collected answers from every group on the plane (your puzzle input). Each
group's answers are separated by a blank line, and within each group, each
person's answers are on a single line. For example:
abc

a
b
c

ab
ac

a
a
a
a

b
This list represents answers from five groups:
    * The first group contains one person who answered "yes" to 3
      questions: a, b, and c.
    * The second group contains three people; combined, they answered "yes"
      to 3 questions: a, b, and c.
    * The third group contains two people; combined, they answered "yes" to
      3 questions: a, b, and c.
    * The fourth group contains four people; combined, they answered "yes"
      to only 1 question, a.
    * The last group contains one person who answered "yes" to only 1
      question, b.
In this example, the sum of these counts is 3 + 3 + 3 + 1 + 1 = 11.
For each group, count the number of questions to which anyone answered
"yes". What is the sum of those counts?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
*/
#[aoc_generator(day6)]
pub fn input_generator(input: &str) -> String {
    input.to_owned()
}

use std::collections::BTreeSet;

#[aoc(day6, part1)]
pub fn part1(input: &str) -> usize {
    let input: Vec<String> = input.split_terminator("\n\n").map(|x| x.to_owned()).collect();
    let mut qs = BTreeSet::new();
    let mut sum = 0;
    for l in input {
	for c in l.chars() {
	    if c != '\n' {
		qs.insert(c);
	    }
	}
	sum += qs.len();
	qs.clear();
    }
    sum
}

#[aoc(day6, part2)]
pub fn part2(input: &str) -> usize {
    let input: Vec<String> = input.split_terminator("\n\n").map(|x| x.to_owned()).collect();
    input.iter().map(|l| {
	let sets: Vec<BTreeSet<char>> = l.split_terminator("\n")
	    .map(|x| x.chars().collect::<BTreeSet<char>>())
	    .collect();
	sets[0].iter().filter(|k| sets.iter().all(|s| s.contains(k))).count()
    }).fold(0, |a, b| a + b)
}

use bitvec::prelude::*;

const NEW_LINE: u8 = 10;
const OFFSET: u8 = 97;

#[aoc(day6, part1, opt)]
pub fn part1_opt(input: &str) -> usize {
    let mut sum = 0;
    let input = input.as_bytes();
    let mut arr = bitarr![Msb0, u32; 0; 26];
    let n = input.len();
    for i in 0..n {
	let b = input[i];
	if b == NEW_LINE {
	    if i + 1 < n && input[i + 1] == NEW_LINE {
		sum += arr.count_ones();
		arr.set_all(false);
	    }
	} else {
	    unsafe {
		arr.set_unchecked((b - OFFSET) as usize, true);
	    }
	}
    }
    sum += arr.count_ones();
    //println!("{:?} ({}, {})", arr, arr.count_zeros(), arr.count_ones());
    sum
}

use bit_field::BitField;

#[aoc(day6, part1, opt_bf)]
pub fn part1_opt_bf(input: &str) -> u32 {
    let mut sum: u32 = 0;
    let input = input.as_bytes();
    let mut arr: u32 = 0;
    let mut was_nl = false;
    for b in input {
	let b = *b;
	if b == NEW_LINE {
	    if was_nl {
		sum += arr.count_ones();
		arr = 0;
	    }
	    was_nl = true;
	} else {
	    was_nl = false;
	    let i = b - OFFSET;
	    arr.set_bit(i.into() , true);
	}
    }
    sum += arr.count_ones();
    sum
}


const BF_MAX: u32 = 134217727; // 2^27 - 1

#[aoc(day6, part2, opt)]
pub fn part2_opt(input: &str) -> u32 {
    let mut sum: u32 = 0;
    let input = input.as_bytes();
    let mut arr: u32 = 0;
    let mut grp: u32 = BF_MAX;
    let mut was_nl = false;
    for b in input {
	let b = *b;
	if b == NEW_LINE {
	    if !was_nl {
		grp &= arr;
		arr = 0;

	    } else {
		sum += grp.count_ones();
		grp = BF_MAX;
	    }
	    was_nl = true;
	} else {
	    was_nl = false;
	    let i = b - OFFSET;
	    arr.set_bit(i.into() , true);
	}
    }
    grp &= arr;
    sum += grp.count_ones();
    sum
}

#[aoc(day6, part2, opt_vec)]
pub fn part2_opt_vec(input: &str) -> u32 {
    let mut sum: u32 = 0;
    let input = input.as_bytes();
    let mut arr: u32 = 0;
    let mut grp: u32 = BF_MAX;
    let mut was_nl = false;
    for b in input.iter().map(|b| b.saturating_sub(OFFSET - 1)) {
	if b == 0 {
	    if !was_nl {
		grp &= arr;
		arr = 0;

	    } else {
		sum += grp.count_ones();
		grp = BF_MAX;
	    }
	    was_nl = true;
	} else {
	    was_nl = false;
	    arr.set_bit((b - 1).into() , true);
	}
    }
    grp &= arr;
    sum += grp.count_ones();
    sum
}
