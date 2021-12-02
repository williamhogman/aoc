use std::str::FromStr;
type Num = i32;

pub enum Command {
    Down(Num),
    Forward(Num)
}
use Command::*;

#[derive(Debug)]
pub enum ParsingError {
    BadCommand,
    BadNum
}

impl FromStr for Command {
    type Err = ParsingError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        use ParsingError::*;
        let (c, val) = s.trim().split_once(' ').ok_or(BadCommand)?;
        let n: Num = val.parse().map_err(|_| BadNum)?;
        match c.as_ref() {
            "forward" => Ok(Forward(n)),
            "down" => Ok(Down(n)),
            "up" => Ok(Down(-n)),
            _ => Err(BadCommand)
        }
    }
}

#[aoc_generator(day2)]
fn commands(data: &str) -> Vec<Command> {
  data.lines().map(|line| line.parse().unwrap()).collect()
}

trait Apply {
    fn apply(self: &Self, other: &Command) -> Self;
    fn origin() -> Self;
    fn summarize(self: &Self) -> Num;
}

fn apply_from_origin<T: Apply>(input: &[Command]) -> T {
    input.iter().fold(T::origin(), |acc, c| acc.apply(c))
}

type Coord2 = (Num, Num);

impl Apply for Coord2 {
    fn origin() -> Self {
        (0, 0)
    }
    fn apply(&self, c: &Command) -> Self {
        let (y, z) = *self;
        match c {
            Forward(n) => (y + n, z),
            Down(n) => (y, z + n)
        }
    }
    fn summarize(&self) -> Num {
        self.0 * self.1
    }
}

type Coord3 = (Num, Num, Num);
impl Apply for Coord3 {
    fn origin() -> Self {
        (0, 0, 0)
    }
    fn apply(&self, c: &Command) -> Self {
        let (y, z, aim) = *self;
        match c {
            Forward(n) => (y + n, z + (n * aim), aim),
            Down(n) => (y, z, aim + n)
        }
    }
    fn summarize(&self) -> Num {
        self.0 * self.1
    }
}

fn solve<T: Apply>(input: &[Command]) -> Num {
    apply_from_origin::<T>(input).summarize()
}

#[aoc(day2, part1)]
pub fn solve_part1(input: &[Command]) -> i32 {
    solve::<Coord2>(input)
}

#[aoc(day2, part2)]
pub fn solve_part2(input: &[Command]) -> i32 {
    solve::<Coord3>(input)
}
