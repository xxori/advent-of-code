from collections import deque

N = 70
def part_1(input):
    q = deque([(0,0,0)])
    seen = set([(0,0)])

    while q:
        r,c,cost = q.popleft()
        if (r,c) == (N,N):
            return cost
        seen.add((r,c))
        print(len(seen))
        next = [(r+1,c,cost+1),(r-1,c,cost+1),(r,c+1,cost+1),(r,c-1,cost+1)]
        nextpos = [x for x in next if (x[0],x[1]) not in seen and 0 <= x[0] <= N and 0 <= x[1] <= N and input[x[0]][x[1]] == 0]
        for p in nextpos:
            q.append(p)
    return -1



with open("input/2024/18.txt") as f:
    coords = [map(int,x.split(",")) for x in f.read().split("\n")[:1024]]
    map = [[0 for _ in range(N+1)] for _ in range(N+1)]
    for c,r in coords:
        map[r][c] = 1
    print("Part 1:",part_1(map))