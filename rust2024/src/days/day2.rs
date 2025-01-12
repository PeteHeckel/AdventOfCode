const INPUT: &str = include_str!("../../inputs/day2.txt");

fn safety_check(line: Vec<u32>) -> bool {
    let safety_check_1: bool = line.iter().is_sorted() || line.iter().rev().is_sorted();
    let safety_check_2: bool = line
        .windows(2)
        .map(|w| w[1].abs_diff(w[0]))
        .all(|diff| diff >= 1 && diff <= 3);

    safety_check_1 && safety_check_2
}

pub fn main() {
    println!("Day2");

    let ans: [u32; 2] = INPUT_DATA.lines().fold([0, 0], |mut acc, line| {
        let nums: Vec<u32> = line
            .rsplit(' ')
            .map(|word| word.parse::<u32>().unwrap())
            .collect();

        let damped_safety_check = nums
            .iter()
            .enumerate()
            .fold(vec![], |mut acc, (i, _)| {
                let mut popped = nums.clone();
                popped.remove(i);
                acc.push(popped);
                acc
            })
            .iter()
            .any(|num_line| safety_check(num_line.to_vec()));

        if safety_check(nums) {
            acc[0] += 1
        }
        if damped_safety_check {
            acc[1] += 1
        }

        acc
    });

    println!("Part 1: {}", ans[0]);
    println!("Part 2: {}", ans[1]);
}
