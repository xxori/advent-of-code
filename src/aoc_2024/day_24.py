import graphviz

def operation(st):
    if st == "AND":
        return lambda x,y: x & y
    if st == "OR":
        return lambda x,y: x | y
    if st == "XOR":
        return lambda x,y: x^y
    raise ValueError("Unexpected Operation")

def part_1(input):
    init, sops = input.split("\n\n")
    mapping = {}
    for i in init.split("\n"):
        name,num = i.split(": ")
        mapping[name] = int(num)
    
    ops = []
    for sop in sops.split("\n"):
        op = sop.split(" ")
        op.pop(-2)
        ops.append(op)

    while ops:
        newops = []
        for op in ops:
            if op[0] not in mapping or op[2] not in mapping:
                newops.append(op)
                continue
                
            func = operation(op[1])
            mapping[op[-1]] = func(mapping[op[0]],mapping[op[2]])
        ops = newops
    
    res = 0
    cc = 0
    while "z{0:02d}".format(cc) in mapping:
        res += mapping["z{0:02d}".format(cc)] << cc
        cc += 1
    
    return res

def part_2(input):
    init, sops = input.split("\n\n")
    mapping = {}
    for i in init.split("\n"):
        name,num = i.split(": ")
        mapping[name] = int(num)
    
    ops = []
    for sop in sops.split("\n"):
        op = sop.split(" ")
        op.pop(-2)
        if op[-1] == "z15":
            op[-1] = "tvp"
        elif op[-1] == "tvp":
            op[-1] = "z15"

        elif op[-1] == "kmb":
            op[-1] = "z10"
        elif op[-1] == "z10":
            op[-1] = "kmb"
        
        elif op[-1] == "dpg":
            op[-1] = "z25"
        elif op[-1] == "z25":
            op[-1] = "dpg"
        
        elif op[-1] == "mmf":
            op[-1] = "vdk"
        elif op[-1] == "vdk":
            op[-1] = "mmf"
        ops.append(op)

    dot = graphviz.Digraph()
    nc = 0
    for op in ops:
        dot.node(op[0])
        dot.node(op[2])
        dot.node(op[3])
        dot.node(str(nc), op[1])
        dot.edge(op[0],str(nc))
        dot.edge(op[2],str(nc))
        dot.edge(str(nc),op[3])
        nc += 1
    dot.render('out.gv', view=True)

if __name__ == "__main__":
    with open("input/2024/24.txt") as f:
        content = f.read()
        print("Part 1:",part_1(content))
        print("Part 2:",part_2(content))

# TVP and Z16 swap