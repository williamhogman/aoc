pub type Fish = u8;
use std::mem;

type Counter = usize;

#[derive(Clone)]
pub struct FishCounter {
    fish: [Counter; 9],
    buf: [Counter; 9],
}

impl FishCounter {
    pub fn from(fish: [Counter; 9]) -> Self {
        Self {
            fish,
            buf: unsafe { mem::uninitialized() }
        }
    }
    pub fn new(input: &[Fish]) -> Self {
        let mut fish = [0; 9];
        for f in input {
            fish[*f as usize] += 1;
        }
        let buf = unsafe { mem::uninitialized() };
        FishCounter { fish, buf}
    }
    pub fn count(&self) -> Counter {
        self.fish.iter().sum()
    }
    pub fn next_round(&mut self) {
        for i in 0..8 {
            self.buf[i] = self.fish[i + 1];
        }
        self.buf[6] += self.fish[0];
        self.buf[8] = self.fish[0];
        mem::swap(&mut self.fish, &mut self.buf);
    }
}

#[aoc_generator(day6)]
pub fn input_generator(input: &str) -> [Counter; 9] {
    let mut data = [0; 9];
    for x in input.split(",").map(|l| l.parse::<u8>().unwrap()) {
        data[x as usize] += 1;
    }
    data
}

fn solve(rounds: usize, fish: &[Counter; 9]) -> Counter {
    let mut fish_counter = FishCounter::from(fish.clone());
    for i in 0..rounds {
        fish_counter.next_round();
    }
    fish_counter.count()
}

#[aoc(day6, part1)]
fn solve_part1(input: &[Counter; 9]) -> Counter {
    solve(80, input)
}

#[aoc(day6, part2)]
fn solve_part2(input: &[Counter; 9]) -> Counter {
    solve(256, input)
}



