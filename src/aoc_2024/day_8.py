from collections import defaultdict


def part_1(coords, rn, cn):
    antinodes = set()
    for nodes in coords:
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                n1, n2 = nodes[i], nodes[j]
                xd, yd = n1[0] - n2[0], n1[1] - n2[1]

                antinodes.add((n1[0] + xd, n1[1] + yd))
                antinodes.add((n2[0] - xd, n2[1] - yd))

    return len([x for x in antinodes if 0 <= x[0] < rn and 0 <= x[1] < cn])


def part_2(coords, rn, cn):
    antinodes = set()
    for nodes in coords:
        if len(nodes) > 1:
            antinodes.update(set(nodes))
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                n1, n2 = nodes[i], nodes[j]
                xd, yd = n1[0] - n2[0], n1[1] - n2[1]

                x, y = xd, yd
                while 0 <= n1[0] + x < rn and 0 <= n1[1] + y < cn:
                    antinodes.add((n1[0] + x, n1[1] + y))
                    x += xd
                    y += yd

                x, y = xd, yd
                while 0 <= n2[0] - x < rn and 0 <= n2[1] - y < cn:
                    antinodes.add((n2[0] - x, n2[1] - y))
                    x += xd
                    y += yd

    return len(antinodes)


with open("input/2024/8.txt") as f:
    input = f.read().split("\n")
    coords = defaultdict(list)
    rn = len(input)
    cn = len(input[0])
    for r in range(rn):
        for c in range(cn):
            if input[r][c] != ".":
                coords[input[r][c]].append((r, c))
    coords = coords.values()
    print("Part 1:", part_1(coords, rn, cn))
    print("Part 1:", part_2(coords, rn, cn))
