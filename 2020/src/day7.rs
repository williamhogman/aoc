/*
***** --- Day 7: Handy Haversacks --- *****
You land at the regional airport in time for your next flight. In fact, it
looks like you'll even have time to grab some food: all flights are
currently delayed due to issues in luggage processing.
Due to recent aviation regulations, many rules (your puzzle input) are
being enforced about bags and their contents; bags must be color-coded and
must contain specific quantities of other color-coded bags. Apparently,
nobody responsible for these regulations considered how long they would
take to enforce!
For example, consider the following rules:
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
These rules specify the required contents for 9 bag types. In this example,
every faded blue bag is empty, every vibrant plum bag contains 11 bags (5
faded blue and 6 dotted black), and so on.
You have a shiny gold bag. If you wanted to carry it in at least one other
bag, how many different bag colors would be valid for the outermost bag?
(In other words: how many colors can, eventually, contain at least one
shiny gold bag?)
In the above rules, the following options would be available to you:
    * A bright white bag, which can hold your shiny gold bag directly.
    * A muted yellow bag, which can hold your shiny gold bag directly, plus
      some other bags.
    * A dark orange bag, which can hold bright white and muted yellow bags,
      either of which could then hold your shiny gold bag.
    * A light red bag, which can hold bright white and muted yellow bags,
      either of which could then hold your shiny gold bag.
So, in this example, the number of bag colors that can eventually contain
at least one shiny gold bag is 4.
How many bag colors can eventually contain at least one shiny gold bag?
(The list of rules is quite long; make sure you get all of it.)
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
 */


/*
#[aoc_generator(day7)]
pub fn input_generator(input: &str) -> Vec<Rule> {
    lazy_static! {
	static ref RE: Regex = Regex::new(r"\s+bag[s]?(?:[\s,\.])?(?:contain)?\s*").unwrap();
	static ref RE_ITEM: Regex = Regex::new(r"^\s?(\d)+ (\w+ \w+)$").unwrap();
    }
    let mut idx = 9999;

        let mut next_id: u16 = 0;
        let (containers, contents) = input.lines().map(|x| RE.split(x)).map(|mut x| {
	    (x.next().unwrap(), x)
	}).unzip();

    let mut rules = containers.enumerate().map(|i, x| {
	(i, Rule{id: i, ..Default::default()})
    }).collect::<HashMap<Rule>>();

    for (i, row) in contents.enumerate() {
	for (j, c) in row.enumerate() {
	    if c.is_empty() || c == "no other" {
		continue
	    }
	    let caps = RE_ITEM.captures(c).unwrap();
	    let caps = RE_ITEM.captures(c).unwrap();
	    rule.counts[i as usize] = caps.get(1).and_then(|x| x.as_str().parse().ok()).unwrap();
	    let name = caps.get(2).unwrap().as_str();
	    let mut rule = rule.get()
	    rule.contains[i as usize] = *id;
	    rules[""].counts[j] = caps.get(1).and_then(|x| x.as_str().parse().ok()).unwrap();
	    rule.contains[j] = *id;
	}

    }
	let mut i: u8 = 0;
	for c in x {
	    println!("'{}'", c);
	    i += 1;
	}
	rule.n = i;
    1
    }).collect()

}

*/
/*#[aoc(day7, part1)]
pub fn part1(input: &[Rule]) -> u32 {
    unreachable!()
}*/
