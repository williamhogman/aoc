use bitvec::BitArr;
use bitvec::prelude::*;

pub type Arr = BitArr!(for 12, in Lsb0, u16);
pub type Card = [u16; 12];

#[aoc_generator(day3)]
fn gen(data: &str) -> Vec<Arr> {
  data.lines().map(|line| parse_item(line)).collect()
}

fn parse_item(s: &str) -> Arr {
    let mut bv = Arr::zeroed();
    for (i, v) in s.chars().enumerate() {
        if v == '1' {
            bv.set(i, true);
        } else if v == '0' {
            bv.set(i, false);
        } else {
            unreachable!("")
        }
    }
    return bv
}

#[aoc(day3, part1)]
pub fn solve_part1(input: &[Arr]) -> i32 {
    let mut arr: Card = Default::default();
    let mut arr_z: Card = Default::default();
    for i in input {
        for (idx, v) in i.iter().enumerate() {
            arr[idx as usize] += if v == true { 1 } else { 0 };
            arr_z[idx as usize] += if v == false { 1 } else { 0 };
        }
    }
    
    let mut result1 = 0;
    let mut r1 = Arr::zeroed();
    let mut r2 = Arr::zeroed();
    let mut result2 = 0;
    for i in 0..arr.len() {
        r1.set(i, arr[i] >= arr_z[i]);
        r2.set(i, arr[i] <= arr_z[i]);
    }
    println!("{} {}", r1, r2);
    result1 * result2
}

