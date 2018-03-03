import json
import random
import socket
import warnings


def send_broadcast(data, port=8384, ip='255.255.255.255'):
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if ip == '255.255.255.255':
        cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    cs.sendto(encode(data), (ip, port))


def encode(b):
    return json.dumps(b).encode("utf-8")


def convert_type(b):
    """Преобразует байтовую строку в массив"""
    return json.loads(b.decode("utf-8"))


def rand(length=4):
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join([alphabet[random.randrange(len(alphabet))] for _ in range(length)])


class GameConfig:
    """Конфигурация игры"""
    map = [[4, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 4],
           [0, 2, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 2, 0],
           [0, 0, 2, 0, 0, 0, 1, 0, 1, 0, 0, 0, 2, 0, 0],
           [1, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 1],
           [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
           [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
           [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
           [4, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 4],
           [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
           [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
           [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
           [1, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 1],
           [0, 0, 2, 0, 0, 0, 1, 0, 1, 0, 0, 0, 2, 0, 0],
           [0, 2, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 2, 0],
           [4, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 4]]
    let = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х',
           'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', '*']
    letters = {'А': {'count': 10, 'price': 1},
               'Б': {'count': 3, 'price': 3},
               'В': {'count': 5, 'price': 2},
               'Г': {'count': 3, 'price': 3},
               'Д': {'count': 5, 'price': 2},
               'Е': {'count': 9, 'price': 1},
               'Ж': {'count': 2, 'price': 5},
               'З': {'count': 2, 'price': 5},
               'И': {'count': 8, 'price': 1},
               'Й': {'count': 4, 'price': 2},
               'К': {'count': 6, 'price': 2},
               'Л': {'count': 4, 'price': 2},
               'М': {'count': 5, 'price': 2},
               'Н': {'count': 8, 'price': 1},
               'О': {'count': 10, 'price': 1},
               'П': {'count': 6, 'price': 2},
               'Р': {'count': 6, 'price': 2},
               'С': {'count': 6, 'price': 2},
               'Т': {'count': 5, 'price': 2},
               'У': {'count': 3, 'price': 3},
               'Ф': {'count': 1, 'price': 10},
               'Х': {'count': 2, 'price': 5},
               'Ц': {'count': 1, 'price': 10},
               'Ч': {'count': 2, 'price': 5},
               'Ш': {'count': 1, 'price': 10},
               'Щ': {'count': 1, 'price': 10},
               'Ъ': {'count': 1, 'price': 10},
               'Ы': {'count': 2, 'price': 5},
               'Ь': {'count': 2, 'price': 5},
               'Э': {'count': 1, 'price': 10},
               'Ю': {'count': 1, 'price': 10},
               'Я': {'count': 3, 'price': 3}, }
    # '*': {'count': 3, 'price': None}}
    """Начальное число фишек"""
    startCount = 7
    """Бонус за полное использование фишек"""
    fullBonus = 15
    """Количество пропусков для завершения игры"""
    skipEnd = 2
    """Время хода"""
    turnTime = 60


class Point:
    """Класс ячейки поля"""
    info = [{'color': 'white', 'multi': 'letter', 'value': 1},
            {'color': 'green', 'multi': 'letter', 'value': 2},
            {'color': 'blue', 'multi': 'word', 'value': 2},
            {'color': 'yellow', 'multi': 'letter', 'value': 3},
            {'color': 'red', 'multi': 'word', 'value': 3}, ]

    def get_info(self):
        """Возвращает информацию о текущей точке"""
        return self.info[self.t]

    def __init__(self, x, y, letter=None, t=None):
        """Создает точку
        x, y - координаты
        t - числовой тип
        letter - буква
        """
        self.x = x
        self.y = y
        self.letter = letter
        if t is None:
            self.t = GameConfig.map[x][y]
        else:
            self.t = t


class Message:
    """Класс возвращаемых сообщений"""

    def __init__(self, res=False, msg=""):
        self.res = res
        self.msg = msg


class MatrixResult:
    """Результат проверки матрицы"""

    def __init__(self, stat, score=0, words=None, errmsg=""):
        self.result = stat
        if stat:
            if words is None:
                warnings.warn("Слова не указаны")
            self.score = score
            self.words = words
        else:
            self.msg = errmsg
            self.wordsError = words


class Matrix:
    """Класс игрового поля"""

    # TODO andrsolo21 создай/укажи 2 метода и назови их красиво
    # первый принимает массив новых букв
    # возвращает структуру состоящую из
    #     a)успеха,
    #     b)суммы очков,
    #     c)найденные слова,
    #     или
    #     d)список ошибок (клетка занята), слово не существует в словаре
    #
    #     ошибки больше нужны для человека
    # второй принимает все то же самое,
    # вызывает первую функцию а затем, в случае успеха, фиксирует изменения
    # По идее все методы есть, их надо красиво скомпоновать
    # те сделать newkoord и newletters локальными, убрать обращение к ним извне и передавать как параметр
    #
    # P.S.
    # TODO думаю словарь хранить тоже в матрице, так как там он и обрабатывается. Как думаешь?
    # TODO P.P.S в этом файле ошибки только в этом классе
    def add_temporary(self, arr):
        """Добавляет несколько элементов во временную матрицу"""
        if type(arr) is list:
            self.temp.extend(arr)
        elif type(arr) is int:
            self.temp.append(arr)
        else:
            raise Exception('Wrong type' + str(arr))

    def accept_temp(self):
        """Принимает временные изменения"""
        for i in self.temp:
            self.map[i.x][i.y] = i
        self.reject_temp()

    def reject_temp(self):
        """Отклоняет временные изменения"""
        self.newkoord = []
        self.newletters = []
        self.tempmap = [["" for i in range(15)] for j in range(15)]
        self.matrvalid = [[0 for i in range(15)] for j in range(15)]

    def check_temp(self):
        """Возвращает True, если временная матрица правильная"""
        # TODO andrsolo21
        return True

    def prov(self, x, y, napr):
        """проверяет, начие слова в этой ячейке (начало слова)"""
        flag = 0
        if napr == 2 and y != 14:
            if y != 0:
                if (self.map[y - 1][x] == '') and (self.map[y + 1][x] != ''):
                    flag = 1
            else:
                if self.map[y + 1][x] != '':
                    flag = 1
        if napr == 1 and x != 14:
            if x != 0:
                if self.map[y][x - 1] == '' and self.map[y][x + 1] != '':
                    flag = 1
            else:
                if self.map[y][x + 1] != '':
                    flag = 1
        if flag == 1:
            return self.schit(x, y, napr)
        else:
            return ['', 0]

    def schit(self, x, y, napr):
        """считывает слово"""
        s = ''
        newword = 0
        if napr == 2:
            a = 1
            while a != 0:
                koord = [x, y]
                if koord in self.newkoord:
                    newword = 1
                s = s + self.map[y][x]
                if y == 14:
                    a = 0
                else:
                    if self.map[y + 1][x] == '':
                        a = 0
                y = y + 1
        else:
            a = 1
            while a != 0:
                koord = [x, y]
                if koord in self.newkoord:
                    newword = 1
                s = s + self.map[y][x]
                if x == 14:
                    a = 0
                else:
                    if self.map[y][x + 1] == '':
                        a = 0
                x = x + 1
        return [s, newword]

    def pasteletters(self):
        """вставляет буквы в матрицу"""
        for i in range(len(self.newkoord)):
            self.tempmap[self.newkoord[i][1]][self.newkoord[i][0]] = self.newletters[i]

    def serch(self):
        """ищет слова в матрице
        основная функция"""

        # n = 0
        # for i in self.temp:
        #    newletters.append([[i.x], [i.y]])
        #   self.newkoord.append(i.letter)
        # self.newkoord = [[4,6],[4,8],[4,9],[4,10]]
        # self.newletters = ['б','т','о','н']
        # движение по оси x = 1
        # движение по оси y = 2
        outx = []
        outy = []
        self.chekKoord()
        self.pasteletters()
        result = MatrixResult()
        if self.ValidationKoord():
            self.map = self.tempmap
            for i in range(len(self.map)):
                for j in range(len(self.map[i])):
                    if (self.map[i][j] != ''):
                        slx = self.prov(j, i, 1)
                        sly = self.prov(j, i, 2)
                        if (slx[1] == 1):
                            outx.append(slx[0])
                        if (sly[1] == 1):
                            outy.append(sly[0])
                        """if (slx[0] != ''):
                            print(slx[0])
                        if (sly[0] != ''):
                            print(sly[0])"""
            return MatrixResult(True, 0, outx + outy)
        else:
            return MatrixResult(False, 0, outx + outy, '')

    def get(self, y, x):
        """Возвращает точку по адресу"""
        return self.map[y][x]

    def chekKoord(self):
        a = []
        b = []
        for i in range(len(self.newkoord)):
            if self.newkoord[i][1] != None and self.newkoord[i][0] != None:
                a.append(self.newkoord[i])
                b.append(self.newletters[i])
        self.newkoord = a
        self.newletters = b
        print('проверили новые данные')

    def ValidationCheck(self, koord):
        # poisk sverhy
        if self.matrvalid[koord[0]][koord[1]] == 0:
            self.count += 1
            self.matrvalid[koord[0]][koord[1]] += 1
            if koord[0] != 0:
                if self.tempmap[koord[0] - 1][koord[1]] != "":
                    # self.matrvalid[koord[0]][koord[1]] = 1

                    self.ValidationCheck([koord[0] - 1, koord[1]])
            # poisk sleva
            if koord[1] != 0:
                if self.tempmap[koord[0]][koord[1] - 1] != "":
                    # self.matrvalid[koord[0]][koord[1]] = 1
                    # self.count += 1
                    self.ValidationCheck([koord[0], koord[1] - 1])
            # poisk vnizy
            if koord[0] != 14:
                if self.tempmap[koord[0] + 1][koord[1]] != "":
                    # self.matrvalid[koord[0]][koord[1]] = 1
                    # self.count += 1
                    self.ValidationCheck([koord[0] + 1, koord[1]])
            # poisk sprava
            if koord[1] != 14:
                if self.tempmap[koord[0]][koord[1] + 1] != "":
                    # self.matrvalid[koord[0]][koord[1]] = 1
                    # self.count += 1
                    self.ValidationCheck([koord[0], koord[1] + 1])

    def ValidationKoord(self):
        self.count = 0
        self.FirstFish = [7, 7]
        if self.tempmap[7][7] != '':
            self.ValidationCheck(self.FirstFish)
            print('нашел ' + str(self.count) + ' букв')
            for i in range(15):
                for j in range(15):
                    if self.tempmap[i][j] != '':
                        self.count -= 1
            print('проверил, осталось: ' + str(self.count) + ' букв')
            if self.count == 0:
                return True
            else:
                return False
        else:
            return False

    def __init__(self):
        """Создает новую игровую карту"""
        self.map = [["" for i in range(15)] for j in range(15)]
        self.tempmap = [["" for i in range(15)] for j in range(15)]
        self.newkoord = []
        self.newletters = []
        self.matrvalid = [[0 for i in range(15)] for j in range(15)]


class GameDictionary:
    """Словарь слов игры"""
    filename = "dictionary"

    def append(self, item):
        """Добавляет новое слово в словарь"""
        self.dict.append(item)
        with open(self.filename, "r", encoding="utf-8") as f:
            f.write(item + "\n")

    def prepare(self, alphabet):
        """Подготавливает словарь к допустимым буквам

        alphabet - строка допустимых символов"""
        alphabet = alphabet.upper()
        if len(alphabet) >= 32:
            return self.dict

        temp_dict = []
        for i in self.dict:
            for j in i:
                if alphabet.count(j) == 0:
                    break
            else:
                temp_dict.append(i)
        return temp_dict

    def __init__(self):
        """Инициализирует словарь начальным списком слов"""
        with open(self.filename, "r", encoding="utf-8") as f:
            self.dict = f.read().upper().split("\n")
