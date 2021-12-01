/*
***** --- Day 24: Lobby Layout --- *****
Your raft makes it to the tropical island; it turns out that the small crab
was an excellent navigator. You make your way to the resort.
As you enter the lobby, you discover a small problem: the floor is being
renovated. You can't even reach the check-in desk until they've finished
installing the new tile floor.
The tiles are all hexagonal; they need to be arranged in a hex_grid with a
very specific color pattern. Not in the mood to wait, you offer to help
figure out the pattern.
The tiles are all white on one side and black on the other. They start with
the white side facing up. The lobby is large enough to fit whatever pattern
might need to appear there.
A member of the renovation crew gives you a list of the tiles that need to
be flipped over (your puzzle input). Each line in the list identifies a
single tile that needs to be flipped by giving a series of steps starting
from a reference tile in the very center of the room. (Every line starts
from the same reference tile.)
Because the tiles are hexagonal, every tile has six neighbors: east,
southeast, southwest, west, northwest, and northeast. These directions are
given in your list, respectively, as e, se, sw, w, nw, and ne. A tile is
identified by a series of these directions with no delimiters; for example,
esenee identifies the tile you land on if you start at the reference tile
and then move one tile east, one tile southeast, one tile northeast, and
one tile east.
Each time a tile is identified, it flips from white to black or from black
to white. Tiles might be flipped more than once. For example, a line like
esew flips a tile immediately adjacent to the reference tile, and a line
like nwwswee flips the reference tile itself.
Here is a larger example:
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
In the above example, 10 tiles are flipped once (to black), and 5 more are
flipped twice (to black, then back to white). After all of these
instructions have been followed, a total of 10 tiles are black.
Go through the renovation crew's list and determine which tiles they need
to flip. After all of the instructions have been followed, how many tiles
are left with the black side up?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
 */

use regex::Regex;
use std::ops::{Add};
use std::iter::Sum;
use std::cmp::Ordering;

#[derive(PartialEq, Eq, Clone, Copy, Debug, Hash)]
pub struct Hex(i32, i32, i32);

impl Ord for Hex {
    fn cmp(&self, other: &Self) -> Ordering {
	self.0.cmp(&other.0)
	    .then_with(|| self.1.cmp(&other.1))
	    .then_with(|| self.2.cmp(&other.2))
    }
}

impl PartialOrd for Hex {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
	Some(self.cmp(&other))
    }
}



impl Add for Hex {
    type Output = Self;

    fn add(self, other: Self) -> Self {
        Self(self.0 + other.0, self.1 + other.1, self.2 + other.2)
    }
}

impl Sum for Hex {
    fn sum<I: Iterator<Item=Hex>>(iter: I) -> Self {
                iter.fold(Hex(0, 0, 0), Add::add)
    }
}

fn parse_line(line: &str) -> Hex {
    lazy_static! {
	static ref RE: Regex = Regex::new(r"e|se|sw|w|nw|ne").unwrap();
    }
    RE.find_iter(line).map(|x| match x.as_str() {
	"nw" => Hex(1, 0, -1),
	"ne" => Hex(1, -1, 0),
	"e" => Hex(0, -1, 1),
	"se" => Hex(-1, 0, 1),
	"sw" => Hex(-1, 1, 0),
	"w" => Hex(0, 1, -1),
	&_ => unreachable!(),
    }).sum()
}


static NEIGHBORS: [Hex; 6] = [
    Hex(1, 0, -1),
    Hex(1, -1, 0),
    Hex(0, -1, 1),
    Hex(-1, 0, 1),
    Hex(-1, 1, 0),
    Hex(0, 1, -1),
];

#[aoc_generator(day24)]
pub fn input_generator(input: &str) -> Vec<Hex> {
    input
        .lines()
        .map(parse_line)
	.collect()
}

#[aoc(day24, part1)]
pub fn part1(input: &[Hex]) -> usize {
    let mut input = input.to_vec();
    input.sort_unstable();
    let mut i = 0;
    let mut sum = 0;
    while i < input.len() {
	let mut j = i + 1;
	while j < input.len() && input[i] == input[j] {
	    j += 1;
	}
	sum += (i - j) % 2;
	i = j;
    }
    sum
}

use std::collections::HashSet;

fn load_initial(input: &[Hex]) -> HashSet<Hex> {
    let mut s = HashSet::with_capacity(input.len());
    let mut input = input.to_vec();
    input.sort_unstable();
    let mut i = 0;
    let mut sum = 0;
    while i < input.len() {
	let mut j = i + 1;
	while j < input.len() && input[i] == input[j] {
	    j += 1;
	}
	if (i - j) % 2 == 1 {
	    s.insert(input[i]);
	}
	i = j;
    }
    s
}

#[aoc(day24, part2)]
pub fn part2(input: &[Hex]) -> usize {
    let mut blacks = load_initial(input);
    let mut updates = HashSet::new();
    let mut to_consider = blacks.clone();

    for i in 0..100 {
	for h in to_consider.iter() {
	    for n in &NEIGHBORS {
		to_consider.insert(*h + *n);
	    }
	}

	for h in to_consider.iter() {
	    let ns = NEIGHBORS.iter()
		.map(|x| *h + *x)
		.filter(|x| blacks.contains(x))
		.count();
	    if blacks.contains(&h) {
		if (ns == 0 || ns > 2) {
		    updates.insert(h);
		}
	    }  else {
		if (ns == 2) {
		    updates.insert(h);
		}
	    }
	}

	to_consider.clear();
	for x in updates {
	    if blacks.contains(&x) {
		blacks.remove(&x);
	    } else {
		blacks.insert(*x);
	    }
	    to_consider.insert(*x);
	}
	updates.clear();
    }

    blacks.len()
}
