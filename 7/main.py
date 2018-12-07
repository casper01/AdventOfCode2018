"""
Day 7: The Sum of Its Parts
"""

import copy


class VertexMapper:
    def __init__(self):
        self.mapper = []

    def getNum(self, symbol):
        if symbol in self.mapper:
            return self.mapper.index(symbol)
        self.mapper.append(symbol)
        return len(self.mapper) - 1

    def getSymbol(self, num):
        return self.mapper[num]

    def getSize(self):
        return len(self.mapper)


class Graph:
    def __init__(self, n):
        self.n = n
        self.matrix = [0] * n
        self.removed = []
        for i in range(len(self.matrix)):
            self.matrix[i] = [0] * n

    def addEdge(self, vFrom, vTo):
        self.matrix[vFrom][vTo] = 1

    def inDegree(self, v):
        return sum([self.matrix[i][v] for i in range(self.n)])

    def outEdges(self, v):
        return [i for i in range(self.n) if self.matrix[v][i] == 1]

    def removeV(self, v):
        for i in range(self.n):
            self.matrix[i][v] = 0
            self.matrix[v][i] = 0
        self.removed.append(v)

    def isEmpty(self):
        return len(self.removed) == self.n

    def isRemovedV(self, v):
        return v in self.removed


class Worker:
    def __init__(self):
        self.busyTime = 0  # starting worker is not busy

    def canTakeTask(self, taskLen, taskStartTime):
        return taskStartTime >= self.busyTime

    def takeTask(self, taskLen, taskStartTime):
        self.busyTime = taskStartTime + taskLen

    def getFreeTime(self):
        return self.busyTime


def main():
    with open('input.txt', 'r') as f:
        data = f.readlines()

    mapper = VertexMapper()
    edges = []
    for line in data:
        words = line.split()
        vFrom = mapper.getNum(words[1])
        vTo = mapper.getNum(words[7])
        edges.append((vFrom, vTo))

    graph = Graph(mapper.getSize())
    for edge in edges:
        graph.addEdge(edge[0], edge[1])
    graphForP2 = copy.deepcopy(graph)

    ans = []
    while not graph.isEmpty():
        possible_choices = [v for v in range(mapper.getSize()) if graph.inDegree(
            v) == 0 and not graph.isRemovedV(v)]
        best = min(possible_choices, key=lambda x: ord(mapper.getSymbol(x)))
        ans.append(mapper.getSymbol(best))
        graph.removeV(best)

    print("part 1:", ''.join(ans))

    # part 2
    graph = graphForP2
    workersCount = 5
    taskMinTime = 60
    workers = []
    for i in range(workersCount):
        workers.append(Worker())
    time = 0
    removeTime = []

    while not graph.isEmpty():
        # find accessible vertices that are not planned to be removed
        possible_choices = [v for v in range(mapper.getSize()) if graph.inDegree(
            v) == 0 and not graph.isRemovedV(v) and v not in [ver[1] for ver in removeTime]]

        # sort them by finish time
        possible_choices.sort(key=lambda x: ord(
            mapper.getSymbol(x)), reverse=True)

        # try to assign tasks to workers - greedy
        for j in range(min(len(workers), len(possible_choices))):
            taskLen = taskMinTime + \
                ord(mapper.getSymbol(possible_choices[j])) - ord('A') + 1
            for i in range(len(workers)):
                if workers[i].canTakeTask(taskLen, time):
                    workers[i].takeTask(taskLen, time)
                    removeTime.append((time + taskLen, possible_choices[j]))
                    break

        # remove vertex representing task that finishes first
        toRemove = min(removeTime, key=lambda x: x[0])
        time = toRemove[0]
        graph.removeV(toRemove[1])
        removeTime.remove(toRemove)

    # find time when the last worker finishes his work
    end = max(workers, key=lambda x: x.getFreeTime())
    print('part 2:', end.getFreeTime())


if __name__ == '__main__':
    main()
