use std::fs;
type Point = (i64,i64);

fn find_min_cost(input: &str) -> Option<i64> {
    println!("{}",input);
    let lines: Vec<_> = input
        .replace("=", "+")
        .lines()
        .map(|x| {
            x.split(",")
                .filter_map(|x| x.split("+").last()?.parse::<i64>().ok())
                .collect::<Vec<_>>()
        })
        .collect();

    let ad: Point = (*lines[0].first().unwrap(), *lines[0].last().unwrap());
    let bd: Point = (*lines[1].first().unwrap(), *lines[1].last().unwrap());
    let target: Point = (
        10000000000000 + *lines[2].first().unwrap(),
        10000000000000 + *lines[2].last().unwrap(),
    );

    // Initialize minimum cost and solution
    let mut min_cost = i64::MAX;
    let mut best_solution = None;

    // Brute-force over possible values of a (number of times Button A is pressed)
    for a in 0..=target.0 / ad.0 {
        // Calculate remaining x and y after using Button A
        let remaining_x = target.0 - a * ad.0;
        let remaining_y = target.1 - a * ad.1;

        // Check if the remaining x and y can be satisfied by Button B
        if remaining_x >= 0
            && remaining_y >= 0
            && remaining_x % bd.0 == 0
            && remaining_y % bd.1 == 0
        {
            let b_x = remaining_x / bd.0;
            let b_y = remaining_y / bd.1;

            // Both b_x and b_y must be equal for Button B to work
            if b_x == b_y {
                let b = b_x; // Number of times Button B is pressed

                // Calculate the cost
                let cost = a * 3 + b;

                // Update minimum cost and solution
                if cost < min_cost {
                    min_cost = cost;
                    best_solution = Some(min_cost);
                }
            }
        }
    }

    best_solution
}

fn main() {
    let input = fs::read_to_string("../input/2024/13.txt").expect("Failed to read input file");
    let inputs = input.split("\n\n");
    let xs: Vec<_> = inputs.filter_map(|line| find_min_cost(line)).collect();
    println!("Part 1: {}", xs.iter().sum::<i64>());
}
