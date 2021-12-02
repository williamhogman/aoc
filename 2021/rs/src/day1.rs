
fn general_solution(data: &[i32], chunk_size: usize) -> i32 {
  let mut count = 0;
  for i in chunk_size..data.len() {
    if data[i] > data[i - chunk_size] {
      count += 1
    }
  }
  count
}

#[aoc_generator(day1)]
fn ints(data: &str) -> Vec<i32> {
  data.lines().map(|line| line.parse::<i32>().unwrap()).collect()
}

#[aoc(day1, part1)]
pub fn solve_part1(input: &[i32]) -> i32 {
  general_solution(input, 1)  
}

#[aoc(day1, part2)]
pub fn solve_part2(input: &[i32]) -> i32 {
  general_solution(input, 3)
}