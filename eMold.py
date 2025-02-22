import numpy as np
import sys
import pygame
import random


def create_first_cell(): # УБЕЙСЯ # вот через этот костыль создаем первую клетку, шоб не рыгать потом эрорами
    global dead_current
    global dead_last
    dead_current += 1
    cells[1][0]["type"] = "root"

def create_cells_debug(cells_number):
# generate cells тоже самое\\
# только сука женерейт целлс не работает, эта же штука аккуратно обвалакивает cells и dead_cells шоб индексы не сломались, вот прям вкусно и НЕ ТРОГАТЬ


    #блять просто иди нахуй
    # тут вроде фулл вручную создаются первые две клетки
    global dead_current
    cells[1][2] = 2
    change_cell_root_debug(1)
    change_cell_root_debug(2)
    cells[2][1] = 1
    dead_current = 3
    """эт я токошо создал вручную первые две клетки ибо так бог сказал """
    simplified_cells_print(cells)
    print()
    # принтим клетки ибо шоб ловить уродов

    #cells_number = 4

    for i in range(2,cells_number):
        cell_id = add_cell_lnkl(2)
        change_cell_root_debug(cell_id)
    #cell_id = add_cell_lnkl(2)
    #change_cell_root_debug(cell_id)
    # тут я черещ уже нормальную функцию создал клетки перед второй клеткой, ибо ну ну ну ну, свзяь плохая, потом перезвонишь

    simplified_cells_print(cells)
    # принтим клетки ибо шоб ловить уродов


    """print("Создаем клетки прост по преколу \n")
    create_cell_debug()
    global first_cell
    cell_id = first_cell
    n = 0
    while(n<4):
        add_cell_lnkl(cell_id)
        change_cell_root_debug(cell_id)
        cell_id = get_dead()
        n += 1

    first_cell = cell_id
    print(cells)
    print()"""



def add_cell_lnkl(id_of_cell):  # """ добавить клетку перед текущей клеткой """ # УДАРЬ МЕНЯ Я НЕ РАБОТАЮ, та всё тише, уже работаешь
    ##  у нас всё храниться так [---,[*клетка*,пред клетка индекс, след клетка индекс],---]
    global dead_current
    global dead_last

    prev = cells[id_of_cell][1]  # это мы находим пред елемент
    new_id = get_dead()
    cells[prev][2] = new_id
    cells[id_of_cell][1] = new_id  # эт мы поменяли индексы в текущей и пред клетке
    # а теперь надо довавить индексы в новой клетке
    #cells[new_id][0] = True
    cells[new_id][1] = prev  # добавляем пред клетку в новую клетку
    cells[new_id][2] = id_of_cell  # добавляем текущию клетку как след клетку для новой клетки
    return new_id # возврат айди созданной клетики

def create_cell_debug(): # хз, не трогай, чёто мутное и страшное, спрашивай беззымянника


    global dead_current
    global dead_last
    cell_id = dead_current
    dead_current += 1
    cells[cell_id][0]["type"] = "DEBUG"
    change_cell_root_debug(cell_id)

def randomize_cells_coords(fieldSize): # рандомайзит коорды клеток, на удивление даже использует нормальную проходку
    print("================================================================")
    print("RANDOMIZING COORDS")
    print()
    global first_cell
    current_cell_id = first_cell
    generated = True

    while(current_cell_id != 0):

        # тут прикол что если мы случайно создали клетку на коордах уже существующей клетки, то надо кабы хуйня переделывать
        # для этого мы чекаем поле, а точнее не существует ли на таких то коордах клетки
        # проверяем мы это через указаный индекс на квадратике поля, если индекс 0, значит тут нет реальной клетки и всё норм
        # а если индекс не 0, значит тут есть клетка (ИЛИ КОГДА ТО БЫЛА, НО ПОСКОЛЬКО МЫ ИСПАОЛЬЗУЕМ ЭТУ ФУНКЦИЮ В САМОМ НАЧАЛЕ ЭТО НЕВАЖНО)
        # генерим ХУ - чекаем не занято ли место по этим ХУ на поле - если занято, переделываем

        generated = False
        while(generated == False):

            cells[current_cell_id][0]["xy"] = (random.randint(0, fieldSize - 1), random.randint(0, fieldSize - 1))
            x, y = cells[current_cell_id][0]["xy"]
            blockCellId = field[x][y][0]  # это индекс клетки на координатах текущей клетки
            generated = True
            print("block cell id", blockCellId)
            if blockCellId != 0: # мы чекаем шо за индекс у клетки на коордах где мы хотим создать новую клетку, если индекс 0, значит там нет клетки, а если не 0, значит перезодаем
                generated = False

        x, y = cells[current_cell_id][0]["xy"]
        field[x][y][0] = current_cell_id # добавляем индекс клетки в поле на свои координаты

        current_cell_id = next_cell(current_cell_id)
    print("RANDOMIZING FINISHED")
    print("========================================")
    print()



def change_cell_root_debug(моль): # блять что это # Я НЕ ТОРЧ
    cells[моль][0]["type"] = "root"
    return "заебись)"

def remove_cell_lnkl(cell_id): # убрать клетку с линкед листа # ХЕЗЕШКА, не провереня функция
    global dead_current
    global dead_last

    prev = cells[cell_id][1] # индекс перпедыдущей клетки
    next = cells[cell_id][2] # индексик след клетки
    cells[prev][2] = next # заменяем индекс предыдущей клетки на индекс клетки следующей от текущей
    cells[next][1] = prev # заменяем индекс следующей клетки на  индекс передущей клетки
    add_dead(cell_id) # добавляем клетку в очередь мертвяков


def gen_empty_cell(): # creates empty cell// создает пустую клетку // использувется только при спавне поля, дальше не юзать
    cell = {"int type": 0, "type": "none", "heading": 0, "energy": 0, "xy": (-1, -1), "genome": 0, "links": 0, "active gene": 0 , "mutation rate": 0, "energy consumption": 0}
    # type - char[4] - leaf,root, bnch(branch), stem, sead
    # heading - 1 to 4 (0 = up, 3 = left), 0 = NaN
    # energy - -10 to ??? (255)
    # xy
    # genome coord, 0 = NaN
    # links 2 - forward, 4 - right, 8 - back, 16 - left
    # active gene - current active gene
    # mutatation rate - 0-1 - chance of mutation
    # energy consumption - потребление енергии за ход
    return cell



def generate_cells(cellsLen): # УБЕЙСЯ # чёт мутное с очередью мертвых тут происходит
    '''
    Эта хуйня генерит первые скокото живых штук
    '''
    #num_of_cells = np.random.randint(int(cellsLen/2)) # колво скок будет живо - рандомно по приколу)))
    global dead_current
    global dead_last

    num_of_cells = 5 #колво скок живо сам задаеш
    for i in range(1, num_of_cells+1):
        cells[i][0]["type"] = "DEBUG"
        cells[i][1] = i - 1
        cells[i][2] = i + 1

    cells[1][1] = num_of_cells
    cells[num_of_cells][2] = 0
    # поменяли индексы крайних чтобы норм работало # замкнули

    dead_current = num_of_cells + 1  # не помню зачем но надо

    dead_last = dead_current + 1
    print(dead_current, dead_last)



def simplified_cells_print(cells): # debug
    toPrint = ["XXX",0,0]

    for i in cells:

        #if i[0]["type"] == "root":
        toPrint[0] = i[0]["type"]
        toPrint[1] = i[1]
        toPrint[2] = i[2]
        print(toPrint)



def get_genome(cell): # NO VALIDATION - can be performed on any cell
    return genomes(cell["genome"]) # ааа, ну это точно недоделано

def create_cell(xy): # лол что
    pass

def genome_traverse(cell): # NO VALIDATION  # проходка по геному
    genome = get_genome(cell)

    for i in range(3):
        if genome[i]//32 <= 2:
            create_cell()
        elif genome[i]//32 == 4:
            create_cell()
        elif genome[i]// 32 == 5:
            create_cell()


def kill_cell(cell_ind): # убить клетку
    """
    :param cell_ind: - индекс клетки
    надо занести клетку в очередь мертвых клеток -add_to_queue(cell_index)
    и удалить её из связоного списка живых - kill_cell(cell_index)
    и удалить её из поля - в тупую поменять тип клетки напрямую через поле
    Разбросать енергию на клетки рядом (НАДО СДЕЛАТЬ)
    И ПОМЕНЯТЬ ЛИНКИ ПРИЛЕГАЮШИХ КЛЕТОК
    тут используем links клетки (массив из 4 булиан елементов где нулвеой - вверх, третий - лево, первый право)

    :return: - нихуя
    """

def consume_energy(cell_ind): # потребляем енергию
    cell = cells[cell_ind][0]
    print(cells[cell_ind])
    cells[cell_ind][0]["energy"] = cell["energy"] - cell["energy consumption"] # кушоем енергию
    if cells[cell_ind][0]["energy"] < 0:
        return 1 # если енергии меньше 0, то посылаем сигнал шоб сдохнуть
    return 0


def produce_energy(cell_ind): # производим энергию ок да
    global яша
    cell = cells[cell_ind][0]
    if cell["type"] == "leaf":
        cells[cell_ind][0]["energy"] += 15 # УДАРЬ МЕНЯ, я имею ввиду 15 потом перенести в переменную leaf_energy_prod
    elif cell["type"] == "root":
        cells[cell_ind][0]["energy"] += яша # ТУТ НАДО ОТДЕЛЬНАЯ ФУННКЕЦИЯ ДЛЯ ВЫКАЧИВАНИЯ ЕНЕРГИИ ИЗ ПОЧВЫ


def organics_check(cell): # чек органики на текущей клетке
    xy = cell["xy"]
    print("корды ", xy)
    if field[xy[0]][xy[1]][1] > 64: # если органики больше 128, то подых # УДАРЬ МЕНЯ, тут 64 потом в переменную перенести
        return 1
    return 0

def upd_cell(cell_ind):  # связная функция, которая трогает каждую клетку, вызывает все остальные функции и переформатриуерт (нет) выходы входы функций шоб всё стыковалось
    death = 0 # не умираем
    cell = cells[cell_ind][0]
    death += consume_energy(cell_ind) # потрбляем енергию
    produce_energy(cell_ind) # производим энерегию (если мы листок иль корешок)
    death += organics_check(cell)



def get_abs_heading(abs_rot, nada_rot): # сделано кирикой, берет относительное напрваление клетки (типо справо от клетки, спереди, слева), и выдаёт абсолютное направление (1 - вверх, 4 - лево)
    """
    Надо функцию которая берет на вход абсолютное направлние клетки, желаемое относительное направление и выдаёт абсолютное направление для относительного напрваление
    :param abs_rot: Направление 0 - никуда, 1 - вверх, 4 - влево  (2 вправо, 3 вниз)
    :param nada_rot: Желаемое направление - 1 - влево, 2 - впероед, 3- вправо 4 - зад
    :return: абсолютное направление для относительного напрваление
    """
    if abs_rot == 0:
        return nada_rot
    adekvat_cord = {1: -1, 2: 0, 3: 1, 4: 2} # переназначаю ваші ебанутіе координаті ібо нехуй
    res = (abs_rot + adekvat_cord[nada_rot]) % 4
    if res == 0:
        res = 4
    return res

def move_energy(arr, now_energy, want_energy=1000, min_energy=0, prioryty=None): # ИСПОЛЬЗОВАТЬ ЧРЕЗ БУФЕРНУЮ ФУНКЦИЮ # ебаный пиздец (сделано киркой), при помощи неких темных манипуляций (не ебу) равномерно распределяет свободную енергию в соседей
    """
    крч типо передает енерегию из целевой клекти в соседей и ахуеть
    :param arr: значит двумерный массив по структре [[*тип клетку сверху*,*кол-во енергии в этой клетке*],[*тип клетку справа*,*кол-во енергии в этой клетке*],[...,...],[...,...]]
    :param now_energy: кол-во свободной енергии, это енергия которую клетка должна отдать (забейте как мы откуда её знаем, просто эту енергию надо распередлить)
    :param want_energy: мы ж хотели ещё параметр желаемого кол-ва енергии (опционален), по дефолту дохуя ставим чтобі не на что не влияло
    :param min_energy: минимально желаемое колво енергии которое хотим иметь (опционально, закидка на гены)
    :param prioryty: список в каком порядке делать обход соседей (опционально, закидка потом для генов)
    :return: новое колво енергии у текущей клетки после передачи
    """
    if prioryty is None:
        prioryty = {1: 0, 2: 1, 3: 2, 4: 3}  # ключи єто расположение (1 - вверрх и далье по часовой), а значения ето порядок обхода (по дефолту совпадают)

    if min_energy >= now_energy:
        return now_energy  # если у нас уже енергии меньше чем мы хотим иметь в минимуме, то нихуя не отдаем и все

    averange = now_energy - min_energy # почитаем суму енергии у всех соседей, ну и сразу нас закидіваем

    x = 0
    for i in range(1, len(arr)+1):

        if (arr[prioryty[int(i)]][0] not in [False]):
            if arr[prioryty[i]][1] < now_energy and arr[prioryty[i]][1] < want_energy:
                # сюда вместо фолс список с типами клеток в которіе не засовіваем енергию
                averange += arr[prioryty[i]][1]
                x += 1
    if x == 0:
        return now_energy # если какогото хуя никому не можем передать то всьо

    averange2 = int(averange/x) # вот крч считаем по скок отдаем

    for i in range(1, len(arr)+1): # вот отдаем типо
        if arr[prioryty[i]][0] not in [False] and arr[prioryty[i]][1] < now_energy and arr[prioryty[i]][1] < want_energy:
            arr[prioryty[i]][1] = averange2
    return min_energy + averange - averange2 * x # посчитали скок у нас осталось когда все отдали

def next_cell(cell_id): # это для получения след елмента линкед листа с клетками
    return cells[cell_id][2]



def add_dead(cell_id): # добавить мертвяка в конец очереди # ХЕЗЕШКА, не проверено
    global dead_last
    global cells_len
    dead_last += 1
    dead_last = dead_last % cells_len
    dead_cells_coords[dead_last] = cell_id
    # в целом тут немного шурли мурли и добавляем клетку в конец очереди

def get_dead(): # достать мертвяка из начала очереди # ХЕЗЕШКА, не проверено
    global dead_current
    global cells_len
    cell_id = dead_cells_coords[dead_current]
    dead_current += 1
    dead_current = dead_current % cells_len
    return cell_id
    # тут возвращаем айди мертвяка

def render_leaf_a(x,y): # made by беззымянникк

    global block_size
    x = x+ int((block_size/2))
    y = y + int((block_size / 2))
    rad = int(block_size / 2)

    pygame.draw.circle(SCREEN, (0, 175, 0), (x, y), rad)
    pygame.draw.circle(SCREEN, (0, 122, 0), (x, y), rad, 3)


def get_axy_from_fxy(fx,fy): # даем колонку и строку, получаем абсолютные коорды левого верхнего края этой клетки
    global block_size
    ax = block_size * fx
    ay = block_size * fy
    return ax, ay

def render(arg): # Рендерит поле, и клетки на нём
    block_size, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK = arg
    global render_mode
    global first_cell # мне надо

    for event in pygame.event.get():  # Выход при нажатии на крестик
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    match (render_mode): # отрисовка самого поля
        case 0:
            pass
        case 1: # anderfan
            draw_grid(arg)
        case 2: # no-name
            draw_grid_безымянник_эдитион(arg) # рисуем базовое пустое поле




    match (render_mode): # отрисовка елементов самого поля (корни, ростки, листья и прочая моль)
        case 0:
            pass
        case 2:

            current_cell_id = first_cell

            while (current_cell_id != 0):
                fx, fy = cells[current_cell_id][0]["xy"]
                ax, ay = get_axy_from_fxy(fx,fy)

                #rect = pygame.Rect(ax, ay, block_size, block_size)
                #col = (0,255,0)
                #pygame.draw.rect(SCREEN, col, rect, 0)

                current_cell_id = next_cell(current_cell_id)

                render_leaf_a(ax,ay)

        case 1: #
            block_size, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK = arg

            for cell in cells: # Тут идёт проверка на то словарь ли ли в cell[0] # чё это нахуй значит
                if isinstance(cell[0], dict): #и если нет, то читаю координаты и рисую # что это за исинстанце, это кто вам давал доступ к запретному плоду встроенных функций
                    if cell[0]["type"] != "none":
                        x, y = cell[0]["xy"]
                        print(cell[0]["xy"])
                        pygame.draw.circle(SCREEN, NEW_CELL, (x, y), 13) # А ХУЛЕ РАДИУС ЭТО КОНСТАНТА
                else: #а если да, то ругаюсь. Это сделано потому, что в add_cell последние из cells являются bool-ами
                    print(cell)
                    print(f"Invalid data type: {type(cell[0])}")


    pygame.display.update()



def draw_grid(arg): # ебаный рот подсмешок, де коменты сука, давно реактивный пе-8 не выкачивал?
    # Set the size of the grid block # что это блять
    block_size, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK = arg
    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)

            pygame.draw.rect(SCREEN, BLACK, rect, 1)


def draw_grid_безымянник_эдитион(arg): # рисуем поле путем беззымянника, ибо я хз шо в функции сверху происходит
    block_size, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK = arg
    global fieldSize
    #fieldX = 0
    #fieldY = 0

    # fx/fy - field related X and Y (columns and rows)
    # ax/ay - absolute X and Y (actual pixel coodrinates)                           ІдІ нахуй
    # первое это колонки\строки, а второе это коорды пикселей

    for fx in range(0,fieldSize):
        for fy in range(0,fieldSize):
            ax = block_size * fx
            ay = block_size * fy

            rect = pygame.Rect(ax, ay, block_size, block_size)

            col = fieldCols[fx][fy][0]

            pygame.draw.rect(SCREEN, col, rect, 0)


def randomize_cols_a_bit(): # установить для каждой ячейки поля чуть чуть отличюшийся цвет
    global fieldSize
    for x in range(fieldSize):
        for y in range(fieldSize):
            chanLevel = random.randint(240,250) # channel level for each R, G and B
            chanDevLevel = random.randint(-5,5) #channel deviation level
            newCol = (chanLevel+chanDevLevel,chanLevel-chanDevLevel,chanLevel)
            fieldCols[x][y][0] = newCol

#### end render


global cells_len
global fieldSize
fieldSize = 16 # высота\широта игр.поля
cells_len = fieldSize ** 2 #  длинна массива с клетками и других связаных (генома, мертвых)

field = [[[0,0] for j in range(fieldSize)] for i in range(fieldSize)] # создаем матрицу с двух-мерным массивом, в пизду нумпи
fieldCols = [[[(255,0,0),(255,255,255)] for j in range(fieldSize)] for i in range(fieldSize)] # это отдельный массив с цветами для клеток, почему так, спросите беззымянника


# Проверяем \\ КОГО, О ЧЕМ ТЫ


cells = [[gen_empty_cell(),0,0] for _ in range(cells_len)]  # linked list, with all of the cells // связный список со всеми клетками
global first_cell
first_cell = 1
dead_cells_coords = list(range(cells_len)) ## ааа, ээээ, ну это помоему очередб с пустыми индексами в cells



global яша
яша = 42
global dead_current # начало очереди
global dead_last # конец очереди
dead_current = 1
dead_last = -1
dead_last = cells_len - 1
# это были указатели начала и конца очереди
print(dead_cells_coords)
print(dead_current)
print(dead_last)
#print(cells)

genomes = [[0 for __ in range(12)] for _ in range(cells_len)] # array with all of the active genomes (len?)


##### render varibables
block_size = 30 # размеры квадратиков поля
global SCREEN, CLOCK
global render_mode # режим рендера
render_mode = 2 # 1 - подсмешок база, 2 - беззымянник # 0 - залагать и умереть)

# ну тут цвета
BLACK = (29, 51, 74)
WHITE = (255, 255, 255)
NEW_CELL = (52, 201, 36)

# ну тут хз чёто наврнео очень нужное
WINDOW_WIDTH = fieldSize * block_size
WINDOW_HEIGHT = fieldSize * block_size
pygame.init()  # вот это должно быть в сетапе
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()  # вот это время в чем то как то ну там спрашивайте ПодСмешка
SCREEN.fill(WHITE)
arg = block_size, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK  # моль)

radius = float(block_size / 30)  # радиус кружочка, шоб он как раз в клетку влазил


"""
легенда для комментов:
УДАРЬ МЕНЯ - чёт сломано, но немного может и работает
УБЕЙСЯ - не использовать, всё сломает
ХЕЗЕШКА - должно работать, но нормально не проверено

"""


def setup():
    #generate_cells(cellsLen)  # тута создаеём # хуйня, чёто мутное
    randomize_cols_a_bit()

    #нонаме - перец с костью
    create_cells_debug(6) # УДАРЬ МЕНЯ \\ шутка генерит клетки, работает и ладно, слава целостности cells
    randomize_cells_coords(fieldSize) # рандомазит коорды стартовых клеток, максмимальная залупа, использовать только и тут и сейчас, оно тупое и еле дышит
    #simplified_cells_print()
    #add_cell_lnkl(3) # ахах ты лох, переделуй) нихуя не працює)))))
    #print(cells)
    #simplified_cells_print()
    # print(genome)
    pass


def update():
    global first_cell
    traverse = True
    current_cell_id = first_cell # я ебу? фирст целл = 1, хуле? # Да завали, работает же # Сьебал, уже не ебу сколько и где оно менятеся, но всё ещё работает
    current_cell = cells[current_cell_id][0]
    print("current cell id", current_cell_id)
    while(current_cell_id != 0):

        upd_cell(current_cell_id)
        current_cell_id = next_cell(current_cell_id)
        print("current cell id", current_cell_id)


def loop():
    n = 0

    while(n<5 or True):
        #update()
        render(arg)
        n += 1

setup()
loop()



# credits: ТриГнома (ПодСмешок, Беззыммянникк, Кирка) )