"""
Day 19: Go With The Flow
"""

import re
from math import sqrt


# previous day code
class Machine:
    def __init__(self, regsize):
        self.reg = [0] * regsize
        self.opcodeMapper = [i for i in range(16)]

    def generateMapper(self, statesExapmples):
        mapper = [-1] * 16
        self.opcodeMapper = self.genMapperRec(statesExapmples, 0, mapper)

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
    def getPossibleOps(state, regsize):
        ans = []
        for op in range(16):
            machine = Machine(regsize)
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


def main():
    with open('input.txt', 'r') as f:
        data = f.read().split('\n')
    regsize = 6

    machine = Machine(regsize)
    instructions = []
    ipind = 0
    for line in data:
        if line[0] == '#':
            ipind = int(re.findall(r'[\d]+', line)[0])
            continue
        comm, a, b, c = line.split()
        comm = getattr(machine, comm)
        a, b, c = int(a), int(b), int(c)
        instructions.append((comm, a, b, c))

    # part 1
    ip = 0
    while ip < len(instructions):
        machine.reg[ipind] = ip
        comm, a, b, c = instructions[ip]
        comm(a, b, c)
        ip = machine.reg[ipind]
        ip += 1
    print('part 1:', machine.reg[0])

    # part 2
    ip = 0
    machine.reg = [0] * regsize
    machine.reg[0] = 1

    while machine.reg[0] == 1:
        machine.reg[ipind] = ip
        comm, a, b, c = instructions[ip]
        comm(a, b, c)
        ip = machine.reg[ipind]
        ip += 1
    num = machine.reg[3]
    s = 0
    for i in range(1, int(sqrt(num)) + 1):
        if num % i == 0:
            s += i
            s += num // i
    print('part 2:', s)


if __name__ == '__main__':
    main()
