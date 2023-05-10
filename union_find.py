class UnionFind:
    def __init__(self, number_of_elements):
        self.N = number_of_elements
        self.parent = [i for i in range(0, self.N)]
        self.rank = [0 for i in range(0, self.N)]

    def add(self):
        self.parent.append(self.N)
        self.rank.append(0)
        self.N += 1

    def find_set(self, i):
        if self.parent[i] == i:
            return i
        else:
            set = self.find_set(self.parent[i])
            self.parent[i] = set
            return set

    def is_same_set(self, i, j):
        return self.find_set(i) == self.find_set(j)

    def union_sets(self, i, j):
        if self.is_same_set(i, j):
            return
        x = self.find_set(i)
        y = self.find_set(j)
        if self.rank[x] > self.rank[y]:
            x, y = y, x
        self.parent[x] = y
        if self.rank[x] == self.rank[y]:
            self.rank[y] += 1


