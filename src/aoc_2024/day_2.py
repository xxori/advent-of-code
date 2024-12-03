def get_diffs(input): return [input[i-1]-input[i] for i in range(1,len(input))]
def increasing_valid(input): return all([d in [1,2,3] for d in get_diffs(input)])
def is_valid(input): return increasing_valid(input) or increasing_valid(input[::-1])

def part_1(input): return sum([is_valid([int(y) for y in x.split()]) for x in input])

# def pos(input): return [input[:i]+input[i+1:] for i in range(len(input))]
# def is_valid_2(input):  return any([is_valid(x) for x in pos(input)])

diffs = [1,2,3]
def increasing_valid_2(report):
    i = 1
    removed = False
    while i < len(report):
        a,b = report[i-1],report[i]
        if b-a in diffs:
            i += 1
            continue
        if i == 1 and report[i+1]-b in diffs:
            toRemove = i - 1
        elif i == len(report)-1 and a-report[i-2] in diffs:
            toRemove = i
        elif b-report[i-2] in diffs:
            toRemove = i - 1
        elif report[i+1]-a in diffs:
            toRemove = i
        else:
            return False
        if removed:
            return False
        removed = True
        report.pop(toRemove)
    return True


def is_valid_2(input): return increasing_valid_2(input.copy()) or increasing_valid_2(input[::-1])

def part_2(input):
    r = 0
    for line in input:
        r += is_valid_2([int(x) for x in line.split(" ")])
    return r

with open("input/2024/2.txt") as f:
    t = f.readlines()
    print(part_1(t))
    print(part_2(t))
# print(increasing_valid_2([5,1,2, 3, 4]))