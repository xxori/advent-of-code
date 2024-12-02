def diffs(input): return [input[i-1]-input[i] for i in range(1,len(input))]
def increasing_valid(input): return all([d in [1,2,3] for d in diffs(input)])
def is_valid(input): return increasing_valid(input) or increasing_valid(input[::-1])

def part_1(input): return sum([is_valid([int(y) for y in x.split()]) for x in input])

def pos(input): return [input[:i]+input[i+1:] for i in range(len(input))]
def is_valid_2(input):  return any([is_valid(x) for x in pos(input)])

def part_2(input):
    return sum([is_valid_2([int(y) for y in x.split()]) for x in input])

with open("input/2024/2.txt") as f:
    t = f.readlines()
    print(part_1(t))
    print(part_2(t))
