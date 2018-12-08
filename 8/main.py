"""
Day 8: Memory Maneuver
"""


class Node:
    def __init__(self):
        self.children = []
        self.meta = []


def createTree(data, it):
    n = Node()
    n.children = [0] * data[it]
    n.meta = [0] * data[it + 1]
    it += 2
    for i in range(len(n.children)):
        n.children[i], it = createTree(data, it)
    for i in range(len(n.meta)):
        n.meta[i] = data[it]
        it += 1
    return n, it


def checksum(node):
    return sum(node.meta) + sum(checksum(child) for child in node.children)


def checksum2(node):
    s = 0
    if not node.children:
        return sum(node.meta)

    for m in node.meta:
        if m not in range(len(node.children) + 1):
            continue
        s += checksum2(node.children[m - 1])
    return s


def main():
    with open('input.txt', 'r') as f:
        data = f.read()

    data = list(map(int, data.split()))
    head, _ = createTree(data, 0)
    print('part 1:', checksum(head))
    print('part 2:', checksum2(head))


if __name__ == '__main__':
    main()
