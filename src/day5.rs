/*
***** --- Day 5: Binary Boarding --- *****
You board your plane only to discover a new problem: you dropped your
boarding pass! You aren't sure which seat is yours, and all of the flight
attendants are busy with the flood of people that suddenly made it through
passport control.
You write a quick program to use your phone's camera to scan all of the
nearby boarding passes (your puzzle input); perhaps you can find your seat
through process of elimination.
Instead of zones_or_groups, this airline uses binary space partitioning to
seat people. A seat might be specified like FBFBBFFRLR, where F means
"front", B means "back", L means "left", and R means "right".
The first 7 characters will either be F or B; these specify exactly one of
the 128 rows on the plane (numbered 0 through 127). Each letter tells you
which half of a region the given seat is in. Start with the whole list of
rows; the first letter indicates whether the seat is in the front (0
through 63) or the back (64 through 127). The next letter indicates which
half of that region the seat is in, and so on until you're left with
exactly one row.
For example, consider just the first seven characters of FBFBBFFRLR:
    * Start by considering the whole range, rows 0 through 127.
    * F means to take the lower half, keeping rows 0 through 63.
    * B means to take the upper half, keeping rows 32 through 63.
    * F means to take the lower half, keeping rows 32 through 47.
    * B means to take the upper half, keeping rows 40 through 47.
    * B keeps rows 44 through 47.
    * F keeps rows 44 through 45.
    * The final F keeps the lower of the two, row 44.
The last three characters will be either L or R; these specify exactly one
of the 8 columns of seats on the plane (numbered 0 through 7). The same
process as above proceeds again, this time with only three steps. L means
to keep the lower half, while R means to keep the upper half.
For example, consider just the last 3 characters of FBFBBFFRLR:
    * Start by considering the whole range, columns 0 through 7.
    * R means to take the upper half, keeping columns 4 through 7.
    * L means to take the lower half, keeping columns 4 through 5.
    * The final R keeps the upper of the two, column 5.
So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.
Every seat also has a unique seat ID: multiply the row by 8, then add the
column. In this example, the seat has ID 44 * 8 + 5 = 357.
Here are some other boarding passes:
    * BFFFBBFRRR: row 70, column 7, seat ID 567.
    * FFFBBBFRRR: row 14, column 7, seat ID 119.
    * BBFFBBFRLL: row 102, column 4, seat ID 820.
As a sanity check, look through your list of boarding passes. What is the
highest seat ID on a boarding pass?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
*/
#[aoc_generator(day5)]
pub fn input_generator(input: &str) -> Vec<(Vec<bool>, Vec<bool>)> {
    input
        .lines()
        .map(|l| l.chars().map(|c| match c { 'R' | 'B' => true, 'F'|'L' => false, _ => unreachable!() }).collect::<Vec<bool>>())
	.map(|l| (l.iter().take(l.len() - 3).map(|x| *x).collect(), l.iter().rev().take(3).map(|x| *x).collect()))
	.collect()
}

fn mid(mn: u8, mx: u8) -> u8 {
    (mn / 2) + (mx / 2)
}

fn find(path: &[bool], range_min: u8, range_max: u8) -> u8 {
    let (mut mn, mut mx) = (range_min, range_max);
    for p in path[..path.len() - 1].iter() {
	let m = mid(mn, mx);
	if *p {
	    mn = m + 1
	} else {
	    mx = m
	}
    }
    if path[path.len() - 1] {
	mn
    } else {
	mx
    }
}


#[aoc(day5, part1)]
pub fn part1(input: &[(Vec<bool>, Vec<bool>)]) -> usize {
    input.iter().map(|(rs, ss)| ((find(rs, 0, 127)) as usize * 8) + (find(ss, 0, 7)) as usize).max().unwrap()
}
