extern crate regex;

use regex::Regex;
/*
***** --- Day 4: Passport Processing --- *****
You arrive at the airport only to realize that you grabbed your North Pole
Credentials instead of your passport. While these documents are extremely
similar, North Pole Credentials aren't issued by a country and therefore
aren't actually valid documentation for travel in most of the world.
It seems like you're not the only one having problems, though; a very long
line has formed for the automatic passport scanners, and the delay could
upset your travel itinerary.
Due to some questionable network security, you realize you might be able to
solve both of these problems at the same time.
The automatic passport scanners are slow because they're having trouble
detecting which passports have all required fields. The expected fields are
as follows:
    * byr (Birth Year)
    * iyr (Issue Year)
    * eyr (Expiration Year)
    * hgt (Height)
    * hcl (Hair Color)
    * ecl (Eye Color)
    * pid (Passport ID)
    * cid (Country ID)
Passport data is validated in batch files (your puzzle input). Each
passport is represented as a sequence of key:value pairs separated by
spaces or newlines. Passports are separated by blank lines.
Here is an example batch file containing four passports:
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884 hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013 eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
The first passport is valid - all eight fields are present. The second
passport is invalid - it is missing hgt (the Height field).
The third passport is interesting; the only missing field is cid, so it
looks like data from North Pole Credentials, not a passport at all! Surely,
nobody would mind if you made the system temporarily ignore missing cid
fields. Treat this "passport" as valid.
The fourth passport is missing two fields, cid and byr. Missing cid is
fine, but missing any other field is not, so this passport is invalid.
According to the above rules, your improved system would report 2 valid
passports.
Count the number of valid passports - those that have all required fields.
Treat cid as optional. In your batch file, how many passports are valid?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
 */

#[derive(Debug, Default)]
pub struct Passport {
    byr: Option<String>,
    iyr: Option<String>,
    eyr: Option<String>,
    hgt: Option<String>,
    hcl: Option<String>,
    ecl: Option<String>,
    pid: Option<String>,
    // cid is not used skip
    // cid: Option<String>,
}


impl Passport {
    fn set_field(&mut self, name: &str, value: &str) {
	let x = Some(value.to_string())
	match name {
	    "byr" => self.byr = x,
	    "iyr" => self.iyr = x,
	    "eyr" => self.eyr = x,
	    "hgt" => self.hgt = x,
	    "hcl" => self.hcl = x,
	    "ecl" => self.ecl = x,
	    "pid" => self.pid = x,
	    "cid" => {}
	    //"cid" => self.cid = Some(value.to_string()),
	    _ => unreachable!()
	}
    }
    pub fn is_valid(&self) -> bool {
	self.byr.is_some() && self.iyr.is_some() && self.eyr.is_some() && self.hgt.is_some() && self.hcl.is_some() && self.ecl.is_some() && self.pid.is_some()
    }

    fn is_byr_valid(&self) -> bool {
	self.byr.and_then(|x| x.parse::<usize>().ok()).filter(|x| between(*x, 1920, 2002)).is_some()
    }

    fn is_iyr_valid(&self) -> bool {
	self.iyr.and_then(|x| x.parse::<usize>().ok()).filter(|x| between(x, 2010, 2020)).is_some()
    }

    fn is_eyr_valid(&self) -> bool {
	self.eyr.and_then(|x| x.parse::<usize>().ok()).filter(|x| between(x, 2020, 2030)).is_some()
    }

    fn is_hgt_valid(&self) -> bool {
	self.hgt.and_then(|x| {
	    if hgt.ends_with("cm") {
		hgt.replace("cm", "").parse().ok().filter(|y| between(y, 150, 193))
	    } else if hgt.ends_with("in") {
		hgt.replace("in", "").parse().ok().filter(|y| between(y, 59, 76))
	    } else {
		None
	    }
	}).is_some()
    }

    pub fn is_hcl_valid(&self) -> bool {
	lazy_static! {
            static ref hcl_re: Regex = Regex::new(r"^#(?:[0-9a-fA-F]{3}){1,2}$").unwrap();
	}
	self.hcl.filter(|x| hcl_re.is_match(&hcl)).is_some()
    }

    pub fn is_ecl_valid(&self) -> bool {
	self.ecl.filter(|x| match &x[..] {
	    "amb" | "blu" | "brn" | "gry" | "grn" | "hzl" | "oth" => true,
	    _ => false
	}).is_some()
    }

    fn is_pid_valid(&self) -> bool {
	lazy_static! {
            static ref pid_re: Regex = Regex::new(r"^\d{9}$").unwrap();
	}
	self.pid.filter(|x| pid_re.is_match(&pid)).is_some()
    }

    pub fn is_p2_valid(&self) -> bool {
	self.is_valid() && self.is_eyr_valid() && self.is_byr_valid() && self.is_iyr_valid() && self.is_hgt_valid() && self.is_hcl_valid() && self.is_ecl_valid() && self.is_pid_valid()
    }
}

fn between(x: usize, min: usize, max: usize) -> bool {
    x >= min && x <= max
}


#[aoc_generator(day4)]
pub fn input_generator(input: &str) -> Vec<Passport> {
    input.split("\n\n").map(|l| {
	let pp = Passport{}
	l.split_whitespace()
	    .map(|x| x.trim())
	    .filter(|x| !x.is_empty())
	    .map(|f| {
		if let Some(i) = f.find(':') {
		    (&f[..i], &f[i+1..])
		} else {
		    unreachable!()
		}
	    })
	    .for_each(|(k, v)| {
		pp.set_field(k, v)
	    })
	    pp
    }).collect()
}


#[aoc(day4, part1)]
pub fn part1(input: &[Passport]) -> usize {
    input.iter().filter(|p| (*p).is_valid()).count()
}

#[aoc(day4, part2)]
pub fn part2(input: &[Passport]) -> usize {
    input.iter().filter(|p| (*p).is_p2_valid()).count()
}
