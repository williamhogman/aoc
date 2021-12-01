#[aoc_generator(day1)]
pub fn input_generator(input: &str) -> Vec<u32> {
    input
        .lines()
        .map(|l| l.parse().unwrap())
	.filter(|x| *x < 2021)
	.collect()
}

const DESIRED_VAL: u32 = 2020;

#[aoc(day1, part1)]
pub fn part1(input: &[u32]) -> u32 {
    let n = input.len();
    for i in 0..n {
	for j in i+1..n {
	    if input[i] + input[j] == DESIRED_VAL {
		return input[i] * input[j]
	    }
	}
    }
    unreachable!()
}

#[aoc(day1, part1, sort)]
pub fn part1_sort(input: &[u32]) -> u32 {
    let mut sorted = input.to_owned();
    sorted.sort_unstable();
    let n = sorted.len();
    for i in 0..n {
	let target = DESIRED_VAL - sorted[i];
	if let Ok(_) = sorted[i..].binary_search(&target) {
	    return target * sorted[i]
	}
    }
    unreachable!()
}

#[aoc(day1, part1, twopointers)]
pub fn part1_twopointers(input: &[u32]) -> u32 {
    let mut sorted = input.to_owned();
    sorted.sort_unstable();
    let mut left = 0;
    let mut right = sorted.len() - 1;
    while left < right {
	let sum = sorted[left] + sorted[right];
	if sum == DESIRED_VAL {
	    return sorted[left] * sorted[right];
	} else if sum < DESIRED_VAL {
	    left += 1
	} else {
	    right -= 1
	}
    }

    unreachable!()
}

#[aoc(day1, part2)]
pub fn part2_naive(input: &[u32]) -> u32 {
    let n = input.len();
    for i in 0..n {
	for j in i+1..n {
	    for k in  j+2..n {
		if input[i] + input[j] + input[k] == DESIRED_VAL {
		    return input[i] * input[j] * input[k]
		}
	    }
	}
    }
    unreachable!()
}

#[aoc(day1, part2, sort)]
pub fn part2_sort(input: &[u32]) -> u32 {
    let mut sorted = input.to_owned();
    sorted.sort_unstable();
    let n = sorted.len();
    for i in 0..n {
	for j in i+1..n {
	    let so_far = sorted[i] + sorted[j];
	    if so_far > DESIRED_VAL {
		continue;
	    }
	    let target = DESIRED_VAL - so_far;
	    if let Ok(_) = sorted[i..].binary_search(&target) {
		return target * sorted[i] * sorted[j]
	    }
	}
    }
    unreachable!()
}


#[aoc(day1, part2, two_pointers)]
pub fn part2_two_pointers(input: &[u32]) -> u32 {
    let mut sorted = input.to_owned();
    sorted.sort_unstable();
    let n = sorted.len();
    for i in 0..n {
	let mut right = n - 1;
	let mut left = i + 1;
	while left < right {
	    let sum = sorted[i] + sorted[left] + sorted[right];
	    if sum == DESIRED_VAL {
		return sorted[left] * sorted[i] * sorted[right];
	    } else if sum < DESIRED_VAL {
		left += 1;
	    } else {
		right -= 1;
	    };
	}
    }
    unreachable!()
}
