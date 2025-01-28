
def inst_to_dir(inst: str) -> tuple[int,int]:
    match inst:
        case "<":
            return (0,-1)
        case "^":
            return (-1,0)
        case ">":
            return (0,1)
        case "v":
            return (1,0)
        case _:
            raise ValueError("Unexpected instruction")

def part_1(grid: list[list[str]], instructions: list[str]) -> int:
    rn = len(grid)
    cn = len(grid[0])
    for r in range(rn):
        for c in range(cn):
            if grid[r][c] == "@":
                rpr,rpc = r,c

    for inst in instructions:
        dir = inst_to_dir(inst)
        # [print("".join(x)) for x in grid]
        npr,npc = rpr+dir[0],rpc+dir[1]
        if grid[npr][npc] == "#":
            continue

        if grid[npr][npc] == ".":
            grid[npr][npc] = "@"
            grid[rpr][rpc] = "."
            rpr,rpc = npr,npc
            continue

        cpr,cpc = npr,npc
        while grid[cpr][cpc] != "." and grid[cpr][cpc] != "#":
            cpr,cpc = cpr+dir[0],cpc+dir[1]
        if grid[cpr][cpc] == "#":
            continue
        grid[cpr][cpc] = "O"
        grid[npr][npc] = "@"
        grid[rpr][rpc] = "."
        rpr,rpc = npr,npc
    
    res = 0
    for r in range(rn):
        for c in range(cn):
            if grid[r][c] == "O":
                res += 100 * r + c
    return res


def canpush(grid: list[list[str]], coords: tuple[int,int], dir: tuple[int,int]) -> bool:
    r,c = coords

    if grid[r+dir[0]][c] == "#" or grid[r+dir[0]][c+1] == "#":
        return False
    
    if grid[r+dir[0]][c] == "[" and not canpush(grid,(r+dir[0],c),dir):
        return False
    if grid[r+dir[0]][c-1] == "[" and not canpush(grid,(r+dir[0],c-1),dir):
        return False
    if grid[r+dir[0]][c+1] == "[" and not canpush(grid,(r+dir[0],c+1),dir):
        return False
    return True

def pushblock(grid: list[list[str]], coords: tuple[int,int], dir: tuple[int,int]) -> bool:
    r,c = coords
    if dir == (0,1):
        if grid[r][c+2] == "#":
            return False
        if grid[r][c+2] == "[" and not pushblock(grid,(r,c+2),dir):
            return False
        grid[r][c+2] = "]"
        grid[r][c+1] = "["
        grid[r][c] = "."
        return True
    if dir == (0,-1):
        if grid[r][c-1] == "#":
            return False
        if grid[r][c-1] == "]" and not pushblock(grid,(r,c-2),dir):
            return False
        grid[r][c-1] = "["
        grid[r][c] = "]"
        grid[r][c+1] = "."
        return True
    
    if grid[r+dir[0]][c] == "#" or grid[r+dir[0]][c+1] == "#":
        return False
    
    if grid[r+dir[0]][c-1] == "[" and grid[r+dir[0]][c+1] == "[" and (not canpush(grid,(r+dir[0],c-1),dir) or not canpush(grid,(r+dir[0],c+1),dir)):
        return False

    if grid[r+dir[0]][c] == "[" and not pushblock(grid,(r+dir[0],c),dir):
        return False
    if grid[r+dir[0]][c-1] == "[" and not pushblock(grid,(r+dir[0],c-1),dir):
        return False
    if grid[r+dir[0]][c+1] == "[" and not pushblock(grid,(r+dir[0],c+1),dir):
        return False

    grid[r+dir[0]][c] = "["
    grid[r+dir[0]][c+1] = "]"
    grid[r][c] = "."
    grid[r][c+1] = "."
    return True
    

        

def part_2(grid: list[list[str]], instructions: list[str]) -> int:
    rn = len(grid)
    cn = len(grid[0])
    for r in range(rn):
        for c in range(cn):
            if grid[r][c] == "@":
                rpr,rpc = r,c

    for inst in instructions:
        # [print("".join(x)) for x in grid]
        dir = inst_to_dir(inst)
        npr,npc = rpr+dir[0],rpc+dir[1]
        if grid[npr][npc] == "#":
            continue

        if grid[npr][npc] == ".":
            grid[npr][npc] = "@"
            grid[rpr][rpc] = "."
            rpr,rpc = npr,npc
            continue

        if grid[npr][npc] == "[":
            a = pushblock(grid,(npr,npc),dir)
        elif grid[npr][npc-1] == "[":
            a = pushblock(grid,(npr,npc-1),dir)
        if a:
            grid[npr][npc] = "@"
            grid[rpr][rpc] = "."
            rpr,rpc = npr,npc
    
    # [print("".join(x)) for x in grid]
    
    res = 0
    for r in range(rn):
        for c in range(cn):
            if grid[r][c] == "[":
                res += 100 * r + c
    return res

with open("input/2024/15.txt") as f:
    content = f.read()
    grid, instructions = content.split("\n\n")
    instructions = list(instructions.replace("\n",""))
    grid1 = [list(x) for x in grid.split("\n")]
    print("Part 1:",part_1(grid1,instructions))

    grid2 = [list(x.replace("#","##").replace("O","[]").replace(".","..").replace("@","@.")) for x in grid.split("\n")]
    print("Part 2:", part_2(grid2,instructions))