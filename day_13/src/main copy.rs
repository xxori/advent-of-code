use std::fs;

type Point = (u64, u64);

fn part_1(input: &str) -> Option<i32> {
    let lines: Vec<_> = input
        .replace("=", "+")
        .lines()
        .map(|x| {
            x.split(",")
                .filter_map(|x| x.split("+").last()?.parse::<u64>().ok())
                .collect::<Vec<_>>()
        })
        .collect();

    let a: Point = (*lines[0].first().unwrap(), *lines[0].last().unwrap());
    let b: Point = (*lines[1].first().unwrap(), *lines[1].last().unwrap());
    let dest: Point = (10000000000000+*lines[2].first().unwrap(), 10000000000000+*lines[2].last().unwrap());

    let (a1, a2) = a;
    let (b1, b2) = b;
    let (x, y) = dest;

    let mut min_cost = None;

    // Iterate over possible values of `m` for `a`
    for m in 0_u64.. {
        let mx = m.checked_mul(a1)?;
        let my = m.checked_mul(a2)?;

        if mx > x || my > y {
            break; // Stop when `m * a1` or `m * a2` exceeds the target
        }

        let rem_x = x.checked_sub(mx)?;
        let rem_y = y.checked_sub(my)?;

        if let Some(n) = solve_linear_diophantine(b1, b2, rem_x, rem_y) {
            let cost = 3 * m as i32 + n as i32;
            min_cost = Some(min_cost.map_or(cost, |current: i32| current.min(cost)));
        }
    }

    min_cost
}

// Solve for `n` given the remainder constraints and the coefficients of `b`
fn solve_linear_diophantine(b1: u64, b2: u64, rem_x: u64, rem_y: u64) -> Option<u64> {
    if rem_x % b1 == 0 && rem_y % b2 == 0 {
        let n_x = rem_x / b1;
        let n_y = rem_y / b2;
        if n_x == n_y {
            return Some(n_x);
        }
    }
    None
}

fn main() {
    let input = fs::read_to_string("../input/2024/13.txt").expect("Failed to read input file");
    let inputs = input.split("\n\n");
    let xs: Vec<i32> = inputs.filter_map(|line| part_1(line)).collect();
    println!("Part 1: {}", xs.iter().sum::<i32>());
}