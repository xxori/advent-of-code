from collections import defaultdict


def is_valid(order: list[int], mapping: dict[int, set[int]]) -> bool:
    if order == []:
        return True
    candidates = mapping[order[0]].copy()
    for i in order[1:]:
        if i not in candidates:
            return False
        candidates.intersection_update(mapping[i])
    return True


def parse(input: str) -> tuple[dict[int, set[int]], list[list[int]]]:
    [order_section, instruction_section] = input.split("\n\n")
    orders = [x.split("|") for x in order_section.split("\n")]
    mapping = defaultdict(set)
    for [x, y] in orders:
        x, y = int(x), int(y)
        mapping[x].add(y)
    printings = [
        [int(y) for y in x.split(",")] for x in instruction_section.split("\n")
    ]
    return (mapping, printings)


def part_1(input):
    mapping, printings = parse(input)
    valid_printings = [x for x in printings if is_valid(x, mapping)]
    middles = [x[len(x) // 2] for x in valid_printings]
    return sum(middles)


# Sort the orders topologically but only with a subset of mappings
def find_correct_order(
    todo: set[int],
    mapping: dict[int, set[int]],
    done: set[int],
    in_order: list[int],
) -> list[int]:
    for page in todo:
        if page not in done:
            done.add(page)
            find_correct_order(
                todo.intersection(mapping[page]), mapping, done, in_order
            )
            in_order.append(page)
    return in_order


def part_2(input):
    mapping, printings = parse(input)
    invalid_printings = [x for x in printings if not is_valid(x, mapping)]
    rearranged = [
        find_correct_order(set(x), mapping, set(), []) for x in invalid_printings
    ]
    middles = [x[len(x) // 2] for x in rearranged]
    return sum(middles)


with open("input/2024/5.txt") as f:
    content = f.read()
    print(part_1(content))
    print(part_2(content))
