"""
Day 14: Chocolate Charts
"""


class Recipe:
    def __init__(self, recipes, matches, expectedString):
        self.recipes = recipes
        self.elf1 = 0
        self.elf2 = 1
        self.actRecipe = 2
        self.matches = matches
        self.expected = list(map(int, list(str(expectedString))))

    def generateRecipe(self):
        r1 = self.recipes[self.elf1]
        r2 = self.recipes[self.elf2]
        newR = map(int, list(str(r1 + r2)))
        for digit in newR:
            self.recipes.append(digit)
            expectedMatch = self.matches[-1] + 1
            if self.recipes[-1] == self.expected[expectedMatch]:
                self.matches.append(expectedMatch)
                if expectedMatch == len(self.expected) - 1:
                    return len(self.recipes) - len(self.expected)
            else:
                self.matches.append(-1)

        self.actRecipe += 1
        self.elf1 = (self.elf1 + 1 + r1) % len(self.recipes)
        self.elf2 = (self.elf2 + 1 + r2) % len(self.recipes)
        return None


def main():
    data = 704321

    recipe = Recipe([3, 7], [-1, -1], data)
    while len(recipe.recipes) < data + 10:
        recipe.generateRecipe()
    part1ans = recipe.recipes[data:data+10]

    i = 0
    while True:
        i += 1
        ans = recipe.generateRecipe()
        if ans:
            break
        if i % 500000 == 0:
            print('it', i)

    print('part 1:', part1ans)
    print('part 2:', ans)


if __name__ == '__main__':
    main()
