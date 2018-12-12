"""
Day 12: Subterranean Sustainability
"""
import re
shift = 0


def state_sum(state, shift):
    return sum(shift + i for i in range(len(state)) if state[i] == '#')


def mutate(state, behaviour, i):
    global shift
    dots = ['.'] * 5

    ans = []
    if state[:5] != dots:
        temp = dots.copy()
        temp.extend(state)
        state = temp
        shift -= 5
    while state[-5:] != dots:
        state.append('.')

    for i in range(len(state)):
        try:
            actSubs = state[i-2:i+3]
            ans.append(behaviour.get(''.join(actSubs), '.'))
        except ValueError:
            ans.append('.')
            continue

    first = max(ans.index('#') - 5, 0)
    last = min(len(ans) - ans[::-1].index('#') + 5, len(ans))
    if first > 0:
        shift += first
    return ans[first:last]


def main():
    global shift
    iterations = 50000000000
    with open('input.txt', 'r') as f:
        data = f.readlines()

    state = "##.#..########..##..#..##.....##..###.####.###.##.###...###.##..#.##...#.#.#...###..###.###.#.#"
    behaviour = {}
    for line in data:
        k, v = line.rstrip().split(' => ')
        behaviour[k] = v

    state = list(state)
    for i in range(iterations):
        if i == 20:
            print('part 1:', state_sum(state, shift))
        
        state = mutate(state, behaviour, i)

        # pattern found
        if i == 1000:
            break

    # part 2
    shift += iterations - 2001
    print('part 2:', state_sum(state, shift))


if __name__ == '__main__':
    main()
