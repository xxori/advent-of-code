from itertools import permutations

ngrid = [["7","8","9"],["4","5","6"],["1","2","3"],["_","0","A"]]
npos = {}
for r in range(len(ngrid)):
    for c in range(len(ngrid[0])):
        npos[ngrid[r][c]] = (r,c)

dgrid = [["_","^","A"],["<","v",">"]]
dpos = {}
for r in range(len(dgrid)):
    for c in range(len(dgrid[0])):
        dpos[dgrid[r][c]] = (r,c)

def numpad(goto):
    cur = "A"
    targ = 0
    res = ""
    while targ < len(goto):
        rdist,cdist = npos[goto[targ]][0]-npos[cur][0],npos[goto[targ]][1] - npos[cur][1]
        vchar = "v" if rdist > 0 else "^"
        hchar = ">" if cdist > 0 else "<"
        cand = vchar * abs(rdist) + hchar * abs(cdist)
        allcands = ["".join(x) for x in permutations(cand)]
        res += max(allcands,key=lambda cand: kscore(res,cand,cur))
        res += "A"
        cur = goto[targ]
        targ += 1
    return res

def kscore(cur,cand,sq):
    if len(cand) == 0:
        return 0
    if sq == "<" and cand[0] == "^":
        return -1
    if sq == "^" and cand[0] == "<":
        return -1
    if sq == "A" and len(cand) >= 2 and cand[:2] == "<<":
        return -1
    score = 0
    if len(cur) >= 1:
        score -= abs(dpos[cand[0]][0]-dpos[cur[-1]][0]) + abs(dpos[cand[0]][1]-dpos[cur[-1]][1])
    if len(cur) >= 1 and cur[-1] == cand[0]:
        score += 1
    for i in range(1,len(cand)):
        if cand[i] == cand[i-1]:
            score += 1
    return score

def keypad(goto):
    cur = "A"
    targ = 0
    res = ""
    while targ < len(goto):
        rdist,cdist = dpos[goto[targ]][0] - dpos[cur][0],dpos[goto[targ]][1] - dpos[cur][1]
        vchar = "v" if rdist > 0 else "^"
        hchar = ">" if cdist > 0 else "<"
        cand = vchar * abs(rdist) + hchar * abs(cdist)
        allcands = ["".join(x) for x in permutations(cand)]
        res += max(allcands,key=lambda cand: kscore(res,cand,cur))
        res += "A"
        cur = goto[targ]
        targ += 1
    return res


def part_1(input):
    tot = 0
    for line in input.split("\n"):
        kp1 = numpad(line)
        kp2 = keypad(kp1)
        kp3 = keypad(kp2)

        tot += len(kp3) * int(line[:-1])
        print(line)
        print(kp3)
        print(kp2)
        print(kp1)
        print()
    return tot

if __name__ == "__main__":
    with open("input/2024/21.txt") as f:
        content = f.read()
        print("Part 1:",part_1(content))