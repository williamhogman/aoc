use lazy_static::lazy_static;
use regex::Regex;
use std::convert::From;
pub type Num = i32;
#[derive(Eq, PartialEq, Clone, Hash, Debug, PartialOrd, Ord)]
pub struct Line(Point, Point);
#[derive(Eq, PartialEq, Clone, Hash, Debug, PartialOrd, Ord, Copy)]
pub struct Point(Num, Num);
use std::cmp::{PartialEq, Eq, min, max, Ordering};
use std::collections::HashMap;
use std::collections::BTreeMap;

impl Point {
    fn id(&self) -> Num {
        self.0 * 1000 + self.1
    }
    fn signum(&self) -> Point {
        Point(self.0.signum(), self.1.signum())
    }
    fn abs(&self) -> Point {
        Point(self.0.abs(), self.1.abs())
    }
    fn max_val(&self) -> Num {
        max(self.0, self.1)
    }
}

impl std::ops::Add for Point {
    type Output = Point;
    fn add(self, other: Point) -> Point {
        Point(self.0 + other.0, self.1 + other.1)
    }
}

impl std::ops::Sub for Point {
    type Output = Point;
    fn sub(self, other: Point) -> Point {
        Point(self.0 - other.0, self.1 - other.1)
    }
}

impl std::ops::Mul<Num> for Point {
    type Output = Point;
    fn mul(self, other: Num) -> Point {
        Point(self.0 * other, self.1 * other)
    }
}

fn ord_to_num(ord: Ordering) -> Num {
    match ord {
        Ordering::Less => -1,
        Ordering::Equal => 0,
        Ordering::Greater => 1,
    }
}
impl From<(Num, Num)> for Point {
    fn from((x, y): (Num, Num)) -> Point {
        Point(x, y)
    }
}

impl From<(Point, Point)> for Line {
    fn from((p1, p2): (Point, Point)) -> Line {
        Line(min(p1, p2), max(p1, p2))
    }
}

impl Line {
    fn is_horizontal(&self) -> bool {
        let Self(Point(x1, y1), Point(x2, y2)) = self;
        x1 == x2
    }
    fn is_vertical(&self) -> bool {
        let Self(Point(x1, y1), Point(x2, y2)) = self;
        y1 == y2
    }
    fn diff(&self) -> Point {
        self.0 - self.1
    }
    fn is_diagonal(&self) -> bool {
        let Point(dx, dy) = self.diff().abs();
        dx == dy
    }
    fn is_acceptable_part1(&self) -> bool {
        self.is_horizontal() || self.is_vertical()
    }
    fn is_acceptable_part2(&self) -> bool {
        self.is_acceptable_part1() || self.is_diagonal()
    }
    fn direction(&self) -> Point {
        (self.1 - self.0).signum()
    }

    fn length(&self) -> Num {
        self.diff().abs().max_val()
    }

    fn iter(&self) -> LineIter<'_> {
        LineIter {
            line: self,
            i: 0,
        }
    }
}

struct LineIter<'a> {
    line: &'a Line,
    i: Num,
}


impl<'a> Iterator for LineIter<'a> {
    type Item = Point;
    fn next(&mut self) -> Option<Self::Item> {
        if self.i > self.line.length() + 1 {
            return None;
        }
        let p = self.line.0 + self.line.direction() * self.i;
        self.i += 1;
        Some(p)
    }
}




#[aoc_generator(day5)]
fn gen(input: &str) -> Vec<Line> {
    lazy_static! {
    static ref RE: Regex = Regex::new(r"(?m)^(\d+),(\d+) -> (\d+),(\d)+$").unwrap();
    }
    RE.captures_iter(input).map(|cap| {
      let (x1, y1, x2, y2) = (cap[1].parse::<Num>().unwrap(), cap[2].parse::<Num>().unwrap(), cap[3].parse::<Num>().unwrap(), cap[4].parse::<Num>().unwrap());
      let p1: Point = (x1, y1).into();
      let p2: Point = (x2, y2).into();
      (p1, p2).into()
    }).collect()
}

#[aoc(day5, part1)]
fn part1(input: &[Line]) -> usize {
    let mut hm: BTreeMap<Point, u8> = BTreeMap::new();
    let points = input.iter()
        .filter(|x| x.is_acceptable_part1())
        .flat_map(|line| line.iter());
    let mut cnt = 0;
    for point in points {
        let mut e = hm.entry(point).or_insert(0);
        *e = e.saturating_add(1);
        if *e == 2 {
            cnt += 1;
        }
    }
    cnt
}

#[aoc(day5, part2)]
fn part2(input: &[Line]) -> usize {
    0
}