"""
Day 24: Immune System Simulator 20XX
"""

import re


class Group:
    def __init__(self, id, type, units, hp, dmg, attackType, initiative, weaknesses, immunities):
        self.id = id
        self.type = type
        self.units = units
        self.hp = hp
        self.dmg = dmg
        self.attackType = attackType
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities

    def hashKey(self):
        return str(self.id) + str(self.units) + str(self.hp) + str(self.dmg) + self.attackType + str(self.initiative) + str(self.weaknesses) + str(self.immunities)

    def effectivePower(self):
        return self.units * self.dmg

    def estimateDmg(self, attacker):
        dmg = attacker.effectivePower()
        if attacker.attackType in self.immunities:
            dmg = 0
        elif attacker.attackType in self.weaknesses:
            dmg *= 2
        return dmg

    def isKilled(self):
        return self.units <= 0

    def killUnits(self, dmg):
        unitsToKill = dmg // self.hp
        self.units -= unitsToKill
        self.units = 0 if self.units < 0 else self.units

    def takeEnemyWithMostDmg(self, defendingGroups, forbiddenGroups):
        defendingGroups.sort(key=lambda d: d.initiative, reverse=True)
        defendingGroups.sort(key=lambda d: d.effectivePower(), reverse=True)
        defendingGroups.sort(key=lambda d: d.estimateDmg(self), reverse=True)
        for dg in defendingGroups:
            if dg.hashKey() not in forbiddenGroups and dg.estimateDmg(self) > 0:
                return dg
        return None


def targetSelection(attackingGroups, defendingGroups):
    attackingGroups.sort(key=lambda x: x.initiative, reverse=True)
    attackingGroups.sort(key=lambda x: x.effectivePower(), reverse=True)

    chosen = set()
    pairs = []
    for attacker in attackingGroups:
        bestAim = attacker.takeEnemyWithMostDmg(defendingGroups, chosen)
        if bestAim:
            chosen.add(bestAim.hashKey())
            pairs.append((attacker, bestAim))
    return pairs


def attacking(pairs1, pairs2):
    pairs1.extend(pairs2)
    pairs = pairs1
    pairs.sort(key=lambda p: p[0].initiative, reverse=True)

    for attacker, aim in pairs:
        if attacker.isKilled() or aim is None:
            continue
        estimatedDmg = aim.estimateDmg(attacker)
        aim.killUnits(estimatedDmg)


def fightRound(army1, army2):
    targets12 = targetSelection(army1, army2)
    targets21 = targetSelection(army2, army1)
    attacking(targets12, targets21)
    return targets12 or targets21


def fight(immuneSystemArmy, infectionArmy):
    notDraw = True
    while notDraw and immuneSystemArmy and infectionArmy:
        notDraw = fightRound(immuneSystemArmy, infectionArmy)
        immuneSystemArmy = [
            i for i in immuneSystemArmy if not i.isKilled()]
        infectionArmy = [i for i in infectionArmy if not i.isKilled()]
    return immuneSystemArmy, infectionArmy


def constructGroups(data, armyName, boost=0):
    groups = []
    id = 1
    for line in data:
        group = list(map(int, re.findall(r'[\d]+', line)))
        if not group:
            continue
        units, hp, dmg, initiative = list(map(int, re.findall(r'[\d]+', line)))
        dmg += boost

        l = line.split()
        attackType = l[l.index('damage') - 1]

        immunities = re.findall(r'[\(; ]+immune to [\S\s]+?[\);]', line)
        if immunities:
            immunities = [i.strip() for i in immunities[0][11:-1].split(',')]

        weaknesses = re.findall(r'[\(; ]+weak to [\S\s]+?[\);]', line)
        if weaknesses:
            weaknesses = [w.strip() for w in weaknesses[0][9:-1].split(',')]

        g = Group(id, armyName, units, hp, dmg, attackType,
                  initiative, weaknesses, immunities)
        groups.append(g)
        id += 1
    return groups


def main():
    with open('input.txt', 'r') as f:
        data = f.read().split('\n')

    # part 1
    armyInd = data.index('Infection:')
    immuneSystemArmy = constructGroups(data[:armyInd], 'Immune')
    infectionArmy = constructGroups(data[armyInd:], 'Infection')
    immuneSystemArmy, infectionArmy = fight(immuneSystemArmy, infectionArmy)
    ans = sum(i.units for i in immuneSystemArmy) + \
        sum(i.units for i in infectionArmy)
    print('part 1:', ans)

    # part 2
    minBoost = 0
    maxBoost = 1000
    actBoost = (minBoost + maxBoost) // 2
    while minBoost < maxBoost:
        # Immune system army
        immuneSystemArmy = constructGroups(data[:armyInd], 'Immune', actBoost)
        # Infection
        infectionArmy = constructGroups(data[armyInd:], 'Infection')

        # fight till one of the teams is killed or draw
        immuneSystemArmy, infectionArmy = fight(
            immuneSystemArmy, infectionArmy)

        if not infectionArmy:
            # we won
            maxBoost = actBoost
        else:
            # we failed
            minBoost = actBoost + 1
        actBoost = (minBoost + maxBoost) // 2

    ans = sum(i.units for i in immuneSystemArmy) + \
        sum(i.units for i in infectionArmy)
    print('part 2:', ans)


if __name__ == '__main__':
    main()
