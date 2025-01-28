use std::collections::HashMap;
use std::fs;

const N: usize = 70;

type Coord = (usize, usize);
fn min_heapify(pos: &mut HashMap<Coord, usize>, heap: &mut Vec<(usize, Coord)>, idx: usize) {
    let mut smallest = idx;
    let left = smallest * 2 + 1;
    let right = smallest * 2 + 2;
    if left < heap.len() && heap[left].0 < heap[smallest].0 {
        smallest = left;
    }
    if right < heap.len() && heap[right].0 < heap[smallest].0 {
        smallest = right;
    }
    if smallest != idx {
        pos.insert(heap[smallest].1, idx);
        pos.insert(heap[idx].1, smallest);
        heap.swap(smallest, idx);
        min_heapify(pos, heap, smallest);
    }
}
fn extract_min(pos: &mut HashMap<Coord, usize>, heap: &mut Vec<(usize, Coord)>) -> (usize, Coord) {
    let m = heap[0];
    let n = heap.len() - 1;
    heap.swap(0, n);
    heap.pop();
    if heap.len() != 0 {
        pos.insert(heap[0].1, 0);
        min_heapify(pos, heap, 0);
    }
    m
}
fn decrease_key(
    pos: &mut HashMap<Coord, usize>,
    heap: &mut Vec<(usize, Coord)>,
    v: Coord,
    dist: usize,
) {
    let mut i = pos[&v];
    heap[i].0 = dist;
    while i != 0 && heap[i].0 < heap[(i - 1) / 2].0 {
        pos.insert(heap[i].1, (i - 1) / 2);
        pos.insert(heap[(i - 1) / 2].1, i);
        heap.swap(i, (i - 1) / 2);
        i = (i - 1) / 2;
    }
}

fn dijkstra(map: &Vec<Vec<u8>>) -> usize {
    let mut pos: HashMap<Coord, usize> = HashMap::with_capacity((N + 1) * (N + 1));
    let mut heap: Vec<(usize, Coord)> = Vec::with_capacity((N + 1) * (N + 1));
    for r in 0..=N {
        for c in 0..=N {
            pos.insert((r, c), heap.len());
            heap.push((usize::MAX, (r, c)));
        }
    }
    heap[0] = (0, (0, 0));
    let mut dist = vec![vec![usize::MAX; N + 1]; N + 1];
    dist[0][0] = 0;

    while !heap.is_empty() {
        let m = extract_min(&mut pos, &mut heap);
        let (ur, uc) = m.1;
        let neighbors = [
            (ur.wrapping_add(1), uc),
            (ur.wrapping_sub(1), uc),
            (ur, uc.wrapping_add(1)),
            (ur, uc.wrapping_sub(1)),
        ];
        for (vr, vc) in neighbors {
            if vr <= N
                && vc <= N
                && map[vr][vc] == 0
                && pos.get(&(vr, vc)).is_some_and(|&x| x != usize::MAX)
                && dist[ur][uc] != usize::MAX
                && dist[ur][uc] + 1 < dist[vr][vc]
            {
                dist[vr][vc] = dist[ur][uc] + 1;
                decrease_key(&mut pos, &mut heap, (vr, vc), dist[ur][uc] + 1);
            }
        }
    }

    return dist[N][N];
}

fn main() {
    let input = fs::read_to_string("../input/2024/18.txt").expect("Failed to read input file");

    let mut map = vec![vec![0u8; N + 1]; N + 1];
    for line in input.lines().take(1024) {
        if let Some((c, r)) = line.split_once(',') {
            let c: usize = c.trim().parse().unwrap();
            let r: usize = r.trim().parse().unwrap();
            map[r][c] = 1;
        }
    }
    println!("Part 1: {}", dijkstra(&map));
    for line in input.lines().skip(1024) {
        if let Some((c, r)) = line.split_once(',') {
            let c: usize = c.trim().parse().unwrap();
            let r: usize = r.trim().parse().unwrap();
            map[r][c] = 1;
            if dijkstra(&map) == usize::MAX {
                println!("Part 2: {},{}", c, r);
                return;
            }
        }
    }
}
