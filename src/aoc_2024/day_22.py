
def num_2000(secret: int) -> int:
    for _ in range(2000):
        secret ^= secret * 64
        secret %= 16777216
        secret ^= secret // 32
        secret %= 16777216
        secret ^= secret * 2048
        secret %= 16777216
    return secret

if __name__ == "__main__":
    with open("input/2024/22.txt") as f:
        print("Part 1:",sum([num_2000(int(x)) for x in f.read().split("\n")]))
