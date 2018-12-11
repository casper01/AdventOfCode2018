"""
Day 11: Chronal Charge
"""


def powerLevel(x, y, gridSerialNum):
    rackId = x + 10
    powerLvl = rackId * y
    ans = powerLvl + gridSerialNum
    ans *= rackId
    ans = int(ans / 100) % 10
    ans -= 5
    return ans


def sumSquare(matrix, x, y, size):
    s = 0
    for i in range(size):
        for j in range(size):
            s += matrix[x + i][y + j]
    return s


def getMax(matrix, sqsize):
    for i in range(len(matrix) - sqsize):
        for j in range(len(matrix[i]) - sqsize):
            matrix[i][j] = sumSquare(matrix, i, j, sqsize)

    m = max(val for row in matrix for val in row)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if m == matrix[i][j]:
                return m, i, j


def addLastColRow(matrix, x, y, size):
    s = 0
    for i in range(size):
        s += matrix[x + size - 1][y + i]
        s += matrix[x + i][y + size - 1]
    s -= matrix[x + size - 1][y + size - 1]
    return s


def generateMatrix(w, h, serial):
    matrix = [0] * w
    for i in range(len(matrix)):
        matrix[i] = []
        matrix[i].append(0)
        for j in range(1, h - 1):
            matrix[i].append(powerLevel(i, j, serial))
    return matrix


def main():
    serial = 5177
    matrix = generateMatrix(301, 301, serial)

    m = 0
    mx, my = 1, 1
    msq = 0

    actsq = 1
    actsize = 0

    # part 1
    expectedSquare = 3
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            try:
                actsize = sumSquare(matrix, i, j, expectedSquare)
            except IndexError:
                continue
            if actsize > m:
                m = actsize
                mx, my = i, j
    print('part 1:', ','.join(map(str, [mx, my])))

    # part 2
    m = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            while actsize >= 0:
                try:
                    actsize += addLastColRow(matrix, i, j, actsq)
                except IndexError:
                    break
                if actsize > m:
                    m = actsize
                    mx, my = i, j
                    msq = actsq
                actsq += 1
            actsq = 1
            actsize = 0
    print('part 2:', ','.join(map(str, [mx, my, msq])))


if __name__ == '__main__':
    main()
