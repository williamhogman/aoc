use std::cmp::{max, min};

#[aoc_generator(day7)]
pub fn input_generator(input: &str) -> Vec<isize> {
    let mut res: Vec<isize> = input.split(',').map(|x| x.parse::<isize>().unwrap()).collect();
    res.sort_unstable();
    res
}

#[aoc(day7, part1)]
pub fn solve_part1(input: &[isize]) -> isize {
    let n: isize = input.len().try_into().unwrap();
    let mut minimal = std::isize::MAX;
    for i in (0..=n).rev() {
        let s = input.iter().map(|x| max(i, *x) - min(i, *x)).sum();
        minimal = min(minimal, s);
    }
    minimal
}

#[aoc(day7, part2)]
pub fn solve_part2(input: &[isize]) -> isize {
    let n: isize = input.len().try_into().unwrap();
    let mut minimal = std::isize::MAX;
    for i in (0..=n).rev() {
        let s = input.iter()
            .map(|x| max(i, *x) - min(i, *x))
            .map(|x| x*(x + 1) /2)
            .sum();
        minimal = min(minimal, s);
    }
    minimal
}