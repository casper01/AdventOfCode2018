"""
Day 25: Four-Dimensional Adventure
"""


def dist(pt1, pt2):
    d = 0
    for i in range(4):
        d += abs(pt1[i] - pt2[i])
    return d


class UnionFind:
    def __init__(self, points):
        self.sets = {}
        for i, pt in enumerate(points):
            self.sets[pt] = i

    def getPoints(self):
        return self.sets

    def findSet(self, pt):
        return self.sets[pt]

    def union(self, pt1, pt2):
        if self.sets[pt1] == self.sets[pt2]:
            return
        newSet = min(self.sets[pt1], self.sets[pt2])
        for c in self.sets:
            if self.sets[c] in (self.sets[pt1], self.sets[pt2]):
                self.sets[c] = newSet

    def getSetsCount(self):
        return len(set(self.sets.values()))


def main():
    with open('input.txt', 'r') as f:
        data = f.read().split('\n')

    pts = []
    for line in data:
        pts.append(tuple(map(int, line.split(','))))

    constellations = UnionFind(pts)
    change = True
    while change:
        change = False
        for pt1 in constellations.getPoints():
            for pt2 in constellations.getPoints():
                if dist(pt1, pt2) > 3 or constellations.findSet(pt1) == constellations.findSet(pt2):
                    continue
                change = True
                constellations.union(pt1, pt2)
    print('part 1:', constellations.getSetsCount())


if __name__ == '__main__':
    main()
