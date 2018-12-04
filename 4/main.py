"""
Day 4: Repose Record
"""

from operator import attrgetter
import datetime


class Date:
    def __init__(self, y, m, d, h, mi):
        self.y = int(y)
        self.m = int(m)
        self.d = int(d)
        self.h = int(h)
        self.mi = int(mi)
        self.full = datetime.datetime(self.y, self.m, self.d, self.h, self.mi)


class Log:
    def __init__(self, date, action):
        self.date = date
        self.action = action

    def getId(self):
        for part in self.action.split():
            if part[0] == '#':
                return part[1:]
        return '?'


def main():
    with open('input.txt', 'r') as f:
        data = f.readlines()

    # parsing data
    logs = []
    for line in data:
        y, m, d = line[1:].split()[0].split('-')
        h, mi = line.split()[1][:-1].split(':')
        date = Date(y, m, d, h, mi)
        logs.append(Log(date, ' '.join(line.split()[2:])))

    # sorting data
    logs.sort(key=attrgetter('date.y', 'date.m',
                             'date.d', 'date.h', 'date.mi'))
    
    # finding asleep time for every minute
    guards = {}
    actGuard = logs[0].getId()
    start = None
    end = None

    for i in range(len(logs)):
        if logs[i].action.split()[0] == 'Guard':
            actGuard = logs[i].getId()
        if logs[i].action == 'falls asleep':
            start = logs[i].date.full
        if logs[i].action == 'wakes up':
            end = logs[i].date.full
            if not actGuard in guards:
                guards[actGuard] = [0] * 60
            while start != end:
                guards[actGuard][start.minute] += 1
                start += datetime.timedelta(minutes=1)

    # part 1
    mostAsleep = max([sum(v) for v in guards.values()])
    guard = next(g for g in guards.keys() if sum(guards[g]) == mostAsleep)
    minute = guards[guard].index(max(guards[guard]))
    ans = int(guard) * minute
    print('part 1:', ans)

    # part 2
    maxMinAsleep = max([max(v) for v in guards.values()])
    guard = next(g for g in guards.keys() if max(guards[g]) == maxMinAsleep)
    minute = guards[guard].index(maxMinAsleep)
    ans = int(guard) * minute
    print('part 2:', ans)


if __name__ == '__main__':
    main()
