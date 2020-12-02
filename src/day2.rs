extern crate regex;

use regex::Regex;

pub struct PasswordRule {
    min: u8,
    max: u8,
    target: char,
    password: String,
}

impl PasswordRule {
    fn is_valid(&self) -> bool {
	let mut n = 0;
	for c in self.password.chars() {
	    if c == self.target {
		n += 1;
	    }
	}
	n >= self.min && n <= self.max
    }

    fn is_valid_part_two(&self) -> bool {
	let min_ok = self.password.chars().nth((self.min - 1).into()).map(|c| c == self.target).unwrap();
	let max_ok = self.password.chars().nth((self.max - 1).into()).map(|c| c == self.target).unwrap();
	(min_ok || max_ok) && !(min_ok && max_ok)
    }
}

fn parse(text: &str) -> PasswordRule {
    lazy_static! {
        static ref RE: Regex = Regex::new(r"(\d+)-(\d+) (\w): (\w+)").unwrap();
    }

    let caps = RE.captures(text).unwrap();

    PasswordRule {
	min: caps.get(1).unwrap().as_str().parse().unwrap(),
	max: caps.get(2).unwrap().as_str().parse().unwrap(),
	target: caps.get(3).unwrap().as_str().chars().nth(0).unwrap(),
	password: caps.get(4).unwrap().as_str().to_owned(),
    }
}

#[aoc_generator(day2)]
pub fn input_generator(input: &str) -> Vec<PasswordRule> {
    input
        .lines()
        .map(parse)
	.collect()
}

#[aoc(day2, part1)]
pub fn day2(input: &[PasswordRule]) -> usize {
    input.iter()
	.map(|r| r.is_valid())
	.filter(|r| *r == true)
	.count()
}

#[aoc(day2, part2)]
pub fn day2_part2(input: &[PasswordRule]) -> usize {
    input.iter()
	.map(|r| r.is_valid_part_two())
	.filter(|r| *r == true)
	.count()
}
