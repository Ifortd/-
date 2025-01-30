import numpy as np


fieldSize = 4
cellsLen = fieldSize
field = np.zeros(cellsLen).reshape(fieldSize, fieldSize)

global cells
cells = []


for i in range(cellsLen):
    cells.append([False, 0, 0])
 # клетки
print(cells)


dead_cells_coords = list(range(36))
dead_current = 0
dead_next = -1

яша = False;
print(field)

'''
текущий елемент индекс= б (0)
последний елмент = 5+1+1%len(dead_cells_coords)
dead_cells_coords = [-,б,в,г,х,ч,н]
'''
def generate_cells(cellsLen):
    '''
    Эта хуйня генерит первые скокото живых штук
    '''
    #num_of_cells = np.random.randint(int(cellsLen/2)) # колво скок будет живо - рандомно по приколу)))
    num_of_cells = 5 #колво скок живо сам задаеш
    for i in range(1, num_of_cells+1):
        cells[i][0] = True
        cells[i][1] = i - 1
        cells[i][2] = i + 1

    cells[1][1] = num_of_cells
    cells[num_of_cells][2] = 0
    # поменяли индексы крайних чтобы норм работало
    return num_of_cells + 1 # не помню зачем но надо
dead_current = generate_cells(cellsLen)
dead_next = dead_current + 1
print(cells)

'''
def add(лист):  #     """ну жобавляем новый елемент в КОНЕЦ СПИСКА"""
    буфер = текущий елмент индекс
    текущий елмент индек = клетка[текущий елмент индекс][2]
    клетка[текущий елмент индекс][1] = буфер


'''

def addCell(id_of_cell, dead_current): # """ добавить елемент перед выбранны """


    ##  у нас всё храниться так [---,[*клетка*,пред клетка индекс, след клетка индекс],---]
    prev = cells[id_of_cell][1] # это мы находим пред елемент
    new_id = dead_current

    cells[prev][2] = new_id
    cells[id_of_cell][1] = new_id # эт мы поменяли индексы в текущей и пред клетке
    # а теперь надо довавить индексы в новой клетке
    cells[new_id][0] = True
    cells[new_id][1] = prev  # добавляем пред клетку в новую клетку
    cells[new_id][2] = id_of_cell # добавляем текущию клетку как след клетку для новой клетки
addCell(3, dead_current)
print(cells)








