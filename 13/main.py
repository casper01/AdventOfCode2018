"""
Day 13: Mine Cart Madness
"""


class Cart:
    def __init__(self, world, x, y):
        self.x = x
        self.y = y
        self.world = world
        self.lastIntersection = 0
        self.prevMove = self.generatePrevMove(self.world[y][x])
        self.predictMyPlace()
        self.killed = False

    def predictMyPlace(self):
        if self.world[self.y-1][self.x] not in ['-', ' '] and self.world[self.y+1][self.x] not in ['-', ' '] and self.world[self.y][self.x-1] not in ['|', ' '] and self.world[self.y][self.x+1] not in ['|', ' ']:
            self.world[self.y][self.x] = '+'
        elif self.world[self.y-1][self.x] not in ['-', ' '] and self.world[self.y+1][self.x] not in ['-', ' ']:
            self.world[self.y][self.x] = '|'
        elif self.world[self.y][self.x-1] not in ['|', ' '] and self.world[self.y][self.x+1] not in ['|', ' ']:
            self.world[self.y][self.x] = '-'
        elif (self.world[self.y+1][self.x] not in ['-', ' '] and self.world[self.y][self.x+1] not in ['|', ' ']) or (self.world[self.y-1][self.x] not in ['-', ' '] and self.world[self.y][self.x-1] not in ['|', ' ']):
            self.world[self.y][self.x] = '/'
        else:
            self.world[self.y][self.x] = '\\'

    def getPossibleMoves(self):
        if self.world[self.y][self.x] == '+':
            return [(self.y-1, self.x), (self.y+1, self.x), (self.y, self.x-1), (self.y, self.x+1)]
        if self.world[self.y][self.x] == '-':
            return [(self.y, self.x-1), (self.y, self.x+1)]
        if self.world[self.y][self.x] == '|':
            return [(self.y-1, self.x), (self.y+1, self.x)]
        if self.world[self.y][self.x] == '/':
            if self.y >= 0 and self.x >= 0 and self.world[self.y - 1][self.x] not in [' ', '-'] and self.world[self.y][self.x - 1] not in [' ', '|']:
                return [(self.y-1, self.x), (self.y, self.x-1)]
            else:
                return [(self.y+1, self.x), (self.y, self.x+1)]
        if self.world[self.y][self.x] == '\\':
            if self.x >= 0 and self.y < len(self.world) and self.world[self.y][self.x-1] not in [' ', '|'] and self.world[self.y+1][self.x] not in [' ', '-']:
                return [(self.y+1, self.x), (self.y, self.x-1)]
            else:
                return [(self.y-1, self.x), (self.y, self.x+1)]
        print('ERROR. No possible moves')
        raise Exception()

    def generatePrevMove(self, actState):
        if actState == '<':
            return (self.y, self.x + 1)
        elif actState == '>':
            return (self.y, self.x - 1)
        elif actState == '^':
            return (self.y + 1, self.x)
        elif actState == 'v':
            return (self.y - 1, self.x)
        else:
            print('ERROR: cannot generate prev move')
            raise Exception()

    def move(self):
        moves = self.getPossibleMoves()
        if self.prevMove in moves:
            moves.remove(self.prevMove)
        if len(moves) == 1:
            self.prevMove = (self.y, self.x)
            self.y, self.x = moves[0]
            return

        actMove = (self.y, self.x)
        # turning left
        if self.lastIntersection == 0:
            if self.prevMove[0] < self.y:
                self.x += 1
            elif self.prevMove[0] > self.y:
                self.x -= 1
            elif self.prevMove[1] < self.x:
                self.y -= 1
            elif self.prevMove[1] > self.x:
                self.y += 1
        # go straight
        elif self.lastIntersection == 1:
            if self.prevMove[0] < self.y:
                self.y += 1
            elif self.prevMove[0] > self.y:
                self.y -= 1
            elif self.prevMove[1] < self.x:
                self.x += 1
            elif self.prevMove[1] > self.x:
                self.x -= 1
        # go right
        if self.lastIntersection == 2:
            if self.prevMove[0] < self.y:
                self.x -= 1
            elif self.prevMove[0] > self.y:
                self.x += 1
            elif self.prevMove[1] < self.x:
                self.y += 1
            elif self.prevMove[1] > self.x:
                self.y -= 1

        self.prevMove = actMove
        self.lastIntersection = (self.lastIntersection + 1) % 3

    def kill(self):
        self.killed = True


def main():
    with open('input.txt', 'r') as f:
        world = f.read()

    world = [list(line) for line in world.split('\n')]

    carts = []
    actPoses = {}
    for y in range(len(world)):
        for x in range(len(world[y])):
            if world[y][x] in ['<', '>', '^', 'v']:
                cart = Cart(world, x, y)
                carts.append(cart)
                actPoses[(y, x)] = cart

    while True:
        carts.sort(key=lambda c: c.x)
        carts.sort(key=lambda c: c.y)
        for cart in carts:
            if cart.killed:
                continue
            del actPoses[(cart.y, cart.x)]
            cart.move()
            if (cart.y, cart.x) in actPoses:
                actPoses[(cart.y, cart.x)].kill()
                cart.kill()
                del actPoses[(cart.y, cart.x)]
                print("Part 1: Collision at", cart.x, cart.y)
            else:
                actPoses[(cart.y, cart.x)] = cart
        carts = [c for c in carts if not c.killed]
        if len(carts) <= 1:
            print('Part 2: last: ', carts[0].x, carts[0].y)
            break


if __name__ == '__main__':
    main()
