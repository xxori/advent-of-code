WIDTH = 101
HEIGHT = 103


def part_1(input):
    res = []
    for sx, sy, vx, vy in input:
        res.append(((sx + vx * 100) % WIDTH, (sy + vy * 100) % HEIGHT))

    q1 = len([p for p in res if p[0] < WIDTH // 2 and p[1] < HEIGHT // 2])
    q2 = len([p for p in res if p[0] > WIDTH // 2 and p[1] < HEIGHT // 2])
    q3 = len([p for p in res if p[0] < WIDTH // 2 and p[1] > HEIGHT // 2])
    q4 = len([p for p in res if p[0] > WIDTH // 2 and p[1] > HEIGHT // 2])
    return q1 * q2 * q3 * q4


def part_2(input):
    for i in range(1000000):
        res = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]
        for sx, sy, vx, vy in input:
            res[(sy + vy * i) % HEIGHT][(sx + vx * i) % WIDTH] = "x"
        for r in res:
            if "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" in "".join(r):
                return i


if __name__ == "__main__":
    with open("input/2024/14.txt") as f:
        inp = f.read().split("\n")
        coords = []
        for line in inp:
            c = line.strip().split(" ")
            p = [int(x) for x in c[0][2:].split(",")]
            v = [int(x) for x in c[1][2:].split(",")]
            coords.append((p[0], p[1], v[0], v[1]))
        print("Part 1:", part_1(coords))
        print("Part 2:", part_2(coords))
