import numpy as np


def part_1(input: str) -> int:
    matrix = np.array(list(map(list, input.split("\n"))))
    d1 = [
        "".join(matrix.diagonal(i).tolist())
        for i in range(-len(matrix) + 1, len(matrix))
    ]
    d2 = [
        "".join(matrix[::-1, :].diagonal(i).tolist())
        for i in range(-len(matrix) + 1, len(matrix))
    ]
    cands = (
        d1
        + d2
        + input.split("\n")
        + ["".join(i.tolist()) for i in np.transpose(matrix)]
    )
    cands += list(map(lambda x: x[::-1], cands))
    return sum(map(lambda x: x.count("XMAS"), cands))


def part_2(input: str) -> int:
    grid = input.split("\n")
    res = 0
    for r in range(1, len(grid) - 1):
        for c in range(1, len(grid[0]) - 1):
            if grid[r][c] == "A":
                ul = grid[r - 1][c - 1]
                ur = grid[r - 1][c + 1]
                bl = grid[r + 1][c - 1]
                br = grid[r + 1][c + 1]
                if ((ul == "M" and br == "S") or (ul == "S" and br == "M")) and (
                    (ur == "M" and bl == "S") or (ur == "S" and bl == "M")
                ):
                    res += 1
    return res


with open("input/2024/4.txt") as f:
    content = f.read()
    print(part_1(content))
    print(part_2(content))
