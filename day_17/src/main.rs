use std::cell::RefCell;
use std::fs;
use rayon::prelude::*;

fn part_1(input: &str, ain: Option<u32>) -> Vec<u32> {
    let lines: Vec<_> = input.split('\n').collect();
    // println!("lines {:?}",lines);
    let abc: Vec<_> = lines[0..=2]
        .iter()
        .filter_map(|x| x.split(": ").last().and_then(|y| y.parse::<u32>().ok()))
        .collect();
    // println!("abc {:?}",abc);
    let instructions: Vec<_> = lines
        .last()
        .unwrap()
        .split(": ")
        .last()
        .unwrap()
        .split(",")
        .filter_map(|x| x.parse::<u32>().ok())
        .collect();
    // println!("instructions {:?}",instructions);
    let mut a = ain.unwrap_or(abc[0]);
    let mut b = abc[1];
    let mut c = abc[2];
    let mut pc: u32 = 0;

    let out: RefCell<Vec<u32>> = RefCell::new(vec![]);
    const OPS: [fn(u32, u32, u32, u32, u32, u32, &RefCell<Vec<u32>>) -> (u32, u32, u32, u32); 8] = [
        |pc: u32, _oplit: u32, opcomb: u32, a: u32, b: u32, c: u32, _out| {
            (pc + 2, a / 2_u32.pow(opcomb), b, c)
        },
        |pc, oplit, _opcomb, a, b, c, _out| (pc + 2, a, b ^ oplit, c),
        |pc, _oplit, opcomb, a, _b, c, _out| (pc + 2, a, opcomb % 8, c),
        |pc, oplit, _opcomb, a, b, c, _out| (if a == 0 { pc + 2 } else { oplit }, a, b, c),
        |pc, _oplit, _opcomb, a, b, c, _out| (pc + 2, a, b ^ c, c),
        |pc, _oplit, opcomb, a, b, c, out: &RefCell<Vec<u32>>| {
            out.borrow_mut().push(opcomb % 8);
            (pc + 2, a, b, c)
        },
        |pc, _oplit, opcomb, a, _b, c, _out| (pc + 2, a, a / 2_u32.pow(opcomb), c),
        |pc, _oplit, opcomb, a, b, _c, _out| (pc + 2, a, b, a / 2_u32.pow(opcomb)),
    ];

    while (pc as usize) < instructions.len() - 1 {
        let ins = instructions[pc as usize];
        let oplit = instructions[pc as usize + 1];
        let opcomb = vec![0, 1, 2, 3, a, b, c][oplit as usize];
        // println!("ins {} oplit {} opcomb {} a {} b {} c {} pc {}",ins,oplit,opcomb,a,b,c,pc);
        (pc, a, b, c) = OPS[ins as usize](pc, oplit, opcomb, a, b, c, &out);
    }
    // println!("{:?}",out.take());
    return out.take();
}

fn part_2(input: &str) -> u32 {
    let lines: Vec<_> = input.split('\n').collect();
    let instructions: Vec<_> = lines
        .last()
        .unwrap()
        .split(": ")
        .last()
        .unwrap()
        .split(",")
        .filter_map(|x| x.parse::<u32>().ok())
        .collect();

    let p1 = |ain| {
        let mut a = ain;
        let mut b = 0;
        let mut c = 0;
        let mut pc = 0;
        let out: RefCell<Vec<u32>> = RefCell::new(vec![]);
        const OPS: [fn(u32, u32, u32, u32, u32, u32, &RefCell<Vec<u32>>) -> (u32, u32, u32, u32);
            8] = [
            |pc, _oplit, opcomb, a, b, c, _out| (pc + 2, a / 2_u32.pow(opcomb), b, c),
            |pc, oplit, _opcomb, a, b, c, _out| (pc + 2, a, b ^ oplit, c),
            |pc, _oplit, opcomb, a, _b, c, _out| (pc + 2, a, opcomb % 8, c),
            |pc, oplit, _opcomb, a, b, c, _out| (if a == 0 { pc + 2 } else { oplit }, a, b, c),
            |pc, _oplit, _opcomb, a, b, c, _out| (pc + 2, a, b ^ c, c),
            |pc, _oplit, opcomb, a, b, c, out| {
                out.borrow_mut().push(opcomb % 8);
                (pc + 2, a, b, c)
            },
            |pc, _oplit, opcomb, a, _b, c, _out| (pc + 2, a, a / 2_u32.pow(opcomb), c),
            |pc, _oplit, opcomb, a, b, _c, _out| (pc + 2, a, b, a / 2_u32.pow(opcomb)),
        ];

        while (pc as usize) < instructions.len() - 1 {
            let ins = instructions[pc as usize];
            let oplit = instructions[pc as usize + 1];
            let opcomb = vec![0, 1, 2, 3, a, b, c][oplit as usize];
            (pc, a, b, c) = OPS[ins as usize](pc, oplit, opcomb, a, b, c, &out);
        }
        return out.take();
    };

    return (0..=u32::MAX).par_bridge().find_first(|x| p1(*x) == instructions).unwrap();
}

fn main() {
    let input = fs::read_to_string("../input/2024/17.txt").expect("Failed to read input file");
    println!("{:?}", part_1(&input, None));
    println!("{:?}",part_2(&input));
}
