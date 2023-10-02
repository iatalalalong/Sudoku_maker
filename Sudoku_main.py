
from random import randint, choice
from copy import deepcopy
def boxcheck(ln, cl):
    v1 = 0
    v2 = 2
    v3 = 0
    v4 = 2
    bx= 0

    while bx<= 8:
        if v1 <= ln <= v2 and v3 <= cl <= v4:
            break
        elif v4 < 8:
            bx += 1
            v3 += 3
            v4 += 3
        elif v4 == 8:
            v3 = 0
            v4 = 2
            v1 += 3
            v2 += 3
            bx += 1
    return(bx)

def board_print(title, board):


    print('\n','=-'*4,title,'=-'*4,'\n')
    print(' '*39)
    for c in board:
        if c[0] == 2 or c[0] == 5 or c[0] == 8:
            ul = '\033[4m'
        else:
            ul = '\033[0m'
        if c[3] != '':
            print(f'{ul}| {c[3]} ', end='')
        else:
            print(f'{ul}|   ', end='')
        if c[1] == 8:
            print(f'{ul}|')
        if c[1] == 2 or c[1] == 5:
            print(f'{ul}|', end='')

    return()

print('Welcome to Sudoku - versão Bruno!')
name = input('Type your name:').strip()
level = int(input('Choose your destiny:\n1 - Easy\n2 - Medium\n3 - Hard\nDigite sua resposta (apenas o numero):').strip())
if level == 1:
    limite1 = 27
    limite2 = 35
if level == 2:
    limite1 = 36
    limite2 = 44
if level == 3:
    limite1 = 45
    limite2 = 50

### creating an empty board

while True:
    tile = ['','','','']
    line = [[],[],[],[],[],[],[],[],[]]
    column = [[],[],[],[],[],[],[],[],[]]
    box = [[],[],[],[],[],[],[],[],[]]
    board = []

    for ln in range(0,9):
        for cl in range(0,9):
            tile[0] = ln
            tile[1] = cl
            tile[2] = boxcheck(ln, cl)
            board.append(tile[:])

#assign the first value (random tile and random value)

    first = randint(0,80)
    valor = randint(1,9)
    board[first][3] = valor
    line[board[first][0]].append(valor)
    column[board[first][1]].append(valor)
    box[board[first][2]].append(valor)

#filling the board (finding the tile with less available options, then assign a value)

    try:
        for n in range(0,80):
            less_avail = 9
            tile = ''
            for c in board:
                if c[3] == '':
                    avail = list(set(range(1,10)) - set(line[c[0]] + column[c[1]] + box[c[2]]))
                    if len(avail) < less_avail:
                        less_avail = len(avail)
                        tile = c
            avail = list(set(range(1,10)) - set(line[tile[0]] + column[tile[1]] + box[tile[2]]))
            value = choice(avail)
            tile[3] = value
            line[tile[0]].append(value)
            column[tile[1]].append(value)
            box[tile[2]].append(value)
    except:
        continue
    break

board_print('SUDOKU - GABARITO', board)


###Removing the numbers
#First will clean the lines, then columns, then boxes. Here I want to make sure at least one tile is empty in every line, column and box
i = 0
f = 8
for n in range(0,9):
    idx = randint(i, f)
    i += 9
    f += 9
    line[board[idx][0]].remove(board[idx][3])
    column[board[idx][1]].remove(board[idx][3])
    box[board[idx][2]].remove(board[idx][3])
    board[idx][3] = ''

for n in range(0,9):
    if len(column[n]) == 9:
        cut = choice(column[n])
        for c in board:
            if c[1] == n and c[3] == cut:
                line[c[0]].remove(cut)
                column[c[1]].remove(cut)
                box[c[2]].remove(cut)
                c[3] = ''

for n in range(0,9):
    if len(box[n]) == 9:
        cut = choice(box[n])
        for c in board:
            if c[2] == n and c[3] == cut:
                line[c[0]].remove(cut)
                column[c[1]].remove(cut)
                box[c[2]].remove(cut)
                c[3] = ''

#Now will clean random tiles until it reaches the level of dificulty chosen

condition = ''
prev_tot = ''
while True:
    if condition == 'broken':                 #if the sudoku is 'broken' (due to the last tile removal) it will assign the value back again
        board[keep_index][3] = keep_value
        line[board[keep_index][0]].append(keep_value)
        column[board[keep_index][1]].append(keep_value)
        box[board[keep_index][2]].append(keep_value)
        condition = ''


    empty = 0
    for c in board:  #counting the empty tiles and verifying it meets the level of dificulty chosen
        if c[3] == '':
            empty += 1

    if limite1 < empty < limite2:
        break

    keep_value = ''
    while keep_value == '':
        c = choice(board)  #choose a random tile to clean, and keep it's index and value, in case it 'breaks' the Sudoku
        if c[3] != '':
            keep_index = board.index(c)
            keep_value = c[3]
            line[c[0]].remove(c[3])
            column[c[1]].remove(c[3])
            box[c[2]].remove(c[3])
            board[keep_index][3] = ''
        else:
            keep_value = ''



###SUDOKU SOLVER###
#Now it will try to solve the game to check if it's broken or not

    tot = 1
    board_solver = []
    tile_solver = ['','','','']
    board_copy = deepcopy(board)
    line_copy = deepcopy(line)
    column_copy = deepcopy(column)
    box_copy = deepcopy(box)

    while tot > 0:    #First it will create an empty 'solver-board' and assign the possible values for each empty tile ('avail')
        tot = 0
        for ln in range(0, 9):
            for cl in range(0, 9):
                tile_solver[0] = ln
                tile_solver[1] = cl
                tile_solver[2] = boxcheck(tile_solver[0], tile_solver[1])
                board_solver.append(tile_solver[:])

        for c in board_copy:
            if c[3] == '':
                avail = list(set(range(1,10)) - set(line_copy[c[0]] + column_copy[c[1]] + box_copy[c[2]]))
                board_solver[board_copy.index(c)][3] = avail
            else:
                board_solver[board_copy.index(c)][3] = ''

        cont = 1
        while cont > 0:     #Then will assign the value for each tile that has only one possible solution
            cont = 0
            for c in board_solver:
                if len(c[3]) == 1:
                    board_copy[board_solver.index(c)][3] = c[3][0]
                    line_copy[c[0]].append(c[3][0])
                    column_copy[c[1]].append(c[3][0])
                    box_copy[c[2]].append(c[3][0])
                    c[3] = ''

            for c in board_copy:   #Updating the 'board-solver'
                if c[3] == '':
                    avail = list(set(range(1, 10)) - set(line_copy[c[0]] + column_copy[c[1]] + box_copy[c[2]]))
                    board_solver[board_copy.index(c)][3] = avail

                else:
                    board_solver[board_copy.index(c)][3] = ''


        for c in board_solver:      #checking if there is another 'one answer only'
                if len(c[3]) == 1:
                    cont +=1
                    break

        for c in board_solver:       #checking if the board is solved
            tot += len(c[3])
        if tot == 0:
            break
        else:
            tot = 0

        for n in range(1,10):    #if the board is not solved yet, will try to find a unique value in the avail for each LINE
            inicio = cont = idx = 0
            fim = 9
            while fim < 82:
                for c in range(inicio, fim):
                    for k in range(0,len(board_solver[c][3])):
                        if n == board_solver[c][3][k]:
                            cont += 1
                            idx = c
                if cont == 1:
                    board_copy[idx][3] = n
                    line_copy[board_copy[idx][0]].append(n)
                    column_copy[board_copy[idx][1]].append(n)
                    box_copy[board_copy[idx][2]].append(n)
                    board_solver[idx][3] = ''

                cont = idx = 0
                inicio += 9
                fim += 9

        for c in range(0, 81):    #Updating the 'board-solver'
            if board_copy[c][3] == '':
                avail = list(
                    set(range(1, 10)) - set(line_copy[board_copy[c][0]] + column_copy[board_copy[c][1]] + box_copy[board_copy[c][2]]))
                board_solver[c][3] = avail
            else:
                board_solver[c][3] = ''

        for n in range(1,10):  #if the board is not solved yet, will try to find a unique value in the avail for each COLUMN
            inicio = cont = idx = 0
            while inicio < 9:
                for c in range(inicio, 81, 9):
                    for k in range(0,len(board_solver[c][3])):
                        if n == board_solver[c][3][k]:
                            cont += 1
                            idx = c
                if cont == 1:
                    board_copy[idx][3] = n
                    line_copy[board_copy[idx][0]].append(n)
                    column_copy[board_copy[idx][1]].append(n)
                    box_copy[board_copy[idx][2]].append(n)
                    board_solver[idx][3] = ''

                cont = idx = 0
                inicio += 1

        for n in range(1,10):  #if the board is not solved yet, will try to find a unique value in the avail for each BOX
            for m in range(0,9):
                for c in board_solver:
                    for k in range(0, len(c[3])):
                        if c[2] == m and c[3][k] == n:
                            cont += 1
                            idx = board_solver.index(c)

                if cont == 1:
                    board_copy[idx][3] = n
                    line_copy[board_copy[idx][0]].append(n)
                    column_copy[board_copy[idx][1]].append(n)
                    box_copy[board_copy[idx][2]].append(n)
                    board_solver[idx][3] = ''

                cont = idx = 0


        for c in board_solver:    #will check if the Sudoku is broken (they run the solver twice and didnt find a solution, which means it has more than 1 solution)
            tot += len(c[3])
        if tot == prev_tot != 0:
            condition = 'broken'
            break
        else:
            prev_tot = tot
        board_solver.clear()

board_print('SUDOKU FINAL', board)
