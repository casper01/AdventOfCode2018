"""
Day 3: No Matter How You Slice It
"""


class Rect:
    def __init__(self, id, x, y, w, h):
        self.id = id
        self.x = x
        self.y = y
        self.w = w
        self.h = h


def torect(data):
    ans = []
    for line in data:
        s = line.split()
        xy = s[2][:-1].split(',')
        wh = s[3].split('x')
        r = Rect(s[0], int(xy[0]), int(xy[1]), int(wh[0]), int(wh[1]))
        ans.append(r)
    return ans


def main():
    with open('input.txt', 'r') as f:
        data = f.readlines()

    rects = torect(data)

    fabricW = 0
    fabricH = 0
    for r in rects:
        fabricW = max(fabricW, r.x + r.w)
        fabricH = max(fabricH, r.y + r.h)

    matrix = [0] * fabricW
    for i in range(len(matrix)):
        matrix[i] = [0] * fabricH

    # part 1
    twoOrMore = 0
    for rect in rects:
        for i in range(rect.x, rect.x + rect.w):
            for j in range(rect.y, rect.y + rect.h):
                matrix[i][j] += 1
                if matrix[i][j] == 2:
                    twoOrMore += 1
    print('part 1:', twoOrMore)

    # part 2
    winnerRect = None
    for rect in rects:
        invalid = False
        for i in range(rect.x, rect.x + rect.w):
            for j in range(rect.y, rect.y + rect.h):
                if matrix[i][j] != 1:
                    invalid = True
                    break
        if not invalid:
            winnerRect = rect
            break
    print('part 2:', winnerRect.id)


if __name__ == '__main__':
    main()
