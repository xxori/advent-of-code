class CliqueFinder:
    def isClique(self, b):
        for i in range(1, b):
            for j in range(i + 1, b):
                if self.graph[self.store[i]][self.store[j]] == 0:
                    return False
        return True

    def findCliques1(self, i, s):
        for j in range(i, self.V - (self.n - s)):
            if self.degree[j] >= self.n - 1:
                self.store[s] = j
                if self.isClique(s + 1):
                    if s < self.n:
                        self.findCliques1(j, s + 1)
                    elif any(
                        self.map[self.store[k]].startswith("t") for k in range(1, s + 1)
                    ):
                        self.res += 1

    def findCliques2(self, i, s):
        if self.res2 is not None:
            return
        for j in range(i, self.V - (self.n - s)):
            if self.degree[j] >= self.n - 1:
                self.store[s] = j
                if self.isClique(s + 1):
                    if s < self.n:
                        self.findCliques2(j, s + 1)
                    else:
                        self.res2 = ",".join(sorted(self.map[self.store[k]] for k in range(1,s+1)))

    def part_1(self):
        self.n = 3
        self.store = [0] * self.V
        self.res = 0
        self.findCliques1(0, 1)
        return self.res

    def part_2(self):
        for n in range(3,self.V+1):
            self.n = n
            self.store = [0] * self.V
            self.res2 = None
            self.findCliques2(0,1)
            if self.res2 is None:
                self.n = n - 1
                self.findCliques2(0,1)
                return self.res2

    def __init__(self, input):
        count = 0
        m = {}
        for line in input.split("\n"):
            first, second = line.split("-")
            if first not in m.keys():
                m[first] = count
                count += 1
            if second not in m.keys():
                m[second] = count
                count += 1
        self.map = {v: k for k, v in m.items()}
        self.V = len(m.keys())
        self.graph = [[0 for _ in range(self.V)] for _ in range(self.V)]
        self.degree = [0 for _ in range(self.V)]
        for line in input.split("\n"):
            first, second = line.split("-")
            first = m[first]
            second = m[second]
            self.graph[first][second] = 1
            self.graph[second][first] = 1
            self.degree[first] += 1
            self.degree[second] += 1


if __name__ == "__main__":
    with open("input/2024/23.txt") as f:
        cf = CliqueFinder(f.read())
        print("Part 1:", cf.part_1())
        print("Part 2:", cf.part_2())
