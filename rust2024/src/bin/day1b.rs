const INPUT: &str = include_str!("../../inputs/day1.txt");

fn main() {
    let left_locs: Vec<i32> = INPUT
        .lines()
        .map(|line| {
            line.split_whitespace()
                .next()
                .unwrap()
                .parse::<i32>()
                .unwrap()
        })
        .collect();

    let right_locs: Vec<i32> = INPUT
        .lines()
        .map(|line| {
            line.split_whitespace()
                .last()
                .unwrap()
                .parse::<i32>()
                .unwrap()
        })
        .collect();

    let similarity: i32 = left_locs
        .into_iter()
        .map(|x| x * right_locs.iter().filter(|&y| *y == x).count() as i32)
        .sum();

    println!("List Similarity is {}", similarity)
}
