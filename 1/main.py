"""
Day 1: Chronal Calibration
"""


def main():
    with open('input.txt', 'r') as f:
        data = f.readlines()

    # part 1
    ans = 0
    for line in data:
        ans += int(line)

    print("part 1:", ans)

    d = {}
    ans = 0
    d[0] = True
    while 1:
        for line in data:
            line = int(line)
            ans += line
            if ans in d:
                print("part 2:", ans)
                return
            else:
                d[ans] = True
    print(d)


if __name__ == '__main__':
    main()
