from collections import deque


def cheats(grid: list[list[int]], s: tuple[int, int], e: tuple[int, int], cheats: int):
    # Use BFS to find shortest path to end
    q: deque[tuple[tuple[int, int], int]] = deque()
    q.appendleft((s, 0))
    parents = {}
    seen = set()
    while q:
        point, cost = q.pop()
        seen.add(point)
        if point == e:
            break
        for nr, nc in (
            (point[0] + 1, point[1]),
            (point[0] - 1, point[1]),
            (point[0], point[1] + 1),
            (point[0], point[1] - 1),
        ):
            if grid[nr][nc] == 0 and (nr, nc) not in seen:
                parents[(nr, nc)] = point
                q.appendleft(((nr, nc), cost + 1))

    # For each element in path, find other elements in path with manhattan distance <= cheats
    path = []
    cur = e
    while cur != s:
        path.append(cur)
        cur = parents[cur]
    path.append(s)
    path = list(enumerate(path))
    count = 0
    for i, p in path:
        for i2 in range(i + 3, len(path)):
            i2, p2 = path[i2]
            dist = abs(p2[0] - p[0]) + abs(p2[1] - p[1])
            if dist <= cheats and i2 - i > dist and i2 - i - dist >= 100:
                count += 1
    return count


if __name__ == "__main__":
    with open("input/2024/20.txt") as f:
        content = f.read()
        sg = [list(st) for st in content.split("\n")]
        grid = [[0 for _ in range(len(sg[0]))] for _ in range(len(sg))]
        for r in range(len(sg)):
            for c in range(len(sg[0])):
                if sg[r][c] == "S":
                    s = (r, c)
                if sg[r][c] == "E":
                    e = (r, c)
                if sg[r][c] == "#":
                    grid[r][c] = 1
        print("Part 1:", cheats(grid, s, e, 2))
        print("Part 2:", cheats(grid, s, e, 20))
