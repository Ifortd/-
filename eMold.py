import numpy as np
import sys
import pygame
import random
import pygame_widgets as pg_w
from pygame_widgets.button import Button

def create_first_cell(): # УБЕЙСЯ # вот через этот костыль создаем первую клетку, шоб не рыгать потом эрорами
    global dead_current
    global dead_last
    dead_current += 1
    cells[1][0]["type"] = "root"

def grow_cell(parent_cell_id, heading, new_type, new_energy=0): # Вот это штука которая выращиевт новые клетки # ХЕЗЕШКА
    global fieldSize
    child_x = cells[parent_cell_id][0]["xy"][0]
    child_y = cells[parent_cell_id][0]["xy"][1]
    # НЕ ЗАБУДЬ ПРО КРАЯ ПОЛЯ УБЕЙСЯ
    # heading - 1 up, ... , 4 - left
    if heading == 2:
        child_x += 1
    elif heading == 4:
        child_x -= 1
    elif heading == 1:
        child_y -= 1
    elif heading == 3:
        child_y += 1
    else:
        child_y = 0
        child_x = 0

    if (child_x < 0 or child_x > fieldSize) or (child_y < 0 or child_y > fieldSize):
        print("при создании новой клетки вышли за границы")
        return False

    if field[child_x][child_y][0] == 0:

        #child_cell_id = get_dead()
        child_cell_id = add_cell_lnkl(parent_cell_id) # БОЖЕ ПОЖАЛЙСУТА РАБОТАЙ ГНИДА\ СЛАВА БОГУ ЦЕЛОСТНОСТИ
        heading = heading -1 # ибо масисы та с 0 начинатеься

        cells[parent_cell_id][0]["linksB"][heading] = child_cell_id # добавляем линк в родителя

        child_link_heading = (heading +  2 ) % 4 # это куда линк в родителя от ребенка (точнее напрвление, типо если родитель создал ребенка справа, то у ребенка линк должен быть влево)
        cells[child_cell_id][0]["linksB"][child_link_heading] = parent_cell_id # добавляем линк в чадо

        # ВОТ ТУТ СОЗДАЕМ САМО ЧАДО

        cells[child_cell_id][0]["type"] = new_type
        cells[child_cell_id][0]["energy"] = new_energy
        field[child_x][child_y][0] = child_cell_id # ложим по чадо в поле на соответсвущие координаты
        cells[child_cell_id][0]["xy"] = (child_x, child_y) # ну кабы коорды в клеть записываем
        cells[child_cell_id][0]["heading"] = heading + 1 # хз, так надо
        return True
    else:
        print("попытка создать клетку в клетку, неудача")
        return False

def change_to_leaf(cell_id):
    cells[cell_id][0]["type"] = "leaf"
    enrg_cons = 15

    cells[cell_id][0]["energy"] = 234634623547425734574573457  # вот тут не уверен


def create_Игорь_debug(): # игорь)
    global dead_current

    cells[0][2] = 1

    # добавляем в линкед лист
    cells[1][2] = 2

    cells[2][1] = 1
    cells[2][2] = 3

    cells[3][1] = 2 # leaf
    # меняем типы
    cells[1][0]["type"] = "stem"
    cells[2][0]["type"] = "bnch"
    cells[3][0]["type"] = "leaf"
    cells[3][0]["energy"] = 200

    # трогаем очередь мертвых
    dead_current = 4

    # направление
    cells[1][0]["heading"] = 4
    cells[2][0]["heading"] = 4
    cells[3][0]["heading"] = 4

    # линки
    cells[1][0]["links"] = 8  # росток
    cells[2][0]["links"] = 8+ 4 #2 + 8  # 1 2 4 8  # стебель
    cells[3][0]["links"] = 1#8  # листок

    cells[1][0]["linksB"][1] = 2
    cells[2][0]["linksB"][2] = 3
    cells[2][0]["linksB"][3] = 1
    cells[3][0]["linksB"][0] = 2

    # трогем коорлинаты
    startX = 4
    startY = 4

    cells[1][0]["xy"] = (startX, startY)
    field[startX][startY][0] = 1
    cells[2][0]["xy"] = (startX+1, startY)
    field[startX+1][startY][0] = 2
    #cells[3][0]["xy"] = (startX+2, startY)
    #field[startX + 2][startY][0] = 3
    cells[3][0]["xy"] = (startX + 1, startY + 1)
    field[startX + 1][startY + 1][0] = 3




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

def create_cell_debug(): # УБЕЙСЯ # хз, не трогай, чёто мутное и страшное, спрашивай беззымянника


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
    global first_cell_LEGACY
    current_cell_id = first_cell_LEGACY
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
    cell = {"int type": 0, "type": "none", "heading": 0, "energy": 0, "xy": (-1, -1), "genome": 0, "links": 0, "linksB":[0,0,0,0], "active gene": 0 , "mutation rate": 0, "energy consumption": 0}
    # type - char[4] - leaf,root, bnch(branch), stem, sead
    # heading - 1 to 4 (1 = up, 4 = left), 0 = NaN
    # energy - -10 to ??? (255)
    # xy
    # genome coord, 0 = NaN
    # links 1 up , 2 - right, 4 - down, 8 - left, НЕТ НИХУЙЯ, ЛИНКИ АБСОЛЮТНЫ, НЕ ОТНОСИТЕЛЬНЫ # ЛЕГАСИ
    # linksB - спроси чего попроще
    # active gene - current active gene
    # mutatation rate - 0-1 - chance of mutation
    # energy consumption - потребление енергии за ход # ЭТО СОН СОБАКИ И ЛЕГАСИ, ЭТО В ОТЕДЬНОЙ ГЛОБ ПЕРЕМННОЙ БУДЕ
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
    if cell["energy"] < 200:
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
    print("===========================================================================")
    print("current cell id", cell_ind)
    death = 0 # не умираем
    cell = cells[cell_ind][0]
    death += consume_energy(cell_ind) # потрбляем енергию
    print("current cell ", cell["type"], "enetrgy ", cell["energy"])
    #move_energy(cell_ind)
    move_energy_b(cell_ind)
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

def get_nearby_cells(cell_id): # ХЕЗЕШКА # Получить клетки рядом с выбранной клеткой
    current_cell = cells[cell_id][0]
    nearby_cells = [0, 0, 0, 0] # массив с клетками рядом, 0 - вверх, 3 - лево
    x, y = current_cell["xy"] # ху текущей клетки

    # получаем индексы клетком рядом
    nearby_cells[0] = field[x][y-1][0]
    nearby_cells[1] = field[x+1][y][0]
    nearby_cells[2] = field[x][y + 1][0]
    nearby_cells[3] = field[x - 1][y][0]
    return nearby_cells

def get_f_links(cell_id): # переформатировать # ЛЕГАСИ
    current_cell = cells[cell_id][0]
    links = [0,0,0,0]
    test_bit = 1

    print()
    for shift in range(4):
        if (test_bit << shift & current_cell["links"] > 0):
            links[shift] = 1
    return links



def get_linked_cells(cell_id): # УДАРЬ МЕНЯ, плохо написанная функция # шо это вообше такое
    current_cell = cells[cell_id][0]
    linked_cells =get_f_links(cell_id)  # мммасссиввв с клетулями, отформатированный линкс (где на индексе 0 - вверх, индекс 3 - лево)
    x, y = current_cell["xy"]  # ху текущей клетки
    nearby_cells = get_nearby_cells(cell_id)


    for i in range(4):
        nearby_cells[i] = linked_cells[i] * nearby_cells[i]

    #print("nearby cells", nearby_cells)
    return nearby_cells

def move_energy_b(cell_id): # та самая буферная функция которая пузырит и формамит штуки шоб впихнуть в мув_енерджи_кор
    current_cell = cells[cell_id][0]

    if current_cell["type"] != "stem" and current_cell["type"] != "none": # мы не хотим передавать энергию пустых клетко и ростков
        nearby_cells = current_cell["linksB"] # массив с индексками соседних клетко - [*индекс клетки сверху*, *индекс клетки справа*, ..., ...]
        f_nearby_cells = [[0, 0] for i in range(4)]


        for i in range(4): # форматим под кор функцию
            tmp_cell_id = nearby_cells[i]
            tmp_cell = cells[tmp_cell_id][0]

            f_nearby_cells[i][1] = tmp_cell["energy"] # энергию надо обязательно передать
            if tmp_cell_id == 0 or tmp_cell["type"] == "leaf": # если это указатель на фантомную (0) клеть или листок, то в него енергию не передаем
                f_nearby_cells[i][0] = False
            else:
                f_nearby_cells[i][0] = True

        rem_energy, o_nearby_cells = move_energy_core(f_nearby_cells, current_cell[
            "energy"])  # УДАРЬ МЕНЯ, тут пока просто даём всю энергию, а не свободную, шо кабы не очень
        # rem_energy - remaining energy for current cell
        # o_nearby_cells - output nearby cells, energy for neaby cells
        print("rem energy", rem_energy, cells[cell_id][0]["type"], cells[cell_id][0]["energy"])
        print("\n o_nearby_cells ", o_nearby_cells)
        cells[cell_id][0]["energy"] = rem_energy # тут вставляем оставшуюся енергию в текущиюе клеть

        for i in range(4): # а тут раздаем соседям их новую енергию
            tmp_cell_id = nearby_cells[i]
            cells[tmp_cell_id][0]["energy"] = o_nearby_cells[i][1]


    elif current_cell["type"] == "none":
        print()
        print("Чёт ты накосячил: попытка передать энергию из пустой клетки (чекай move_energy_b)")
        input("Нажми enter что бы продолжить ")



def move_energy_LEGACY(cell_id): # та самая буферная функция которая пузырит и формамит штуки шоб впихнуть в мув_енерджи_кор

    current_cell = cells[cell_id][0]
    if current_cell["type"] != "stem" or current_cell["type"] != "none": # чёт там валидация шоб из пустого в порожнее не лить энергию
        nearby_cells = get_nearby_cells(cell_id) # клетки рядом
        nearby_cells = get_linked_cells(cell_id)
        f_nearby_cells = [[0,0] for i in range(4)] # formatted for move energy core (значит двумерный массив по структре [[*тип клетку сверху*,*кол-во енергии в этой клетке*])

        for i in range(4): # форматим под кор функцию
            tmp_cell_id = nearby_cells[i]
            tmp_cell = cells[tmp_cell_id][0]


            f_nearby_cells[i] = [True, tmp_cell["energy"]]
            if tmp_cell_id == 0 or tmp_cell["type"] == "leaf":
            #f_nearby_cells[tmp_cell_id] = [ tmp_cell["type"], tmp_cell["energy"] ] # берем кол-во енергии и тип

                f_nearby_cells[i][0] = False

        print("\n nearby cells pure ", nearby_cells)
        print(" f nearby cells ", f_nearby_cells)
        rem_energy, o_nearby_cells = move_energy_core(f_nearby_cells, current_cell["energy"] ) # УДАРЬ МЕНЯ, тут пока просто даём всю энергию, а не свободную, шо кабы не очень
        # rem_energy - remaining energy for current cell
        # o_nearby_cells - output nearby cells, energy for neaby cells
        print("rem energy", rem_energy, cells[cell_id][0]["type"],cells[cell_id][0]["energy"])
        print("\n aboba ", o_nearby_cells)


        cells[cell_id][0]["energy"] = rem_energy

       # for tmp_cell_id in range(4): # вставляем енергию в соседнии клетки
        #    cells[tmp_cell_id][0]["energy"] = o_nearby_cells[tmp_cell_id][1]

        for i in range(4):
            tmp_cell_id = nearby_cells[i]
            cells[tmp_cell_id][0]["energy"] = o_nearby_cells[i][1]


    elif current_cell["type"] == "none":
        print()
        print("Чёт ты накосячил: попытка передать энергию из пустой клетки (чекай move_energy)")
        input("Нажми enter что бы продолжить ")





def move_energy_core(arr, now_energy, want_energy=1000, min_energy=0, prioryty=None): # ИСПОЛЬЗОВАТЬ ЧРЕЗ БУФЕРНУЮ ФУНКЦИЮ # ебаный пиздец (сделано киркой), при помощи неких темных манипуляций (не ебу) равномерно распределяет свободную енергию в соседей
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
        return [now_energy, arr]  # если у нас уже енергии меньше чем мы хотим иметь в минимуме, то нихуя не отдаем и все

    averange = now_energy - min_energy # почитаем суму енергии у всех соседей, ну и сразу нас закидіваем

    x = 0
    for i in range(1, len(arr)+1):

        if (arr[prioryty[int(i)]][0] not in [False]):
            if ((arr[prioryty[i]][1] < now_energy) and (arr[prioryty[i]][1] < want_energy)):
                # сюда вместо фолс список с типами клеток в которіе не засовіваем енергию
                print("енергія соседа которого дабвляем ", arr[prioryty[i]][1])
                averange += arr[prioryty[i]][1]
                x += 1
    if x == 0:
        return [now_energy, arr] # если какогото хуя никому не можем передать то всьо

    averange2 = int(averange/x) # вот крч считаем по скок отдаем
    print("averange2 ", averange2 )
    for i in range(1, len(arr)+1): # вот отдаем типо
        if arr[prioryty[i]][0] not in [False] and arr[prioryty[i]][1] < now_energy and arr[prioryty[i]][1] < want_energy:
            arr[prioryty[i]][1] = averange2

    now_energy = min_energy + averange - averange2 * x # посчитали скок у нас осталось когда все отдали
    return [now_energy, arr]

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
    cell_id = dead_cells_coords[dead_current] # достаем индекс мертвяка
    dead_current += 1 # указатель инкрементируем на 1 (ну шоб на след мертвяка укащывал)
    dead_current = dead_current % cells_len # если мы вышли за границы массива, вовзарт в начало массива
    return cell_id
    # тут возвращаем айди мертвяка

def render_leaf_a(x,y): # made by беззымянникк

    global block_size
    x = x+ int((block_size/2))
    y = y + int((block_size / 2))
    rad = int(block_size / 2)

    pygame.draw.circle(SCREEN, (0, 175, 0), (x, y), rad)
    pygame.draw.circle(SCREEN, (0, 122, 0), (x, y), rad, 3)

def render_branch_a(x,y,cell_id=0):
    global block_size
    # c - center
    xc = x + int((block_size / 2))
    yc = y + int((block_size / 2))
    rad = int(block_size / 2)
    col = (64, 64, 64)
    width = 5

    links = cells[cell_id][0]["linksB"]
    coords = [(xc, y),(x + block_size, yc),(xc, y + block_size),(x, yc)]

    for link in range(4):
        if links[link] != 0:
            pygame.draw.line(SCREEN, col, coords[link], (xc, yc), width=width)
    pygame.draw.circle(SCREEN, col, (xc, yc), width/2)
    """
    pygame.draw.line(SCREEN, col, (xc, y), (xc,yc), width=width) # вверх
    pygame.draw.line(SCREEN, col, (xc, y + block_size), (xc,yc) , width=width) # низ

    pygame.draw.line(SCREEN, col, (x, yc), (x, yc), width=width) # лево
    pygame.draw.line(SCREEN, col, (x + block_size, yc), (x, yc) , width=width) # право
    """

def render_links_debug(x,y,cell_id):
    global block_size
    # c - center
    xc = x + int((block_size / 2))
    yc = y + int((block_size / 2))
    rad = int(block_size / 2)
    col = (255, 35, 35)
    width = 4

    cell_links = get_f_links(cell_id)

    print("links", cell_links)

    if cell_links[0]:
        pygame.draw.line(SCREEN, col, (xc, y), (xc, yc), width=width)
    if cell_links[1]:
        pygame.draw.line(SCREEN, col, (x+block_size, yc), (xc, yc), width=width)
    if cell_links[2]:
        pygame.draw.line(SCREEN, col, (xc, y+block_size), (xc, yc), width=width)
    if cell_links[3]:
        pygame.draw.line(SCREEN, col, (x, yc), (xc, yc), width=width)



def render_stem_a(x,y): # made by беззымянникк

    global block_size
    # c - center
    xc = x+ int((block_size/2))
    yc = y + int((block_size / 2))
    rad = int(block_size / 2)
    col = (64, 64, 64)
    width = 5

    #pygame.draw.circle(SCREEN, (0, 175, 0), (x, y), rad)
    pygame.draw.circle(SCREEN, (175, 175, 175), (xc, yc), rad)

    pygame.draw.line(SCREEN, col, (xc,y), (xc,y+block_size), width=width)
    pygame.draw.line(SCREEN, col, (x, yc), (x+block_size, yc), width=width)

    pygame.draw.circle(SCREEN, col, (xc, yc), rad, width)

def randomize_cols_a_bit(): # установить для каждой ячейки поля чуть чуть отличюшийся цвет
    global fieldSize
    diversion = 5
    for x in range(fieldSize):
        for y in range(fieldSize):
            chanLevel = random.randint(240-diversion,255-diversion) # channel level for each R, G and B
            chanDevLevel = random.randint(-diversion,diversion) #channel deviation level
            newCol = (chanLevel+chanDevLevel,chanLevel-chanDevLevel,chanLevel)
            fieldCols[x][y][0] = newCol

def get_axy_from_fxy(fx,fy): # даем колонку и строку, получаем абсолютные коорды левого верхнего края этой клетки
    global block_size
    ax = block_size * fx
    ay = block_size * fy
    return ax, ay


def render(arg): # Рендерит поле, и клетки на нём
    block_size, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK = arg
    global render_mode
    global debug_mode
    global first_cell_LEGACY # мне надо
    global fontDebugSmall
    global smallFontSize
    global debug_links


    match (render_mode): # отрисовка самого поля
        case 0:
            pass
        case 1: # anderfan
            draw_grid(arg)
            pause = [buttons()['pause']]
        case 2: # no-name
            draw_grid_безымянник_эдитион(arg) # рисуем базовое пустое поле




    match (render_cells): # отрисовка елементов самого поля (корни, ростки, листья и прочая моль)
        case 0:
            pass
        case 2:

            current_cell_id = first_cell_LEGACY
            current_cell_id = cells[0][2]

            while (current_cell_id != 0):
                fx, fy = cells[current_cell_id][0]["xy"]
                ax, ay = get_axy_from_fxy(fx,fy)

                #rect = pygame.Rect(ax, ay, block_size, block_size)
                #col = (0,255,0)
                #pygame.draw.rect(SCREEN, col, rect, 0)

                if cells[current_cell_id][0]["type"] == "stem":
                    render_stem_a(ax,ay)
                elif cells[current_cell_id][0]["type"] == "bnch":
                    render_branch_a(ax,ay, current_cell_id)
                else:
                    render_leaf_a(ax,ay)



                if debug_mode == 1: # рендер отладочных букававак
                    nudatipa = smallFontSize - 3

                    current_cell = cells[current_cell_id][0]
                    line1text = "Type:" + current_cell["type"]
                    line1 = fontDebugSmall.render(line1text, False, (255,255,255),(0,0,0))
                    SCREEN.blit(line1, (ax,ay))

                    line2text = "Enrg:" + str(current_cell["energy"])
                    line2 = fontDebugSmall.render(line2text, False, (255, 255, 255), (0, 0, 0))
                    SCREEN.blit(line2, (ax, ay+nudatipa*1))

                    line3text = "Ind:" + str(current_cell_id)
                    line3 = fontDebugSmall.render(line3text, False, (255, 255, 255), (0, 0, 0))
                    SCREEN.blit(line3, (ax, ay + nudatipa * 2))

                if debug_links == 1:
                    render_links_debug(ax,ay,current_cell_id)

                current_cell_id = next_cell(current_cell_id)

        case 1: #
            block_size, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK = arg

            for cell in cells:  # Тут идёт проверка на то словарь ли ли в cell[0] # чё это нахуй значит
                if isinstance(cell[0],
                              dict):  # и если нет, то читаю координаты и рисую # что это за исинстанце, это кто вам давал доступ к запретному плоду встроенных функций
                    if cell[0]["type"] != "none":
                        x, y = cell[0]["xy"]
                        print(cell[0]["xy"])
                        pygame.draw.circle(SCREEN, NEW_CELL, (x, y), 13)  # А ХУЛЕ РАДИУС ЭТО КОНСТАНТА
                else:  # а если да, то ругаюсь. Это сделано потому, что в add_cell последние из cells являются bool-ами
                    print(cell)
                    print(f"Invalid data type: {type(cell[0])}")

    pg_w.update(pygame.event.get())
    pygame.display.update()

def buttons():
    buttons_dict = {
        "pause": Button(
            # Mandatory Parameters
            SCREEN,  # Surface to place button on
            100,  # X-coordinate of top left corner
            WINDOW_HEIGHT - 70,  # Y-coordinate of top left corner
            100,  # Width
            70,  # Height

            # Optional Parameters
            text='pause',  # Text to display
            fontSize=20,  # Size of font
             margin=20,  # Minimum distance between text/image and edge of button
            inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
            hoverColour=(150, 0, 0),  # Colour of button when being hovered over
            pressedColour=(0, 200, 20),  # Colour of button when being clicked
            radius=0,  # Radius of border corners (leave empty for not curved)
            onClick=lambda: pause()  # Function to call when clicked on
        )
    }
    return buttons_dict


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

            col = fieldCols[fx][fy][0] # цвет достаем из мега массива который я нашаманиваю где то выше

            pygame.draw.rect(SCREEN, col, rect, 0)




#### end render
def pause():
    global running
    running = not (running)


def handle_input():
    for event in pygame.event.get():  # Выход при нажатии на крестик
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

fieldSize = 12 # высота\широта игр.поля
cells_len = fieldSize ** 2 #  длинна массива с клетками и других связаных (генома, мертвых)

field = [[[0,0] for j in range(fieldSize)] for i in range(fieldSize)] # создаем матрицу с двух-мерным массивом, в пизду нумпи
fieldCols = [[[(255,0,0),(255,255,255)] for j in range(fieldSize)] for i in range(fieldSize)] # это отдельный массив с цветами для клеток, почему так, спросите беззымянника


# Проверяем \\ КОГО, О ЧЕМ ТЫ


cells = [[gen_empty_cell(),0,0] for _ in range(cells_len)]  # linked list, with all of the cells // связный список со всеми клетками
first_cell_LEGACY = 1 # УБЕЙСЯ, какойто долбоеб (беззымянник) забыл как у нас работает линкед лист и положил это сюда, оно тут не долэно быть
# для получения индекса первой клетки надо спрашивать cells[0][2] - фантомную клеть.
dead_cells_coords = list(range(cells_len)) ## ааа, ээээ, ну это помоему очередб с пустыми индексами в cells




яша = 42

dead_current = 1# начало очереди
dead_last = -1# конец очереди
dead_last = cells_len - 1
# это были указатели начала и конца очереди
print(dead_cells_coords)
print(dead_current)
print(dead_last)
#print(cells)

genomes = [[0 for __ in range(12)] for _ in range(cells_len)] # array with all of the active genomes (len?)


##### render varibables
block_size = 60 # размеры квадратиков поля
render_mode = 1 # 1 - подсмешок база, 2 - беззымянник # 0 - залагать и умереть)
render_cells = 2 # 1 - сломанные приколы от подсмешка, 2 - рабочее чё-то от беззымянника, 0 - плакать
debug_mode = 1 # 0 - no, 1 - спрашивай беззымянника
debug_links = 0
running = True

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

radius = float(block_size / 30)  # УЛЬТИМАТИВНЫЙ РАДИУС???????? ЧТО ЭТО, ПОЧЕМУ /30


smallFontSize = 17 # УБЕЙСЯ, хуйня, я уже заспыпл когда писал, чёт мутное и нерабочее
fontDebugSmall = pygame.font.Font(None, smallFontSize)  # малый шрифт для дебага на клетках


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
    create_Игорь_debug()
    grow_cell(2, 1, "bnch", 0)
    #create_cells_debug(3) # шутка генерит клетки, работает и ладно, слава целостности cells
    #randomize_cells_coords(fieldSize) # рандомазит коорды стартовых клеток, максмимальная залупа, использовать только и тут и сейчас, оно тупое и еле дышит

    #simplified_cells_print()
    #add_cell_lnkl(3) # ахах ты лох, переделуй) нихуя не працює)))))
    #print(cells)
    #simplified_cells_print()
    # print(genome)
    pass


def update():

    global first_cell_LEGACY
    traverse = True
    current_cell_id = first_cell_LEGACY #first_cell_LEGACY # я ебу? фирст целл = 1, хуле? # Да завали, работает же # Сьебал, уже не ебу сколько и где оно менятеся, но всё ещё работает
    current_cell_id = cells[0][2]
    current_cell = cells[current_cell_id][0]

    while(current_cell_id != 0):

        upd_cell(current_cell_id)
        current_cell_id = next_cell(current_cell_id)



def loop():
    n = 0

    while (n < 5 or True):
        handle_input()
        if running == True:
            update()
        render(arg)
        n += 1

setup()
loop()



# credits: ТриГнома (ПодСмешок, Беззыммянникк, Кирка) )
# идея: foo52ru техношаман