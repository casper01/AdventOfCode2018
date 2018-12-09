"""
Day 9: Marble Mania
"""


class Node:
    def __init__(self, val):
        self.val = val
        self.next = self
        self.prev = self


class Dll:
    def __init__(self, initVal):
        self.head = Node(initVal)

    def shift(self, shift):
        while shift > 0:
            self.head = self.head.next
            shift -= 1
        while shift < 0:
            self.head = self.head.prev
            shift += 1

    def add(self, val):
        self.head = self.head.prev

        prevN = self.head
        nextN = self.head.next
        act = Node(val)
        act.prev = prevN
        act.next = nextN
        nextN.prev = act
        prevN.next = act
        self.head = act

    def remove(self):
        prevN = self.head.prev
        nextN = self.head.next
        prevN.next = nextN
        nextN.prev = prevN
        self.head = nextN

    def getVal(self):
        return self.head.val


def game(players, last):
    lastplaced = 0
    pl = 0
    marbles = Dll(0)
    plPoints = [0] * players

    while lastplaced != last:
        lastplaced += 1
        if lastplaced % 1000000 == 0:
            print('it:', lastplaced)

        if not lastplaced % 23 == 0:
            marbles.shift(2)
            marbles.add(lastplaced)
        else:
            plPoints[pl] += lastplaced
            marbles.shift(-7)
            plPoints[pl] += marbles.getVal()
            marbles.remove()
        pl = (pl + 1) % players
    return max(plPoints)


def main():
    players = 405
    last = 70953
    print('part 1:', game(players, last))
    print('part 2:', game(players, 100*last))


if __name__ == '__main__':
    main()
