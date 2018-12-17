"""
Day 17: Reservoir Research
"""

import re


class Grid:
    def __init__(self, points, waterSource):
        self.waterSource = waterSource
        self.shiftx = None
        self.shifty = None
        self.matrix = self.generateGrid(points)
        self.width = len(self.matrix)
        self.height = len(self.matrix[0])

    def countWater(self):
        ans = 0
        for col in self.matrix:
            for cell in col:
                if cell in ['~', '|']:
                    ans += 1
        # in answer do not include lines above first line with #
        # First line is empty (with only source), the rest has exactly one '|'
        return ans - self.shifty + 1

    def countWaterStatic(self):
        ans = 0
        for col in self.matrix:
            for cell in col:
                if cell in ['~']:
                    ans += 1
        return ans

    def generateGrid(self, points):
        minx = min(points, key=lambda p: p[0][0])[0][0]
        maxx = max(points, key=lambda p: p[0][1])[0][1]
        miny = min(points, key=lambda p: p[1][0])[1][0]
        maxy = max(points, key=lambda p: p[1][1])[1][1]
        self.shiftx = minx - 1
        self.shifty = miny
        matrix = [0] * (maxx - minx + 3)
        for i in range(len(matrix)):
            matrix[i] = ['.'] * (maxy + 1)

        for point in points:
            for x in range(point[0][0], point[0][1] + 1):
                for y in range(point[1][0], point[1][1] + 1):
                    matrix[x-self.shiftx][y] = '#'
        return matrix

    def fillWater(self):
        self.fillWaterDown(
            self.waterSource[0] - self.shiftx, self.waterSource[1])

    def fillWaterDown(self, wx, wy):
        sources = [(wx, wy)]
        while sources:
            wx, wy = sources.pop()
            wy += 1
            if self.matrix[wx][wy] != '.':
                continue
            while wy < self.height and self.matrix[wx][wy] == '.':
                self.matrix[wx][wy] = '|'
                wy += 1

            if wy == self.height:
                continue
            if self.matrix[wx][wy] == '|':
                continue

            while True:
                wy -= 1
                cont = self.fillWaterSide(wx, wy)
                if cont:
                    sources.extend(cont)
                    break
                if wy == 0:
                    break

    def fillWaterSide(self, wx, wy):
        self.matrix[wx][wy] = '~'
        continuations = []

        tempx, tempy = wx + 1, wy
        isTop = False
        while tempx < self.width and self.matrix[tempx][tempy] in ['.', '|']:
            self.matrix[tempx][tempy] = '~'
            if tempy + 1 < self.height and self.matrix[tempx][tempy + 1] in ['.', '|']:
                continuations.append((tempx, tempy))
                isTop = True
                break
            tempx += 1
        tempx, tempy = wx - 1, wy
        while tempx >= 0 and self.matrix[tempx][tempy] in ['.', '|']:
            self.matrix[tempx][tempy] = '~'
            if tempy + 1 < self.height and self.matrix[tempx][tempy + 1] in ['.', '|']:
                continuations.append((tempx, tempy))
                isTop = True
                break
            tempx -= 1

        # if level is the top one, it must be changed
        if isTop:
            x = wx
            while x < self.width and self.matrix[x][tempy] == '~':
                self.matrix[x][tempy] = '|'
                x += 1
            x = wx - 1
            while x >= 0 and self.matrix[x][tempy] == '~':
                self.matrix[x][tempy] = '|'
                x -= 1
        return continuations

    def print(self):
        for y in range(len(self.matrix[0])):
            for x in range(len(self.matrix)):
                print(self.matrix[x][y], end='')
            print()
        print()


def main():
    with open('input.txt', 'r') as f:
        data = f.read().split('\n')

    points = []
    waterSource = (500, 0)
    for line in data:
        xfirstlines = re.findall('^x=.*', line)
        yfirstlines = re.findall('^y=.*', line)

        if xfirstlines:
            x, yfrom, yto = map(int, re.findall(r'[\d]+', xfirstlines[0]))
            points.append(((x, x), (yfrom, yto)))
        elif yfirstlines:
            y, xfrom, xto = map(int, re.findall(r'[\d]+', yfirstlines[0]))
            points.append(((xfrom, xto), (y, y)))

    grid = Grid(points, waterSource)
    grid.fillWater()
    # grid.print()
    print('part 1:', grid.countWater())
    print('part 2:', grid.countWaterStatic())


if __name__ == '__main__':
    main()
