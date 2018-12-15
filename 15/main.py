"""
Day 15: Beverage Bandits
"""

import queue


class Unit:
    def __init__(self, type, x, y, game):
        self.x = x
        self.y = y
        self.type = type
        self.enemyT = 'G' if type == 'E' else 'E'
        self.world = game.world
        self.game = game
        self.hp = 200
        self.dmg = 3

    def isAlive(self):
        return self.hp > 0

    def kill(self, dmg):
        self.hp -= dmg
        if not self.isAlive():
            if self.type == 'E' and not self.game.killedElfsAllowed:
                raise ValueError()
            self.world[self.y][self.x] = '.'
            self.type = 'dead'
            self.x = -100
            self.y = -100
            self.dmg = 0

    def getInRange(self):
        ans = []
        for enemy in self.game.units:
            if enemy.type != self.enemyT or not enemy.isAlive():
                continue
            ans.extend(self.getAccessibleNeighbours((enemy.y, enemy.x)))
        return ans

    def getAccessibleNeighbours(self, field):
        ans = []
        if self.world[field[0]-1][field[1]] == '.':
            ans.append((field[0]-1, field[1]))
        if self.world[field[0]][field[1]-1] == '.':
            ans.append((field[0], field[1]-1))
        if self.world[field[0]][field[1]+1] == '.':
            ans.append((field[0], field[1]+1))
        if self.world[field[0]+1][field[1]] == '.':
            ans.append((field[0]+1, field[1]))
        return ans

    def isReachable(self, start, end):
        q = queue.Queue()
        q.put(start)
        visited = [False] * len(self.world)
        for i in range(len(visited)):
            visited[i] = [float('inf')] * len(self.world[i])
        visited[start[0]][start[1]] = 0

        while not q.empty():
            field = q.get()
            dist = visited[field[0]][field[1]]

            if field == end:
                return True, visited

            acc = self.getAccessibleNeighbours(field)
            for a in acc:
                if visited[a[0]][a[1]] != float('inf'):
                    continue
                visited[a[0]][a[1]] = dist + 1
                q.put(a)
        return False, visited

    def getReachable(self, fields):
        mypos = (self.y, self.x)
        ans = []
        for field in fields:
            self.world[self.y][self.x] = '.'
            isreachable, fieldMap = self.isReachable(field, mypos)
            self.world[self.y][self.x] = self.type
            if isreachable:
                ans.append((field, fieldMap))
        return ans

    def getNearest(self, fields):
        mypos = (self.y, self.x)
        bestField, bestMap = min(
            fields, key=lambda f: f[1][mypos[0]][mypos[1]])
        return bestField, bestMap

    def getBestMove(self):
        mypos = (self.y, self.x)
        fieldsInRange = self.getInRange()
        fieldsReachable = self.getReachable(fieldsInRange)
        if not fieldsReachable:
            return mypos
        _, nearestMap = self.getNearest(fieldsReachable)
        neighbours = self.getAccessibleNeighbours((self.y, self.x))
        neighbours.sort(key=lambda n: n[1])
        neighbours.sort(key=lambda n: n[0])
        chosenMove = min(neighbours, key=lambda n: nearestMap[n[0]][n[1]])
        return chosenMove

    def move(self):
        if not self.isAlive():
            return
        if self.tryAttack(self.game.units):
            return

        newPos = self.getBestMove()
        self.world[self.y][self.x] = '.'
        self.y, self.x = newPos
        self.world[self.y][self.x] = self.type

        self.tryAttack(self.game.units)

    def tryAttack(self, enemies):
        closest = []
        for u in self.game.units:
            if u.type == self.enemyT and u.isAlive() and self.game.dist((self.y, self.x), (u.y, u.x)) == 1:
                closest.append(u)
        if not closest:
            return False
        closest = min(closest, key=lambda c: c.hp)
        self.attack(closest)
        return True

    def attack(self, enemy):
        enemy.kill(self.dmg)


class Game:
    def __init__(self, killedElfsAllowed):
        self.resetWorld()
        self.units = []
        self._findCharacters()
        self.rounds = 0
        self.killedElfsAllowed = killedElfsAllowed

    def isOver(self):
        return sum(1 for u in self.units if u.type == 'E') == 0 or sum(1 for u in self.units if u.type == 'G') == 0

    def getBattleRes(self):
        hits = sum(u.hp for u in self.units)
        return (self.rounds-1) * hits

    def dist(self, pt1, pt2):
        return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])

    def _findCharacters(self):
        for y in range(len(self.world)):
            for x in range(len(self.world[y])):
                if self.world[y][x] in ['G', 'E']:
                    self.units.append(Unit(self.world[y][x], x, y, self))

    def playRound(self):
        self.rounds += 1
        self.units.sort(key=lambda u: u.x)
        self.units.sort(key=lambda u: u.y)

        for unit in self.units:
            unit.move()
        self.units = [u for u in self.units if u.isAlive()]

    def print(self):
        for line in self.world:
            print(''.join(line))

    def resetWorld(self):
        with open('input.txt', 'r') as f:
            data = f.read().split('\n')

        self.world = []
        for line in data:
            self.world.append(list(line))

    def updateElfDmg(self, newDmg):
        for u in self.units:
            if u.type == 'E':
                u.dmg = newDmg

    def playGame(self, elfDmg):
        self.updateElfDmg(elfDmg)

        while not self.isOver():
            print('it', self.rounds, '-----------------------')
            self.playRound()

    def elfsWon(self):
        return sum(1 for u in self.units if u.type == 'G') == 0


def main():
    game1 = Game(True)

    # part 1
    game1.playGame(3)
    print('part 1:', game1.getBattleRes())

    # part 2
    game2 = Game(False)
    dmg = 24
    while True:
        print('checking for dmg', dmg)
        try:
            game2.playGame(dmg)
            if game2.elfsWon():
                break
        except ValueError:
            pass
        dmg += 1
        game2 = Game(False)

    print('part 1:', game1.getBattleRes())
    print('part 2:', game2.getBattleRes())


if __name__ == '__main__':
    main()
