"""
Day 18: Settlers of The North Pole
"""

import copy


def getNeighs(grid, y, x):
    neighs = []
    for i in range(y - 1, y + 2):
        for j in range(x - 1, x + 2):
            if i == y and j == x:
                continue
            neighs.append((i, j))
    ans = []
    for pt in neighs:
        if pt[0] < 0 or pt[1] < 0 or pt[0] >= len(grid) or pt[1] >= len(grid[pt[0]]):
            continue
        ans.append(grid[pt[0]][pt[1]])
    return ans


def evolveSingle(prevGrid, newGrid, y, x):
    if prevGrid[y][x] == '.':
        if sum(1 for x in getNeighs(prevGrid, y, x) if x == '|') >= 3:
            newGrid[y][x] = '|'
        else:
            newGrid[y][x] = '.'
    elif prevGrid[y][x] == '|':
        if sum(1 for x in getNeighs(prevGrid, y, x) if x == '#') >= 3:
            newGrid[y][x] = '#'
        else:
            newGrid[y][x] = '|'
    elif prevGrid[y][x] == '#':
        if sum(1 for x in getNeighs(prevGrid, y, x) if x == '|') >= 1 and sum(1 for x in getNeighs(prevGrid, y, x) if x == '#') >= 1:
            newGrid[y][x] = '#'
        else:
            newGrid[y][x] = '.'


def printGrid(grid):
    for line in grid:
        print(''.join(line))


def evolve(prevGrid, newGrid):
    for y in range(len(prevGrid)):
        for x in range(len(prevGrid[y])):
            evolveSingle(prevGrid, newGrid, y, x)


def resourceValue(grid):
    wood = 0
    lumb = 0
    for line in grid:
        for cell in line:
            if cell == '|':
                wood += 1
            elif cell == '#':
                lumb += 1
    return wood * lumb


def simulateEvolution(grid, minutes):
    d = {}
    streak = 0
    minute = 0
    cycleCondition = 5
    # solusion will use 2 instances - no need to create new one every iteration
    newGrid = copy.deepcopy(grid)

    while minute < minutes:
        evolve(grid, newGrid)
        grid, newGrid = newGrid, grid
        hashkey = resourceValue(grid)
        if hashkey in d:
            streak += 1
            if streak > cycleCondition:
                cycle = minute - d[hashkey]
                minutes = minute + (minutes - minute) % cycle
        else:
            streak = 0
        d[hashkey] = minute

        # just logging
        if (minute + 1) % 100 == 0:
            print('\tit: ', (minute + 1), '/', minutes)
        minute += 1
    return hashkey


def main():
    with open('input.txt', 'r') as f:
        data = f.read().split('\n')

    # create grid
    grid = []
    for line in data:
        grid.append(list(line))

    # part 1
    print('part 1:', simulateEvolution(copy.deepcopy(grid), 10))
    print('part 2:', simulateEvolution(grid, 1000000000))


if __name__ == '__main__':
    main()
