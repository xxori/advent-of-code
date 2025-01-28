from functools import lru_cache
import numpy as np

point = tuple[int, int]


def part_1(input: str):
    lines = input.split("\n")
    a = tuple(int(x.split("+")[-1]) for x in lines[0].split(","))
    b = tuple(int(x.split("+")[-1]) for x in lines[1].split(","))
    dest = tuple(int(x.split("=")[-1]) for x in lines[2].split(","))

    @lru_cache(None)
    def proc(cur: point, cost: int) -> int | None:
        if cur == dest:
            return cost
        if cur[0] > dest[0] or cur[1] > dest[1]:
            return None

        tob = proc((cur[0] + b[0], cur[1] + b[1]), cost + 1)
        if tob:
            return tob

        toa = proc((cur[0] + a[0], cur[1] + a[1]), cost + 3)
        if toa:
            return toa
        return None

    return proc((0, 0), 0)


DEL = 1e-4

"""
ia + jb = k
la + mb = n

a = (k-jb)/i
l(k-jb)/i+mb = n
lk/i - ljb/i + mb = n
b(m-lj/i) = n-lk/i
b = (i/(mi-lj))((ni-lk)/i) = (ni-lk)/(mi-lj)
a = (n-mb)/l
"""

def line_to_point(line: str):
    return tuple(int(x.split("+")[-1]) for x in line.split(","))

def solve(input: str, offset: int):
    a,b,dest = [line_to_point(line) for line in input.replace("=","+").split("\n")]
    dest = (dest[0]+offset,dest[1]+offset)
    i,j,k = a[0],b[0],dest[0] # Two equations
    l,m,n = a[1],b[1],dest[1]

    numerB = n*i-l*k
    denomB = m*i - l*j
    if l == 0 or denomB == 0 or numerB % denomB != 0:
        return 0
    b = numerB // denomB
    numerA = n - m * b
    if numerA % l != 0:
        return 0
    a = numerA // l
    return 3 * a + b

# def solve(input: str, offset: int):
#     lines = input.split("\n")
#     a = tuple(int(x.split("+")[-1]) for x in lines[0].split(","))
#     b = tuple(int(x.split("+")[-1]) for x in lines[1].split(","))
#     dest = tuple(offset + int(x.split("=")[-1]) for x in lines[2].split(","))

#     coefs = np.array([[a[0], b[0]], [a[1], b[1]]])
#     consts = np.array(dest)

#     a, b = np.linalg.solve(coefs, consts)
#     ar, br = a.round(), b.round()
#     if abs(a - ar) < DEL and abs(b - br) < DEL:
#         return 3 * ar.astype(int) + br.astype(int)
#     return 0


if __name__ == "__main__":
    with open("input/2024/13.txt") as f:
        inputs = f.read().split("\n\n")
        p1 = [solve(line, 0) for line in inputs]
        p2 = [solve(line, 10000000000000) for line in inputs]
        print("Part 1:", sum(p1))
        print("Part 2:", sum(p2))
