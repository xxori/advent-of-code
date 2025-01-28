use std::fs;
use rayon::prelude::*;

fn possible(target: u64, partial: u64, nums: &[u64]) -> bool {
    match nums {
        [] => partial == target,
        [h, t @ ..] => {
            if partial > target {return false;}
            let ndigits = 10_u64.pow(h.ilog10() + 1);
            possible(target, partial + h, t)
                || possible(target, partial * h, t)
                || possible(target, ndigits * partial + h, t)
        }
    }
}

fn main() {
    let f = fs::read_to_string("../input/2024/7.txt").unwrap();
    let lines = f.lines().par_bridge().map(|x| {
        let mut it = x.split(":");
        let target: u64 = it.next().unwrap().parse().unwrap();
        let nums = it
            .next()
            .unwrap()
            .split_whitespace()
            .filter_map(|x| x.parse::<u64>().ok())
            .collect::<Vec<_>>();
        (target, nums)
    });
    let p2: u64 = lines
        .filter(|(target, nums)| possible(*target, 0, &nums[..]))
        .map(|x|x.0).sum();
    println!("Part2 {}", p2);
}
