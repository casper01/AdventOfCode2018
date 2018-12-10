"""
Day 10: The Stars Align
"""

import time
import os
import re


class Point:
    def __init__(self, pos, v):
        self.pos = (pos[1], pos[0])
        self.v = (v[1], v[0])

    def move(self):
        x = self.pos[0] + self.v[0]
        y = self.pos[1] + self.v[1]
        self.pos = (x, y)


def printPoints(points, minX, maxX, minY, maxY):
    os.system('clear')
    matrix = [' '] * (maxX - minX + 1)
    for i in range(len(matrix)):
        matrix[i] = [' '] * (maxY - minY + 1)

    for pt in points:
        matrix[pt.pos[0] - minX][pt.pos[1] - minY] = '#'

    for row in matrix:
        print(''.join(row))


def main():
    with open('input.txt', 'r') as f:
        data = f.readlines()

    points = []
    for line in data:
        xp, yp, xv, yv = map(int, re.findall(r'[-\d]+', line))
        pos = xp, yp
        v = xv, yv
        points.append(Point(pos, v))

    sec = 0
    while sec != 10888:
        sec += 1

        for pt in points:
            pt.move()

        minX = min(points, key=lambda x: x.pos[0]).pos[0]
        maxX = max(points, key=lambda x: x.pos[0]).pos[0]
        minY = min(points, key=lambda x: x.pos[1]).pos[1]
        maxY = max(points, key=lambda x: x.pos[1]).pos[1]

        if maxX - minX > 100 or maxY - minY > 100:
            continue

        printPoints(points, minX, maxX, minY, maxY)
        print('SECS:', sec)
        time.sleep(1)


if __name__ == '__main__':
    main()
