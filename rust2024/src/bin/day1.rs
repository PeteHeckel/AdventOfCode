const INPUT: &str = include_str!("../../inputs/day1.txt");

fn main() {
    let mut left_locs: Vec<i32> = INPUT
        .lines()
        .map(|line| {
            line.split_whitespace()
                .next()
                .unwrap()
                .parse::<i32>()
                .unwrap()
        })
        .collect();

    let mut right_locs: Vec<i32> = INPUT
        .lines()
        .map(|line| {
            line.split_whitespace()
                .last()
                .unwrap()
                .parse::<i32>()
                .unwrap()
        })
        .collect();

    left_locs.sort();
    right_locs.sort();

    let sum: i32 = left_locs
        .into_iter()
        .zip(right_locs.into_iter())
        .map(|x| (x.0 - x.1).abs())
        .sum();
    println!("List Difference is {}", sum);
}
