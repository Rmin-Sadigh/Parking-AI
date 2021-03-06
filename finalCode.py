# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#   :::::: P A R K I N G   A I   B Y   A R M I N   G H A Y U R S A D I G H : :  :   :    :     :        :          :
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────

# ────────────────────────────────────────────────────────────────────────────── I ──────────
#   :::::: I M P O R T I N G   L I B R A R I E S : :  :   :    :     :        :          :
# ────────────────────────────────────────────────────────────────────────────────────────

import numpy as np
import copy
import itertools
import threading
import time
import os
import sys

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────── II ──────────
#   :::::: I N I T I A L I Z I N G   V A R I A B L E S   A N D   O B J E C T S : :  :   :    :     :        :          :
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────── NOTICE ─────
# Edit this list according to your problem
# first array represents [rows,columns,number of cars]
# the rest of the arrays are car positions
# make sure the first car is the car you want to get out
# exiting the parking is defined as reaching the right edge
# of the parking so plan your cars accordingly
# ─────────────────────────────────────────────────────────────────── NOTICE ─────

initList = [
    [5, 6, 5],
    [3, 1, "h", 2],
    [3, 3, "v", 2],
    [2, 4, "v", 2],
    [3, 5, "v", 2],
    [2, 6, "v", 2],
]

minMovesReq = 500
idCounter = 0

rows = initList[0][0]
cols = initList[0][1]
if initList[0][2] != len(initList) - 1:
    print(
        "The number of cars in the first array does not match the number of cars defined afterwards. The program will exit. edit the list and run the program again"
    )
    exit()
carNum = initList[0][2]

initList.pop(0)

states = list()
successors = list()

done = False


class state:
    def __init__(self, lst, step):
        self.minMoves = step
        global minMovesReq
        global idCounter

        idCounter = idCounter + 1
        self.ID = idCounter

        self.lst = lst
        self.cars = list()
        for i in range(1, len(lst) + 1):
            self.cars.append(car(i, lst[i - 1]))
        self.schema = np.zeros((rows, cols), dtype=int)
        for carObj in self.cars:
            if carObj.orientation[2] == "v":
                col = carObj.orientation[1] - 1
                startRow = carObj.orientation[0] - 1
                endRow = startRow + carObj.orientation[3] - 1
                for j in range(startRow, endRow + 1):
                    if self.schema[j][col] != 0:
                        print(
                            "Cars number {} and {} have overlap. The program will exit. Edit the list and run the code again.".format(
                                self.schema[j][col], carObj.ID
                            )
                        )
                        exit()
                    self.schema[j][col] = carObj.ID
            else:
                row = carObj.orientation[0] - 1
                startCol = carObj.orientation[1] - 1
                endCol = startCol + carObj.orientation[3] - 1
                for j in range(startCol, endCol + 1):
                    if self.schema[row][j] != 0:
                        print(
                            "Cars number {} and {} have overlap. The program will exit. Edit the list and run the code again.".format(
                                self.schema[row][j], carObj.ID
                            )
                        )
                        exit()
                    self.schema[row][j] = carObj.ID
        self.possibleMoves = dict()
        for carObj in self.cars:
            self.possibleMoves[carObj.ID] = carObj.calcMoves(self.schema)
            if self.possibleMoves[carObj.ID] == []:
                del self.possibleMoves[carObj.ID]

    def moveCar(self, carID, moveStep):
        return self.cars[carID - 1].move(copy.deepcopy(self.lst), moveStep)

    def checkUnique(self, checkList):
        for stateObj in states:
            if np.array_equal(stateObj.lst, checkList):
                return False
            else:
                continue
        return True

    def relief(self):
        for stateObj in states:
            if np.array_equal(stateObj.schema, self.schema):
                if stateObj.minMoves > self.minMoves:
                    stateObj.minMoves = copy.deepcopy(self.minMoves)
                    return

    def checkSucc(self):
        if self.schema[initList[0][0] - 1][cols - 1] == 1:
            return True
        else:
            return False


class car:
    def __init__(self, ID, orientation):
        self.ID = ID
        self.orientation = orientation

    def calcMoves(self, schema):
        domain = []
        if self.orientation[2] == "v":
            col = self.orientation[1] - 1
            startRow = self.orientation[0] - 1
            endRow = startRow + self.orientation[3] - 1

            for i in range(startRow - 1, -1, -1):
                if schema[i][col] == 0:
                    domain.append(i - startRow)
                else:
                    break

            for i in range(endRow + 1, rows, 1):
                if schema[i][col] == 0:
                    domain.append(i - endRow)
                else:
                    break
        else:
            row = self.orientation[0] - 1
            startCol = self.orientation[1] - 1
            endCol = startCol + self.orientation[3] - 1

            for i in range(startCol - 1, -1, -1):
                if schema[row][i] == 0:
                    domain.append(i - startCol)
                else:
                    break

            for i in range(endCol + 1, cols, 1):
                if schema[row][i] == 0:
                    domain.append(i - endCol)
                else:
                    break

        return sorted(domain, reverse=True)

    def move(self, lst, moveStep):
        if lst[self.ID - 1][2] == "v":
            lst[self.ID - 1][0] = lst[self.ID - 1][0] + moveStep
            return lst
        else:
            lst[self.ID - 1][1] = lst[self.ID - 1][1] + moveStep
            return lst


#
# ──────────────────────────────────────────────────────────────────────────────────────────────── III ──────────
#   :::::: T H R E A D   F O R   L O A D I N G   A N I M A T I O N : :  :   :    :     :        :          :
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────
#


def animate():
    for c in itertools.cycle(
        [
            "[      <<<>>>      ]",
            "[     <<<  >>>     ]",
            "[    <<<    >>>    ]",
            "[   <<<      >>>   ]",
            "[  <<<        >>>  ]",
            "[ <<<          >>> ]",
            "[<<<            >>>]",
            "[<<      <>      >>]",
            "[<      <<>>      >]",
        ]
    ):
        if done:
            break
        sys.stdout.write("\rPlease wait while calculations are being done " + c)
        sys.stdout.flush()
        time.sleep(0.1)
    # ────────────────────────────────────────────────────────────────────────────── IV ──────────
    #   :::::: S H O W I N G   T H E   R E S U L T S : :  :   :    :     :        :          :
    # ────────────────────────────────────────────────────────────────────────────────────────
    sys.stdout.flush()
    if len(successors) > 0:
        sys.stdout.write(
            "\r!!       DONE. Min moves required to solve this puzzle is= {}      !!".format(
                minMovesReq
            )
        )
    else:
        sys.stdout.write(
            "\r!!!!!!        This puzzle can't be solved in any ways        !!!!!!"
        )


# ────────────────────────────────────────────────────────────────────────────────────────────────── V ──────────
#   :::::: I N I T I A L I Z I N G   T H E   C A L C U L A T I O N S : :  :   :    :     :        :          :
# ────────────────────────────────────────────────────────────────────────────────────────────────────────────

os.system("cls")
states.append(state(initList, 0))

t = threading.Thread(target=animate)
t.start()

# ────────────────────────────────────────────────────────────────────────────────────────────────── VI ──────────
#   :::::: C R E A T I N G   N E W   S T A T E S   I N   A   L O O P : :  :   :    :     :        :          :
# ────────────────────────────────────────────────────────────────────────────────────────────────────────────

for stateObj in states:
    for key, value in stateObj.possibleMoves.items():
        for steps in value:
            if stateObj.minMoves >= minMovesReq:
                break
            newState = copy.deepcopy(
                state(
                    stateObj.moveCar(key, steps), copy.deepcopy(stateObj.minMoves) + 1
                )
            )
            if stateObj.checkUnique(stateObj.moveCar(key, steps)):
                if key == 1 and steps > 0:
                    states.insert(states.index(stateObj) + 1, newState)
                else:
                    states.append(newState)
            else:
                newState.relief()
    if stateObj.checkSucc():
        successors.append(stateObj)
        minMovesReq = copy.deepcopy(min(stateObj.minMoves for stateObj in successors))

done = True
