/*
***** --- Day 11: Seating System --- *****
Your plane lands with plenty of time to spare. The final leg of your
journey is a ferry that goes directly to the tropical island where you can
finally start your vacation. As you reach the waiting area to board the
ferry, you realize you're so early, nobody else has even arrived yet!
By modeling the process people use to choose (or abandon) their seat in the
waiting area, you're pretty sure you can predict the best place to sit. You
make a quick map of the seat layout (your puzzle input).
The seat layout fits neatly on a grid. Each position is either floor (.),
an empty seat (L), or an occupied seat (#). For example, the initial seat
layout might look like this:
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
Now, you just need to model the people who will be arriving shortly.
Fortunately, people are entirely predictable and always follow a simple set
of rules. All decisions are based on the number of occupied seats adjacent
to a given seat (one of the eight positions immediately up, down, left,
right, or diagonal from the seat). The following rules are applied to every
seat simultaneously:
    * If a seat is empty (L) and there are no occupied seats adjacent to
      it, the seat becomes occupied.
    * If a seat is occupied (#) and four or more seats adjacent to it are
      also occupied, the seat becomes empty.
    * Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.
After one round of these rules, every seat in the example layout becomes
occupied:
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
After a second round, the seats with four or more occupied adjacent seats
become empty again:
#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
This process continues for three more rounds:
#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
At this point, something interesting happens: the chaos stabilizes and
further applications of these rules cause no seats to change state! Once
people stop moving around, you count 37 occupied seats.
Simulate your seating area by applying the seating rules repeatedly until
no seats change state. How many seats end up occupied?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
 */

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Tile {
    Floor,
    Free,
    Taken,
}

type Point = (i16, i16);

pub struct Update(Point, Tile);

use array2d::Array2D;

#[aoc_generator(day11)]
pub fn input_generator(input: &str) -> Array2D<Tile> {
    let rows: Vec<Vec<Tile>> = input
        .lines()
        .map(|l| l.chars().map(|c| match c {
	    '.' => Tile::Floor,
	    'L' => Tile::Free,
	    '#' => Tile::Taken,
	    _ => unreachable!()
	}).collect())
	.collect();
    Array2D::from_rows(&rows)
}

static ADJACENT: &'static [Point] = &[
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    // (0, 0) but thats us
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
];

pub fn round(state: &Array2D<Tile>) -> Vec<Update> {
    let mut updates: Vec<Update> = Vec::with_capacity(50);
    for i in 0..state.num_rows() {
	for j in 0..state.num_columns() {
	    if state[(i, j)] == Tile::Floor {
		continue
	    }
	    let adj_taken = ADJACENT
		.iter()
		.map(|(a, b)| (i.wrapping_add(*a as usize), j.wrapping_add(*b as usize) ))
		.map(|(a, b)| *state.get(a as usize, b as usize).unwrap_or(&Tile::Floor))
		.filter(|a| *a == Tile::Taken)
		.count();
	    if state[(i, j)] == Tile::Free && adj_taken == 0 {
		updates.push(Update((i as i16, j as i16), Tile::Taken))
	    } else if adj_taken > 4  {
		updates.push(Update((i as i16, j as i16), Tile::Free))
	    }

	}
    }
    updates
}

#[aoc(day11, part1)]
pub fn part1(input: &Array2D<Tile>) -> usize {
    let mut state = input.clone();
    loop {
	let updates = round(&state);
	if updates.len() == 0 {
	    break
	}
	for Update((i, j), t) in updates {
	    state.set(i as usize, j as usize, t).unwrap()
	}
    }
    state.elements_row_major_iter().filter(|t| **t == Tile::Taken).count()
}
