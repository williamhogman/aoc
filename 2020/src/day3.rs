/*
***** --- Day 3: Toboggan Trajectory --- *****
With the toboggan login problems resolved, you set off toward the airport.
While travel by toboggan might be easy, it's certainly not safe: there's
very minimal steering and the area is covered in trees. You'll need to see
which angles will take you near the fewest trees.
Due to the local geology, trees in this area only grow on exact integer
coordinates in a grid. You make a map (your puzzle input) of the open
squares (.) and trees (#) you can see. For example:
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
These aren't the only trees, though; due to something you read about once
involving arboreal genetics and biome stability, the same pattern repeats
to the right many times:
..##.........##.........##.........##.........##.........##.......  --->
#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....  --->
.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........#.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...##....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
You start on the open square (.) in the top-left corner and need to reach
the bottom (below the bottom-most row on your map).
The toboggan can only follow a few specific slopes (you opted for a cheaper
model that prefers rational numbers); start by counting all the trees you
would encounter for the slope right 3, down 1:
From your starting position at the top-left, check the position that is
right 3 and down 1. Then, check the position that is right 3 and down 1
from there, and so on until you go past the bottom of the map.
The locations you'd check in the above example are marked here with O where
there was an open square and X where there was a tree:
..##.........##.........##.........##.........##.........##.......  --->
#..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
.#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........X.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...#X....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
In this example, traversing the map using this slope would cause you to
encounter 7 trees.
Starting at the top-left corner of your map and following a slope of right
3 and down 1, how many trees would you encounter?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
 */
use bitvec::prelude::*;


pub struct GameMap {
    per_row: usize,
    map: BitVec,
    trees: Vec<usize>,
}

impl GameMap {
    fn get(&self, (row, col): (usize, usize)) -> bool {
	let col_fix = col % self.per_row;
	if row == 0 {
	    self.map[col_fix]
	} else {
	    self.map[row * self.per_row + col_fix]
	}
    }

    fn in_bounds(&self, (row, _): (usize, usize)) -> bool {
	row * self.per_row < self.map.len() as usize
    }

    fn on_path_trees(&self, (downs, rights): (usize, usize)) -> usize {
	let delta = downs * self.per_row + rights;
	let mut cur = delta;
	let mut on_path = 0;
	let mut tree_index = 0;
	while cur < self.map.len() {
	    if let Ok(new_i) = self.trees[tree_index..].binary_search(&(cur + delta)) {
		tree_index = new_i;
		on_path += 1;
	    }
	    cur += delta;
	}
	on_path
    }

    fn on_paths(&self, paths: &[(usize, usize)]) -> usize {
	if paths.len() == 0 {
	    return 0
	}
	let mut deltas: Vec<usize> = paths.iter().map(|(downs, rights)| downs * self.per_row + rights).collect();
	deltas.sort_unstable();
	let mut counts = vec![0; deltas.len()];
	let mut i = 0;
	for tree in self.trees.iter() {
	    for (i, d) in deltas.iter().enumerate() {
		if tree % d == 0 {
		    counts[i] += 1
		}
	    }
	}
	counts.iter().fold(1, |a, b| a * b)
    }
}

#[aoc_generator(day3)]
pub fn input_generator(input: &str) -> Box<GameMap> {
    let per_row = (input.find('\n').unwrap() as usize) + 1;
    let mut bv = BitVec::with_capacity(input.len());
    let mut counter = 0;
    let mut trees = Vec::new();
    for c in input.chars() {
	if c == '\n' {
	    continue
	}
	let is_tree = c == '#';
	bv.push(is_tree);

	if is_tree {
	    trees.push(counter);
	}
	counter += 1;
    }
    Box::new(GameMap{per_row: per_row, map: bv, trees: trees})
}

fn for_slope(input: &GameMap, down: usize, right: usize) -> usize {
    let mut coords: (usize, usize) = (0, 0);
    let mut n: usize = 0;
    while input.in_bounds(coords) {
	if input.get(coords) {
	    n += 1;
	}
	coords.0 += down;
	coords.1 += right;
    }
    n
}


#[aoc(day3, part1)]
pub fn part1(input: &GameMap) -> usize {
    for_slope(&input, 1, 3)
}

#[aoc(day3, part2)]
pub fn part2(input: &GameMap) -> usize {
    /*
    Right 1, down 1.
    Right 3, down 1. (This is the slope you already checked.)
    Right 5, down 1.
    Right 7, down 1.
    Right 1, down 2.
     */
    let attempts = vec!((1,1), (1, 3), (1, 5), (1, 7), (2, 1));

    attempts.iter()
	.map(|(a, b)| for_slope(&input, *a, *b))
	.fold(1, |a, b| a * b)
}


#[aoc(day3, part1, opt)]
pub fn part1_opt(input: &GameMap) -> usize {
    input.on_path_trees((1, 3))
}

#[aoc(day3, part2, opt)]
pub fn part2_opt(input: &GameMap) -> usize {
    let attempts = vec!((1,1), (1, 3), (1, 5), (1, 7), (2, 1));
    input.on_paths(&attempts)
}
