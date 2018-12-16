"""
Day 16: Chronal Classification
"""

import re
import ast


class Machine:
    def __init__(self):
        self.reg = [0] * 4
        self.opcodeMapper = [i for i in range(16)]

    def generateMapper(self, statesExapmples):
        mapper = [-1] * 16
        self.opcodeMapper = self.genMapperRec(statesExapmples, 0, mapper)
        print(self.opcodeMapper)

    def genMapperRec(self, examples, i, mapper):
        while True:
            print(i, mapper)
            # success, solution found
            if i >= len(examples):
                return mapper
            state = examples[i]
            ops = self.getPossibleOps(state)
            if mapper[state.opcode] != -1:
                if mapper[state.opcode] in ops:
                    i += 1
                else:
                    return False
            else:
                break
        for op in ops:
            if op in mapper:
                continue
            mapper[state.opcode] = op
            testSol = self.genMapperRec(examples, i + 1, mapper)
            if testSol:
                return testSol
            mapper[state.opcode] = -1
        return False

    @staticmethod
    def getPossibleOps(state):
        ans = []
        for op in range(16):
            machine = Machine()
            machine.reg = state.before[:]
            machine.command(op, state.a, state.b, state.c)
            if machine.reg == state.after:
                ans.append(op)
        return ans

    def command(self, opcode, a, b, c):
        opcode = self.opcodeMapper[opcode]
        if opcode == 0:
            return self.addr(a, b, c)
        elif opcode == 1:
            return self.addi(a, b, c)
        elif opcode == 2:
            return self.mulr(a, b, c)
        elif opcode == 3:
            return self.muli(a, b, c)
        elif opcode == 4:
            return self.banr(a, b, c)
        elif opcode == 5:
            return self.bani(a, b, c)
        elif opcode == 6:
            return self.borr(a, b, c)
        elif opcode == 7:
            return self.bori(a, b, c)
        elif opcode == 8:
            return self.setr(a, b, c)
        elif opcode == 9:
            return self.seti(a, b, c)
        elif opcode == 10:
            return self.gtir(a, b, c)
        elif opcode == 11:
            return self.gtri(a, b, c)
        elif opcode == 12:
            return self.gtrr(a, b, c)
        elif opcode == 13:
            return self.eqir(a, b, c)
        elif opcode == 14:
            return self.eqri(a, b, c)
        elif opcode == 15:
            return self.eqrr(a, b, c)

    def addr(self, a, b, c):
        self.reg[c] = self.reg[a] + self.reg[b]

    def addi(self, a, b, c):
        self.reg[c] = self.reg[a] + b

    def mulr(self, a, b, c):
        self.reg[c] = self.reg[a] * self.reg[b]

    def muli(self, a, b, c):
        self.reg[c] = self.reg[a] * b

    def banr(self, a, b, c):
        self.reg[c] = self.reg[a] & self.reg[b]

    def bani(self, a, b, c):
        self.reg[c] = self.reg[a] & b

    def borr(self, a, b, c):
        self.reg[c] = self.reg[a] | self.reg[b]

    def bori(self, a, b, c):
        self.reg[c] = self.reg[a] | b

    def setr(self, a, b, c):
        self.reg[c] = self.reg[a]

    def seti(self, a, b, c):
        self.reg[c] = a

    def gtir(self, a, b, c):
        self.reg[c] = 1 if a > self.reg[b] else 0

    def gtri(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] > b else 0

    def gtrr(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] > self.reg[b] else 0

    def eqir(self, a, b, c):
        self.reg[c] = 1 if a == self.reg[b] else 0

    def eqri(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] == b else 0

    def eqrr(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] == self.reg[b] else 0


class State:
    def __init__(self, before, after, opcode, a, b, c):
        self.before = before
        self.after = after
        self.opcode = opcode
        self.a = a
        self.b = b
        self.c = c


def findRec(allOptions, i, mapper):
    if i >= len(allOptions):
        return mapper
    actOptions = allOptions[i]
    for option in actOptions:
        # option already used
        if option in mapper:
            continue
        mapper[i] = option
        testSol = findRec(allOptions, i + 1, mapper)
        if testSol:
            return testSol
        mapper[i] = -1
    # there is no solution or we dont use all commands
    return False


def main():
    with open('input.txt', 'r') as f:
        data = f.read().split('\n')

    # data for part 1
    states = []
    for i in range(0, len(data), 4):
        try:
            before = ast.literal_eval(re.findall(r'\[[0-9, ]*\]$', data[i])[0])
            opcode, a, b, c = map(int, data[i+1].split())
            after = ast.literal_eval(re.findall(
                r'\[[0-9, ]*\]$', data[i+2])[0])
            states.append(State(before, after, opcode, a, b, c))
        except IndexError:
            algInd = i
            break

    # data for part 2
    algorithm = []
    for i in range(algInd, len(data)):
        if len(data[i]) > 4:
            opcode, a, b, c = map(int, data[i].split())
            algorithm.append(State(None, None, opcode, a, b, c))

    # part 1
    cnt = 0
    for state in states:
        if len(Machine.getPossibleOps(state)) >= 3:
            cnt += 1
        elif len(Machine.getPossibleOps(state)) == 0:
            print(state.before, state.after,
                  state.opcode, state.a, state.b, state.c)
    print('part 1:', cnt)

    # part 2
    mapper = [set([i for i in range(16)]) for _ in range(16)]
    for state in states:
        possibleOps = Machine.getPossibleOps(state)
        mapper[state.opcode] = mapper[state.opcode] & set(possibleOps)
    for i in range(len(mapper)):
        mapper[i] = list(mapper[i])

    realMapper = [-1] * 16
    realMapper = findRec(mapper, 0, realMapper)

    machine = Machine()
    machine.opcodeMapper = realMapper

    for comm in algorithm:
        machine.command(comm.opcode, comm.a, comm.b, comm.c)
    print('part 2:',  machine.reg[0])


if __name__ == '__main__':
    main()
