"""
Day 22: Mode Maze
"""

import queue
import heapq


class Maze:
    def __init__(self, depth, targetX, targetY):
        self.depth = depth
        self.width = targetX + 1
        self.height = targetY + 1
        self.targetX = targetX
        self.targetY = targetY
        self.geol, self.eros = self.investigateArea()

    def investigateArea(self):
        self.geol = {}
        self.eros = {}

        for y in range(self.height):
            for x in range(self.width):
                self.geol[(y, x)] = self.geologicIndex(x, y)
                self.eros[(y, x)] = self.erosionLevel(x, y)
        return self.geol, self.eros

    def getRiskLevel(self):
        return sum(self.regionType(x, y) for y in range(self.targetY + 1) for x in range(self.targetX + 1))

    def geologicIndex(self, x, y):
        if (y, x) in self.geol:
            return self.geol[(y, x)]
        if (x, y) == (0, 0):
            return 0
        if y == 0:
            return x * 16807
        if x == 0:
            return y * 48271
        if x == self.targetX and y == self.targetY:
            return 0
        yxm = self.eros[(y, x-1)] if (y, x -
                                      1) in self.eros else self.erosionLevel(x-1, y)
        ymx = self.eros[(y-1, x)] if (y-1,
                                      x) in self.eros else self.erosionLevel(x, y-1)
        self.geol[(y, x)] = yxm * ymx
        return self.geol[(y, x)]

    def erosionLevel(self, x, y):
        if (y, x) in self.eros:
            return self.eros[(y, x)]
        self.eros[(y, x)] = (self.geologicIndex(x, y) + self.depth) % 20183
        return self.eros[(y, x)]

    def regionType(self, x, y):
        mod = self.erosionLevel(x, y) % 3
        return mod

    def getNeighs(self, u):
        y, x, t = u
        for tool in self.getPossibleTools(x, y):
            if tool == t:
                continue
            yield (y, x, tool)

        possibleSides = [(y, x + 1), (y + 1, x), (y - 1, x), (y, x - 1)]
        for pt in possibleSides:
            if pt[0] < 0 or pt[1] < 0:
                continue
            if t in self.getPossibleTools(pt[1], pt[0]):
                yield pt[0], pt[1], t

    def getPossibleTools(self, x, y):
        if x == self.targetX and y == self.targetY:
            return set(['t'])
        if x == 0 and y == 0:
            return set(['t'])
        if self.regionType(x, y) == 0:
            return set(['c', 't'])
        if self.regionType(x, y) == 1:
            return set(['c', 'n'])
        if self.regionType(x, y) == 2:
            return set(['t', 'n'])

    def weight(self, fromV, toV):
        if fromV[2] == toV[2]:
            return 1
        return 7

    def findRoute(self):
        dist = {}
        s = (0, 0, 't')
        dist[s] = 0
        a = [(dist[s], s)]
        dest = (self.targetY, self.targetX, 't')

        while a:
            u = heapq.heappop(a)[1]
            if dist[u] > dist.get(dest, float('inf')):
                continue
            for v in self.getNeighs(u):
                w = self.weight(u, v)
                if dist.get(v, float('inf')) > dist[u] + w:
                    dist[v] = dist[u] + w
                    heapq.heappush(a, (dist[v], v))
        return dist[dest]


def main():
    # official data
    depth = 4080
    targetX, targetY = 14, 785
    maze = Maze(depth, targetX, targetY)

    # test data
    # depth = 510
    # targetX, targetY = 10, 10

    print('part 1:', maze.getRiskLevel())
    print('part 2:', maze.findRoute())


if __name__ == '__main__':
    main()
