from functools import lru_cache

@lru_cache(None)
def proc1(matching: str, avail: tuple[str]) -> bool:
    if matching == "":
        return True

    res = []
    for pattern in avail:
        if pattern == matching:
            return True
        if matching.startswith(pattern):
            res.append(proc1(matching[len(pattern):],avail))
    return any(res)

@lru_cache(None)
def proc2(matching: str, avail: tuple[str]) -> int:
    if matching == "":
        return 1

    res = 0
    for pattern in avail:
        if matching.startswith(pattern):
            res += proc2(matching[len(pattern):],avail)
    return res

def part_1(avail, opts):
    s = 0
    for opt in opts:
        s += int(proc1(opt,avail))
    return s

def part_2(avail, opts):
    s = 0
    for opt in opts:
        s += int(proc2(opt,avail))
    return s
    


if __name__ == "__main__":
    with open("input/2024/19.txt") as f:
        lines = f.read().split("\n\n")
        avail = tuple(lines[0].split(", "))
        opts = lines[1].split("\n")
        print("Part 1:",part_1(avail,opts))
        print("Part 2:",part_2(avail,opts))
