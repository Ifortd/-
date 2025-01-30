import numpy as np


def add_cell(id_of_cell):  # """ добавить клетку перед текущей клеткой """
    ##  у нас всё храниться так [---,[*клетка*,пред клетка индекс, след клетка индекс],---]
    global dead_current
    global dead_next

    prev = cells[id_of_cell][1]  # это мы находим пред елемент
    new_id = dead_current
    cells[prev][2] = new_id
    cells[id_of_cell][1] = new_id  # эт мы поменяли индексы в текущей и пред клетке
    # а теперь надо довавить индексы в новой клетке
    cells[new_id][0] = True
    cells[new_id][1] = prev  # добавляем пред клетку в новую клетку
    cells[new_id][2] = id_of_cell  # добавляем текущию клетку как след клетку для новой клетки

def gen_empty_cell(): # creates empty cell// создает пустую клетку
    cell = {"type": "none", "heading": 0, "energy": 0, "xy": (0, 0), "genome": 0}
    # type - char[4] - leaf,root, bnch(branch), stem, sead
    # heading - 1 to 4 (0 = up, 3 = left), 0 = NaN
    # energy - -10 to ??? (255)
    # xy
    # genome coord, 0 = NaN
    return cell


def generate_cells(cellsLen):
    '''
    Эта хуйня генерит первые скокото живых штук
    '''
    #num_of_cells = np.random.randint(int(cellsLen/2)) # колво скок будет живо - рандомно по приколу)))
    global dead_current
    global dead_next

    num_of_cells = 5 #колво скок живо сам задаеш
    for i in range(1, num_of_cells+1):
        cells[i][0]["type"] = "DEBUG"
        cells[i][1] = i - 1
        cells[i][2] = i + 1

    cells[1][1] = num_of_cells
    cells[num_of_cells][2] = 0
    # поменяли индексы крайних чтобы норм работало # замкнули

    dead_current = num_of_cells + 1  # не помню зачем но надо
    print(dead_current)
    dead_next = dead_current + 1

   #


def simplified_cells_print(): # debug
    toPrint = []
    for i in cells:

        if i[1] + i[2] > 0:
            i[0] = "Real"
        else:
            i[0] = "XXX"
        toPrint.append(i)

    print("\n", toPrint, "\n len", len(toPrint))



fieldSize = 4 # высота\широта игр.поля
cellsLen = fieldSize ** 2 #  длинна массива с клетками и других связаных (генома, мертвых)
field = np.zeros(cellsLen).reshape(fieldSize, fieldSize) # создаём матрицу


cells = [[gen_empty_cell(),0,0] for _ in range(cellsLen)]  # linked list, with all of the cells // связный список со всеми клетками
dead_cells_coords = list(range(cellsLen))


global dead_current
global dead_next
dead_current = 0
dead_next = -1

genome = [[0,0,0,0,0,0,0] for _ in range(cellsLen)] # array with all of the active genomes (len?)



def setup():

    #for i in range(cellsLen):
    #    cells.append([False, 0, 0])
     # клетки
    #print(cells)

    generate_cells(cellsLen)  # тута создаеём
    print(dead_current)

    яша = False;

    #нонаме - перец с костью


    simplified_cells_print()
    add_cell(3)
    #print(cells)
    simplified_cells_print()


setup()


