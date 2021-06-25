from operator import itemgetter

# Please start with smaller files first because the more te pizzas the slower it will process
# Just change 'input 5' to whatever name of the other input files

file = open('input5', 'r', encoding='utf-8')  # Open input file
linear_problem = [line.replace("\n", "").replace("\t", "").split(' ') for line in file]  # Parse input file

# Remove potential empty strings
i = 0
while i < len(linear_problem):
    j = 0
    while True:
        if j == len(linear_problem[i]):
            break
        elif linear_problem[i][j] == "":
            linear_problem[i].remove("")
            j -= 1
        j += 1
    i += 1

# Parse pizza count and party count for the 3 different party sizes
pizzas = int(linear_problem[0][0])
partySize = []
for i in range(1, 4):
    partySize.append(int(linear_problem[0][i]))

# Create list with pizzas
pizzaList = list()


class pizza:
    ID = int()
    given = bool()  # If certain pizza is given to at least one team this becomes True, else is False
    ingredients = list()


# Parse pizzas from input array
for i in range(1, pizzas + 1):
    p = pizza()
    p.ID = i
    p.given = False
    p.ingredients = list()
    for j in range(1, len(linear_problem[i])):
        p.ingredients.append(linear_problem[i][j])
    pizzaList.append(p)

# Combinations for the groups of 2
combinations = []
combinationsOf2 = []
for i in range(len(pizzaList)):
    for j in range(i + 1, len(pizzaList)):
        ings = list()
        for a in pizzaList[i].ingredients:
            if a not in ings:
                ings.append(a)
        for a in pizzaList[j].ingredients:
            if a not in ings:
                ings.append(a)

        combinationsOf2.append([len(ings) ** 2, i, j])

combinationsOf2.sort(key=itemgetter(0))
combinations += combinationsOf2
del combinationsOf2  # Free up some RAM

# Combinations for the groups of 3
combinationsOf3 = []
for i in range(len(pizzaList)):
    for j in range(i + 1, len(pizzaList)):
        for k in range(j + 1, len(pizzaList)):
            ings = list()
            for a in pizzaList[i].ingredients:
                if a not in ings:
                    ings.append(a)
            for a in pizzaList[j].ingredients:
                if a not in ings:
                    ings.append(a)
            for a in pizzaList[k].ingredients:
                if a not in ings:
                    ings.append(a)

            combinationsOf3.append([len(ings) ** 2, i, j, k])

combinationsOf3.sort(key=itemgetter(0))
combinations += combinationsOf3
del combinationsOf3  # Free up some RAM

# Combinations for the groups of 4
combinationsOf4 = []
for i in range(len(pizzaList)):
    for j in range(i + 1, len(pizzaList)):
        for k in range(j + 1, len(pizzaList)):
            for l in range(k + 1, len(pizzaList)):
                ings = list()
                for a in pizzaList[i].ingredients:
                    if a not in ings:
                        ings.append(a)
                for a in pizzaList[j].ingredients:
                    if a not in ings:
                        ings.append(a)
                for a in pizzaList[k].ingredients:
                    if a not in ings:
                        ings.append(a)
                for a in pizzaList[l].ingredients:
                    if a not in ings:
                        ings.append(a)
                combinationsOf4.append([len(ings) ** 2, i, j, k, l])

combinationsOf4.sort(key=itemgetter(0))
combinations += combinationsOf4
del combinationsOf4  # Free up some RAM

combinations.reverse()

# Select from highest to lowest score to give every pizza
# For every potential remaining pizzas there is a combination that covers them
# Attention for 5 remaining pizzas(can contain 2-3, 4, only 4 2 or 3)

bestCombs = list()  # List to put best combinations
availCount = pizzas  # It counts available pizzas
for comb in combinations:

    # If the remaining available pizzas are 5, the algorithm must check whether or not there is a team of 3 and a team of 2
    if availCount == 5:
        # Seek valid comb of 3 pizzas
        for combof3 in combinations:
            validCombof3 = True
            if len(combof3) == 4:
                for p in combof3[1:]:
                    if pizzaList[p].given or not partySize[1] > 0:
                        validCombof3 = False
                        break
            else:
                validCombof3 = False

            # if still valid combo of 3
            if validCombof3:
                # Pretend to give the combo of 3 to correctly check for valid combo of 2
                for i in combof3[1:]:
                    pizzaList[i].given = True

                # Seek valid comb of 2 pizzas
                for combof2 in combinations:
                    validCombof2 = True
                    if len(combof2) == 3:
                        for p in combof2[1:]:
                            if pizzaList[p].given or not partySize[0] > 0:
                                validCombof2 = False
                                break
                    else:
                        validCombof2 = False

                    if validCombof2:
                        # Give both comb of 3 and of 2 and add them to list
                        for i in combof2[1:]:
                            pizzaList[i].given = True

                        bestCombs.append(combof3)
                        bestCombs.append(combof2)
                        partySize[0] -= 1
                        partySize[1] -= 1
                        availCount -= 5
                        break

                # if there is no valid
                if availCount != 0:
                    for i in combof3[1:]:
                        pizzaList[i].given = False

    pizCount = len(comb[1:])
    validComb = True
    # Check wehter on not the combination is valid
    for p in comb[1:]:
        if pizzaList[p].given or not partySize[pizCount - 2] > 0:
            validComb = False
            break

    # If it is valid give the pizzas
    if validComb:
        partySize[pizCount - 2] -= 1
        bestCombs.append(comb)
        availCount -= pizCount
        for i in comb[1:]:
            pizzaList[i].given = True

Teams = len(bestCombs)
bestCombs.reverse()

print('-----------Combinations-----------')
print(bestCombs)
print('----------Remaining Teams-----------')
print(partySize)
print('-------------Points-------------')

points = 0
for c in bestCombs:
    points += c[0]

print(points)

# Print the results into a file
f = open("output", "w")
f.write(str(Teams) + "\n")

for c in bestCombs:
    f.write(str(len(c[1:])) + " " + str(c[1:]).replace("[", "").replace("]", "").replace(",", "") + "\n")

f.close()

file.close()
