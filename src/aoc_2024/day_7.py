import time
import math


def isPossible(target: int, nums: tuple[int]) -> bool:
    n = len(nums)
    dp = {}

    def dfs(index: int, acc: int) -> bool:
        if index == n:
            return acc == target
        if (index, acc) in dp:
            return dp[(index, acc)]

        h = nums[index]
        result = dfs(index + 1, acc + h) or dfs(index + 1, acc * h)
        dp[(index, acc)] = result
        return result

    return dfs(0, 0)


def parse(input: str) -> list[tuple[int, tuple[int]]]:
    lines = input.split("\n")
    res = []
    for line in lines:
        t, r = line.split(":")
        t = int(t)
        r = tuple(int(n) for n in r.split(" ") if n != "")
        res.append((t, r))
    return res


def part_1(input: list[tuple[int, tuple[int]]]) -> int:
    i = filter(lambda x: isPossible(*x), input)
    return sum(x[0] for x in i)


def isPossible_2(target: int, nums: tuple[int]) -> bool:
    n = len(nums)
    dp = {}

    def dfs(index: int, acc: int) -> bool:
        if index == n:
            return acc == target
        if (index, acc) in dp:
            return dp[(index, acc)]

        h = nums[index]
        concat_acc = acc * (10 ** (math.floor(math.log10(h)) + 1)) + h
        result = (
            dfs(index + 1, acc + h)
            or dfs(index + 1, acc * h)
            or dfs(index + 1, concat_acc)
        )
        dp[(index, acc)] = result
        return result

    return dfs(0, 0)


def part_2(input: list[tuple[int, tuple[int]]]) -> int:
    i = filter(lambda x: isPossible_2(*x), input)
    return sum(x[0] for x in i)


with open("input/2024/7.txt") as f:
    content = f.read()
    bcache = time.time()
    inp = parse(content)
    acache = time.time()
    print("Parsing time ", acache - bcache)

    bp1 = time.time()
    p1 = part_1(inp)
    ap1 = time.time()
    print(p1)
    print("Part 1 time", ap1 - bp1)

    bp2 = time.time()
    p2 = part_2(inp)
    ap2 = time.time()
    print(p2)
    print("Part 2 time", ap2 - bp2)
