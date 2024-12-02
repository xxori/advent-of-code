from collections import Counter

def run(x: str):
    lines = x.split("\n")
    f,s=[],[]
    for i in lines:
        a,b = i.split("   ")
        f.append(int(a))
        s.append(int(b))
    f.sort()
    s.sort()
    print(sum(map(lambda x: abs(x[0]-x[1]),zip(f,s))))

    c = Counter(s)
    print(sum(map(lambda x: x*c[x],f)))

if __name__ == "__main__":
    with open("input/2024/1.txt") as f:
        s = f.read()
        run(s)
