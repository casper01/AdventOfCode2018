"""
Day 2: Inventory Management System
"""


def mode(dic):
    ans = 1
    for val in dic.values():
        if val == 3:
            ans *= 3
        elif val == 2:
            ans *= 2
    return ans


def getCommonLets(id1, id2):
    ans = []
    for i in range(min(len(id1), len(id2))):
        if id1[i] == id2[i]:
            ans.append(id1[i])
    return ''.join(ans)


def main():
    with open('input.txt', 'r') as f:
        d = f.readlines()

    # part 1
    two = 0
    three = 0

    for idd in d:
        dic = {}
        for let in idd:
            dic[let] = dic.get(let, 0) + 1
        if mode(dic) % 2 == 0:
            two += 1
        if mode(dic) % 3 == 0:
            three += 1
    print('part 1:', two * three)

    # part 2
    maxVal = 0
    ans = []

    for bid1 in d:
        for bid2 in d:
            if bid1 == bid2:
                continue
            temp = getCommonLets(bid1, bid2)
            if len(temp) > maxVal:
                maxVal = len(temp)
                ans = temp
    print('part 2:', ans)


if __name__ == '__main__':
    main()
