/*
***** --- Day 9: Encoding Error --- *****
With your neighbor happily enjoying their video game, you turn your
attention to an open data port on the little screen in the seat in front of
you.
Though the port is non-standard, you manage to connect it to your computer
through the clever use of several paperclips. Upon connection, the port
outputs a series of numbers (your puzzle input).
The data appears to be encrypted with the eXchange-Masking Addition System
(XMAS) which, conveniently for you, is an old cypher with an important
weakness.
XMAS starts by transmitting a preamble of 25 numbers. After that, each
number you receive should be the sum of any two of the 25 immediately
previous numbers. The two numbers will have different values, and there
might be more than one such pair.
For example, suppose your preamble consists of the numbers 1 through 25 in
a random order. To be valid, the next number must be the sum of two of
those numbers:
    * 26 would be a valid next number, as it could be 1 plus 25 (or many
      other pairs, like 2 and 24).
    * 49 would be a valid next number, as it is the sum of 24 and 25.
    * 100 would not be valid; no two of the previous 25 numbers sum to 100.
    * 50 would also not be valid; although 25 appears in the previous 25
      numbers, the two numbers in the pair must be different.
Suppose the 26th number is 45, and the first number (no longer an option,
as it is more than 25 numbers ago) was 20. Now, for the next number to be
valid, there needs to be some pair of numbers among 1-19, 21-25, or 45 that
add up to it:
    * 26 would still be a valid next number, as 1 and 25 are still within
      the previous 25 numbers.
    * 65 would not be valid, as no two of the available numbers sum to it.
    * 64 and 66 would both be valid, as they are the result of 19+45 and
      21+45 respectively.
Here is a larger example which only considers the previous 5 numbers (and
has a preamble of length 5):
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
In this example, after the 5-number preamble, almost every number is the
sum of two of the previous 5 numbers; the only number that does not follow
this rule is 127.
The first step of attacking the weakness in the XMAS data is to find the
first number in the list (after the preamble) which is not the sum of two
of the 25 numbers before it. What is the first number that does not have
this property?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
 */
use itertools::Itertools;

#[aoc_generator(day9)]
pub fn input_generator(input: &str) -> Vec<u64> {
    input
        .lines()
        .map(|l| l.parse().unwrap())
	.collect()
}

#[aoc(day9, part1)]
pub fn part1(input: &[u64]) -> u64 {
    input.windows(26)
	.filter(|wnd| wnd[0..25].iter().combinations(2).all(|x| x[0] + x[1] != wnd[25]))
		.map(|wnd| wnd[25])
		.next().unwrap()
}

#[aoc(day9, part1, opt)]
pub fn part1_opt(input: &[u64]) -> u64 {
    for wnd in input.windows(26) {
	let mut adds_up = false;
	'outer: for i in 0..25 {
	    for j in i+1..25 {
		if wnd[i] + wnd[j] == wnd[25] {
		    adds_up = true;
		    break 'outer;
		}
	    }
	}
	if !adds_up {
	    return wnd[25];
	}
    }
    unreachable!()
}

#[aoc(day9, part2)]
pub fn part2(input: &[u64]) -> u64 {
    let target: u64 = 217430975;
    let mut i = 0;
    let mut j = 1;
    let mut current = input[0] + input[1];
    while j < input.len() {
	if current < target {
	    j += 1;
	    current += input[j];
	}
	if current > target {
	    current -= input[i];
	    i += 1;
	}
	if current == target {
	    return input[i..j].iter().min().unwrap() + input[i..j].iter().max().unwrap()
	}
    }
    unreachable!();
}


use std::collections::VecDeque;

#[aoc(day9, part2, queue)]
pub fn part2_queue(input: &[u64]) -> u64 {
    let mut deq = VecDeque::with_capacity(25);
    let target: u64 = 217430975;
    let mut current = 0;
    for val in input {
	deq.push_back(val);
	current += val;
	while current > target {
	    current -= deq.pop_front().unwrap();
	}
	if current == target {
	    return deq.iter().minmax().into_option().map(|(a, b)| *a + *b).unwrap()
	}
    }
    unreachable!();
}
