type Counter = usize;

#[derive(Clone)]
pub struct FishCounter {
    fish: [Counter; 9],
}

impl FishCounter {
    pub fn from(fish: [Counter; 9]) -> Self {
        Self {
            fish,
        }
    }
    pub fn count(&self) -> Counter {
        self.fish.iter().sum()
    }
    #[inline]
    pub fn next_round(&mut self) {
        let spawned = self.fish[0];
        for i in 0..8 {
            self.fish[i] = self.fish[i + 1];
        }
        self.fish[6] += spawned;
        self.fish[8] = spawned;
    }
}

#[aoc_generator(day6)]
pub fn input_generator(input: &str) -> [usize; 9] {
    let mut data = [0; 9];
    for x in input.split(',').map(|l| l.parse::<u8>().unwrap()) {
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