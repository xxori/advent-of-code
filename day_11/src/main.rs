use std::{collections::HashMap, fs};

fn proc(cache: &mut HashMap<(u64, u8), u64>, n: u64, s: u8) -> u64 {
    if !cache.contains_key(&(n, s)) {
        let digs = if n == 0 { 1 } else { n.ilog10() + 1 };
        let r = match (s, n) {
            (0, _) => 1,
            (_, 0) => proc(cache, 1, s - 1),
            _ if digs % 2 == 0 => {
                let div = 10_u64.pow(digs / 2);
                proc(cache, n / div, s - 1) + proc(cache, n % div, s - 1)
            }
            _ => proc(cache, n * 2024, s - 1),
        };
        cache.insert((n, s), r);
    }
    *cache.get(&(n, s)).unwrap()
}

fn main() {
    let f = fs::read_to_string("../input/2024/11.txt").unwrap();
    let nums = f.split_whitespace().filter_map(|x| x.parse::<u64>().ok());
    let mut cache: HashMap<(u64, u8), u64> = HashMap::new();
    let r1 = nums.clone().map(|x| proc(&mut cache, x, 25)).sum::<u64>();
    let r2 = nums.map(|x| proc(&mut cache, x, 75)).sum::<u64>();
    println!("Part 1: {}", r1);
    println!("Part 2: {}", r2);
}
