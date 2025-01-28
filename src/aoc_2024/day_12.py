point = tuple[int, int]


def offsets(p: point) -> list[point]:
    r, c = p
    return [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]


def diags(p: point) -> list[point]:
    r, c = p
    return [(r + 1, c + 1), (r + 1, c - 1), (r - 1, c + 1), (r - 1, c - 1)]


# Returns list of external edge points around boundary and area of the partition with flood fill
def proc(
    grid: list[list[str]],
    visited: list[list[bool]],
    acc: tuple[list[tuple[point, point]], int],
    loc: point,
    prev: point,
    finding: str,
) -> tuple[list[tuple[point, point]], int]:
    r, c = loc
    # If the location is out of the grid or a different char, it marks the edge of the partition
    if not 0 <= r < len(grid) or not 0 <= c < len(grid[0]) or grid[r][c] != finding:
        return ([(prev, loc), *acc[0]], acc[1])
    # If we have already visited the location, we can just short circuit and exit
    if visited[r][c]:
        return acc

    # Mark visited and increment area, and process for each adjacent tile
    visited[r][c] = True
    acc = (acc[0], acc[1] + 1)
    for offset in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
        acc = proc(grid, visited, acc, offset, loc, finding)
    return acc


# Turn a set of all external boundary nodes into the nubmer of sides of the shape
# We use two points as each edge has an in-side and out-side so we store an inside and outside node across the edge
def sides(points: set[tuple[point, point]], cur: tuple[point, point], acc: int) -> int:
    if not points:
        return acc

    # We can traverse the straight edge if both inner and
    # outer side are shifted in any cardinal direction
    for ioff, outoff in zip(offsets(cur[0]), offsets(cur[1])):
        if (ioff, outoff) in points:
            points.remove((ioff, outoff))
            return sides(points, (ioff, outoff), acc)

    # Process traversing external corners, i.e. the internal point
    # remains the same and the external point shifts diagonally
    for offset in diags(cur[1]):
        if (cur[0], offset) in points:
            points.remove((cur[0], offset))
            return sides(points, (cur[0], offset), acc + 1)

    # Process traversing internal corners, i.e. the internal point
    # shifts diagonally and the external point remains the same
    for offset in diags(cur[0]):
        if (offset, cur[1]) in points:
            points.remove((offset, cur[1]))
            return sides(points, (offset, cur[1]), acc + 1)

    # If none of the other conditions are met, there may be some unconnected edges
    # I.e multiple internal holes in the shape. Jump to a random other remaining point
    f = points.pop()
    return sides(points, f, acc + 1)


with open("input/2024/12.txt") as f:
    input = [list(x) for x in f.read().split("\n")]
    visited = [[False for _ in range(len(input[0]))] for _ in range(len(input))]
    p1 = 0
    p2 = 0
    for r in range(len(input)):
        for c in range(len(input[0])):
            if not visited[r][c]:
                edges, area = proc(input, visited, ([], 0), (r, c), (-1,-1), input[r][c])
                p1 += len(edges) * area
                edges = set(edges)
                # Select min point so we dont double count any edges
                f = min(edges)
                edges.remove(f)
                si = sides(edges, f, 1)
                p2 += si * area
    print("Part 1:", p1)
    print("Part 2:", p2)
