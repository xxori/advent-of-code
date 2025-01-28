def part_1(input):
    lines = input.split("\n")
    instructions = [int(x) for x in lines[-1].split(":")[-1].strip().split(",")]
    out = []
    ops = [
        lambda pc, oplit, opcomb, a, b, c: (pc + 2, a // (2**opcomb), b, c),
        lambda pc, oplit, opcomb, a, b, c: (pc + 2, a, b ^ oplit, c),
        lambda pc, oplit, opcomb, a, b, c: (pc + 2, a, opcomb % 8, c),
        lambda pc, oplit, opcomb, a, b, c: (oplit if a else pc + 2, a, b, c),
        lambda pc, oplit, opcomb, a, b, c: (pc + 2, a, b ^ c, c),
        lambda pc, oplit, opcomb, a, b, c: (out.append(opcomb % 8), (pc + 2, a, b, c))[
            1
        ],
        lambda pc, oplit, opcomb, a, b, c: (pc + 2, a, a // (2**opcomb), c),
        lambda pc, oplit, opcomb, a, b, c: (pc + 2, a, b, a // (2**opcomb)),
    ]

    def process(pc: int, a: int, b: int, c: int) -> tuple[int, int, int, int]:
        ins = instructions[pc]
        oplit = instructions[pc + 1]
        opcomb = [0, 1, 2, 3, a, b, c][oplit]
        return ops[ins](pc, oplit, opcomb, a, b, c)

    a, b, c = [int(x.split(":")[-1].strip()) for x in lines[:3]]
    pc = 0

    while pc < len(instructions) - 1:
        pc, a, b, c = process(pc, a, b, c)

    return out


"""
2,4,1,5,7,5,1,6,0,3,4,0,5,5,3,0

b = a % 8 (last 3 bits)
b ^= 5
c = a // 2^b
b ^= 6
a = a // 2^3
b ^= c
print b % 8
repeat while a != 0

Each loop will take 3 bits and print something based off them and rest of string.
We can thus reverse engineer in reverse order, building up different possible inputs.
"""


def part_2(input):
    lines = input.split("\n")
    instructions = [int(x) for x in lines[-1].split(":")[-1].strip().split(",")]

    def o(a):
        b = a % 8
        b ^= 5
        c = a // (2**b)
        b ^= 6
        b ^= c
        return b % 8

    curs = [0]
    for t in instructions[::-1]:
        nc = []
        for cur in curs:
            for i in range(8):
                if o((cur << 3) + i) == t:
                    nc.append((cur << 3) + i)
        curs = nc
    return min(curs)


if __name__ == "__main__":
    with open("input/2024/17.txt") as f:
        content = f.read()
        print("Part 1:", ",".join(str(x) for x in part_1(content)))
        print("Part 2:", part_2(content))
