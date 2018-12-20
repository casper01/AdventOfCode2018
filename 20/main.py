"""
Day 20: A Regular Map
"""
import queue


def findEnclosingParenthesisAndSplits(data, start):
    i = start
    lvl = 0
    splits = []
    splits.append(start)
    while True:
        if data[i] == '(':
            lvl += 1
        elif data[i] == ')':
            lvl -= 1
        elif data[i] == '|' and lvl == 1:
            splits.append(i)
        if lvl == 0:
            splits.append(i)
            return i, splits
        i += 1


def addEdge(maze, fromE, toE):
    if fromE not in maze:
        maze[fromE] = []
    if toE not in maze:
        maze[toE] = []
    maze[fromE].append(toE)
    maze[toE].append(fromE)
    return maze


def walk(data):
    maze = {}
    actPos = (0, 0)
    active = set()
    pending = []
    sleeping = []
    active.add(actPos)

    for i in range(len(data)):
        if data[i] == 'N':
            newactive = set()
            for pos in active:
                newpos = pos[0], pos[1] - 1
                maze = addEdge(maze, pos, newpos)
                newactive.add(newpos)
            active = newactive
        elif data[i] == 'S':
            newactive = set()
            for pos in active:
                newpos = pos[0], pos[1] + 1
                maze = addEdge(maze, pos, newpos)
                newactive.add(newpos)
            active = newactive
        elif data[i] == 'W':
            newactive = set()
            for pos in active:
                newpos = pos[0] - 1, pos[1]
                maze = addEdge(maze, pos, newpos)
                newactive.add(newpos)
            active = newactive
        elif data[i] == 'E':
            newactive = set()
            for pos in active:
                newpos = pos[0] + 1, pos[1]
                maze = addEdge(maze, pos, newpos)
                newactive.add(newpos)
            active = newactive
        elif data[i] == '(':
            pending.append(active)
            sleeping.append([])
        elif data[i] == '|':
            sleeping[-1].extend(active)
            active = pending[-1]
        elif data[i] == ')':
            pending.pop()
            active.update(set(sleeping.pop()))
    return maze


def findLongestPath(maze):
    visited = {}
    unvisitedLeft = len(maze.keys())
    q = queue.Queue()
    q.put((0, 0))
    visited[(0, 0)] = 0
    maxdist = -1

    while not q.empty():
        pos = q.get()
        d = visited[pos]
        if maxdist < d:
            maxdist = d
        for neighs in maze[pos]:
            if neighs in visited:
                continue
            visited[neighs] = visited[pos] + 1
            unvisitedLeft -= 1
            q.put(neighs)
    return maxdist


def findLongerPath(maze, minDoors):
    visited = {}
    unvisitedLeft = len(maze.keys())
    q = queue.Queue()
    q.put((0, 0))
    visited[(0, 0)] = 0
    counter = 0

    while not q.empty():
        pos = q.get()
        d = visited[pos]
        if minDoors <= d:
            counter += 1
        for neighs in maze[pos]:
            if neighs in visited:
                continue
            visited[neighs] = visited[pos] + 1
            unvisitedLeft -= 1
            q.put(neighs)
    return counter


def main():
    with open('input.txt', 'r') as f:
        data = f.read()

    data = data[1:-1]
    maze = {}
    maze = walk(data)
    print('part1:', findLongestPath(maze))
    print('part1:', findLongerPath(maze, 1000))


if __name__ == '__main__':
    main()
