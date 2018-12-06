"""
Day 6: Chronal Coordinates
"""
from operator import attrgetter


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.possesed = 0


def dist(pt1, pt2):
    return abs(pt1.x - pt2.x) + abs(pt1.y - pt2.y)


def main():
    with open('input.txt', 'r') as f:
        data = f.readlines()

    # parse data
    points = []
    for line in data:
        x, y = line.split(',')
        points.append(Point(int(x), int(y)))

    # find box all the points are in
    minXPt = min(points, key=attrgetter('x'))
    maxXPt = max(points, key=attrgetter('x'))
    minYPt = min(points, key=attrgetter('y'))
    maxYPt = max(points, key=attrgetter('y'))

    # create matrix
    infinitePts = [minXPt, maxXPt, minYPt, maxYPt]
    matrix = [0] * (maxXPt.x + 1)
    for i in range(len(matrix)):
        matrix[i] = [0] * (maxYPt.y + 1)

    # part 2 data
    regionSize = 0
    distLimit = 10000

    for xx in range(minXPt.x, len(matrix)):
        for yy in range(minYPt.y, len(matrix[0])):
            actPt = Point(xx, yy)

            # part 2
            s = sum(dist(p, actPt) for p in points)
            if s < distLimit:
                regionSize += 1

            # part 1
            closestPt = min(points, key=lambda p: dist(p, actPt))
            minDist = dist(closestPt, actPt)
            suchPts = 0
            for p in points:
                if dist(p, actPt) == minDist:
                    suchPts += 1
                if suchPts >= 2:
                    break
            else:
                matrix[xx][yy] = closestPt
                closestPt.possesed += 1

    # boundaries - if a point is on boundary, it is infinite
    for i in range(len(matrix)):
        infinitePts.append(matrix[i][minYPt.y])
        infinitePts.append(matrix[i][maxYPt.y])
    for i in range(len(matrix[0])):
        infinitePts.append(matrix[minXPt.x][i])
        infinitePts.append(matrix[maxXPt.x][i])
    infinitePts = set(infinitePts)

    best = max(points, key=lambda p: p.possesed if p not in infinitePts else -1)

    print('part 1:', best.possesed)
    print('part 2:', regionSize)


if __name__ == '__main__':
    main()
