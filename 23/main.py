"""
Day 23: Experimental Emergency Teleportation
"""

import re
from z3 import *


def myAbs(v):
    return If(v >= 0, v, -v)


class Nanobot:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def distToNanobot(self, two):
        return abs(self.x - two.x) + abs(self.y - two.y) + abs(self.z - two.z)

    def distToNanobotZ3(self, two):
        return myAbs(self.x - two.x) + myAbs(self.y - two.y) + myAbs(self.z - two.z)

    def distToPt(self, p):
        return myAbs(self.x - p[0]) + myAbs(self.y - p[1]) + myAbs(self.z - p[2])


def main():
    with open('input.txt', 'r') as f:
        data = f.read().split('\n')

    # parsing data
    nanobots = []
    for line in data:
        x, y, z, r = map(int, re.findall(r'[-\d]+', line))
        nanobots.append(Nanobot(x, y, z, r))

    # part 1
    maxN = max(nanobots, key=lambda x: x.r)
    ans = sum(1 for x in nanobots if x.distToNanobot(maxN) <= maxN.r)
    print('part 1:', ans)

    # part 2 (z3)
    minX = min(n.x for n in nanobots)
    maxX = max(n.x for n in nanobots)
    minY = min(n.y for n in nanobots)
    maxY = max(n.y for n in nanobots)
    minZ = min(n.z for n in nanobots)
    maxZ = max(n.z for n in nanobots)
    x = Int('x')
    y = Int('y')
    z = Int('z')
    s = Optimize()
    s.add(x >= minX, x <= maxX, y >= minY, y <= maxY, z >= minZ, z <= maxZ)
    dist = 0
    for n in nanobots:
        dist += If(n.distToPt((x, y, z)) <= n.r, 1, 0)
    s.maximize(dist)
    s.check()
    ans = abs(s.model()[x].as_long()) + abs(s.model()[y].as_long()) + abs(s.model()[z].as_long())
    print('part 2:', ans)


if __name__ == '__main__':
    main()
