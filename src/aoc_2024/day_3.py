import re

pattern1 = re.compile(r"mul\(\d{1,3},\d{1,3}\)")
pattern2 = re.compile(r"don't\(\)|do\(\)|mul\(\d{1,3},\d{1,3}\)")

def part_1(input):
    matches = re.findall(pattern1,input)
    res = 0
    for m in matches:
        trimmed = m[4:-1]
        a,b = trimmed.split(",")
        res += int(a) * int(b)
    return res

def part_2(input):
    matches = re.findall(pattern2,input)
    res = 0
    enabled = True
    for m in matches:
        if m == "don't()":
            enabled = False
        elif m == "do()":
            enabled = True
        elif enabled:
            trimmed = m[4:-1]
            a,b = trimmed.split(",")
            res += int(a) * int(b)
    return res


with open("input/2024/3.example.txt") as f:
    content = f.read()
    print(part_1(content))
    print(part_2(content))
