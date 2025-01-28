
def part_1(input: str):
    layout = []
    for i,c in enumerate(input):
        if i % 2:
            layout.extend(["."]*int(c))
        else:
            layout.extend([str(i//2)]*int(c))
    l = 0
    r = len(layout)-1
    while l < r:
        while layout[l] != '.':
            l += 1
        while layout[r] == '.':
            r -= 1
        layout[l],layout[r] = layout[r], layout[l]
    layout[l],layout[r] = layout[r], layout[l]

    res = 0
    for i,n in enumerate(layout[:r+1]):
        res += i * int(n)
    return res

def part_2(input: str):
    files = []
    holes = []
    for i,c in enumerate(input):
        if i % 2:
            holes.append(int(c))
        else:
            files.append((i//2,int(c)))

    i = 0
    ending = False
    for i,f in reversed(enumerate(files)):
        ending = False
        for i,h in enumerate(holes):
            if h >= f[1]:
                nh = h - f[1]
                files

    


with open("input/2024/9.example.txt") as f:
    content = f.read()
    print(part_1(content))
    print(part_2(content))