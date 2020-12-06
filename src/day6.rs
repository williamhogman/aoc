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
pub fn input_generator(input: &str) -> Vec<String> {
    input.split_terminator("\n\n").map(|x| x.to_owned()).collect()
}

use std::collections::BTreeSet;

#[aoc(day6, part1)]
pub fn part1(input: &[String]) -> usize {
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
pub fn part2(input: &[String]) -> usize {
    input.iter().map(|l| {
	let sets: Vec<BTreeSet<char>> = l.split_terminator("\n")
	    .map(|x| x.chars().collect::<BTreeSet<char>>())
	    .collect();
	sets[0].iter().filter(|k| sets.iter().all(|s| s.contains(k))).count()
    }).fold(0, |a, b| a + b)
}

use bitvec::prelude::*;

#[aoc(day6, part1, opt)]
pub fn part1_opt(input: &[String]) -> usize {
    let mut sum = 0;
    for l in input {
	let l = l.as_bytes();
	let mut arr = bitarr![Msb0, u8; 0; 26];
	for b in l {
	    if *b == 10u8 {
		continue
	    }
	    unsafe {
		arr.set_unchecked((*b - 97u8).into(), true);
	    }

	}
	println!("{:?} ({}, {})", arr, arr.count_zeros(), arr.count_ones());
	sum += arr.count_ones();
    }
    sum
}
