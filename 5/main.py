"""
Day 5: Alchemical Reduction
"""


def getFullyReacting(data):
    stack = []

    for el in data:
        stack.append(el)

        if len(stack) < 2:
            continue

        change = True
        while change:
            change = False
            if len(stack) < 2:
                break
            a = stack[-1]
            b = stack[-2]
            if a != b and a.lower() == b.lower():
                stack.pop()
                stack.pop()
                change = True
    return ''.join(stack)


def removePolymer(data, pol):
    ans = []
    for d in data:
        if d.lower() == pol.lower():
            continue
        ans.append(d)
    return ''.join(ans)


def main():
    with open('input.txt', 'r') as f:
        data = f.read()

    # data = 'dabAcCaCBAcCcaDA'
    ans = []

    print('part 1:', len(getFullyReacting(data)))

    for pol in range(ord('A'), ord('Z') + 1):
        p = chr(pol)
        tempData = removePolymer(data, p)
        tempData = getFullyReacting(tempData)
        ans.append(len(tempData))

    print('part 2:', min(ans))


if __name__ == '__main__':
    main()
