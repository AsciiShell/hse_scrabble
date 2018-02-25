import json
import random
import socket
import warnings
from threading import Thread


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
    let = ['А','Б','В','Г','Д','Е','Ж','З','И','Й','К','Л','М','Н', 'О','П','Р','С', 'Т', 'У','Ф','Х','Ц','Ч','Ш','Щ','Ъ','Ы','Ь','Э','Ю','Я','*']
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
               'Я': {'count': 3, 'price': 3},
               '*': {'count': 3, 'price': None}}
    """Начальное число фишек"""
    startCount = 7
    """Бонус за полное использование фишек"""
    fullBonus = 15
    """Количество пропусков для завершения игры"""
    skipEnd = 2


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
        if t is None:
            self.t = GameConfig.map[x][y]
        else:
            self.t = t
        self.letter = letter


class Matrix:
    """Класс игрового поля"""

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

    def check_temp(self):
        """Возвращает True, если временная матрица правильная"""
        # TODO andrsolo21
        return True

    def prov(self,  x, y, napr):
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
            return self.schit( x, y, napr)
        else:
            return ['', 0]

    def schit(self,  x, y, napr):
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
            self.map[self.newkoord[i][1]][self.newkoord[i][0]] = self.newletters[i]


    def serch(self):
        """ищет слова в матрице"""

        #n = 0
        #for i in self.temp:
        #    newletters.append([[i.x], [i.y]])
        #   self.newkoord.append(i.letter)
        # self.newkoord = [[4,6],[4,8],[4,9],[4,10]]
        # self.newletters = ['б','т','о','н']
        # движение по оси x = 1
        # движение по оси y = 2
        self.outx = []
        self.outy = []
        self.chekKoord()
        self.pasteletters()
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if (self.map[i][j] != ''):
                    slx = self.prov( j, i, 1)
                    sly = self.prov( j, i, 2 )
                    if (slx[1] == 1):
                        self.outx.append(slx[0])
                    if (sly[1] == 1):
                        self.outy.append(sly[0])
                    """if (slx[0] != ''):
                        print(slx[0])
                    if (sly[0] != ''):
                        print(sly[0])"""

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


    def __init__(self):
        """Создает новую игровую карту"""
        self.map = [["" for i in range(15)] for j in range(15)]
        self.newkoord = []
        self.newletters = []


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
        alphabet = alphabet.lower()
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
            self.dict = f.read().lower().split("\n")


def send_broadcast(data, port=8384):
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    cs.sendto(_encode(data), ('255.255.255.255', port))


def _encode(b):
    return json.dumps(b).encode("utf-8")


def _convert_type(b):
    """Преобразует байтовую строку в массив"""
    return json.loads(b.decode("utf-8"))


class Player:
    """Абстрактный класс игрока"""
    lastID = 0

    def __init__(self, name, t, rid=None, dif=None, ip=None):
        """Создает нового игрока с указанным именем"""
        self.name = name
        self.type = t
        self.id = Player.lastID
        Player.lastID += 1
        self.rid = rid
        self.dif = dif
        self.ip = ip


class Message:
    """Класс возвращаемых сообщений"""

    def __init__(self, res=False, msg=""):
        self.res = res
        self.msg = msg


class GameServerPrepare:
    """Основной класс игры"""

    def create_game_async(self):
        """Асинхронный метод для ожидания информации"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", 8383))
        while self.gamePrepare:
            data, address = sock.recvfrom(1024)
            data = _convert_type(data)
            if data["action"] == "getStatus":
                send_broadcast({"game": self.players, "queue": self.queue})
            elif data["action"] == "connectGame":
                for i in self.queue:
                    if i['rid'] == data['rid']:
                        break
                else:
                    self.queue.append({"ip": address, "name": data["name"], "rid": data["rid"]})
            elif data["action"] == 'continue':
                pass
            else:
                warnings.warn("Неизвестное действие " + data["action"])
            print(data)

    def create_game(self, player_name):
        """Создает игру с указанными параметрами"""
        self.gamePrepare = True
        self.players = {}
        self.queue = []
        me = Player(player_name, "local")
        self.players[me.id] = me
        self.gamePrepareThread = Thread(target=self.create_game_async)

    def get_status(self):
        if self.gamePrepare:
            return {"game": self.players, "queue": self.queue}
        else:
            return False

    def add_player(self, t, rid=None):
        if self.gamePrepare:
            return Message(False, 'Игра не находится в процессе подготовки')
        if len(self.players) >= 4:
            return Message(False, 'Достаточно игроков')
        if t == 'bot':
            p = Player('BOT_' + str(random.randint(1000, 9999)), 'bot')
            self.players[p.id] = p
        elif t == 'net':
            for i in self.queue:
                if i['rid'] == rid:
                    p = Player(i['name'], 'net', rid, ip=i['ip'])
                    self.players[p.id] = p
            else:
                return Message(False, "Игрок {} не найден ".format(str(rid)))
        else:
            return Message(False, 'Неизвестный тип ' + t)
        return Message(True)

    def delete_player(self, rid):
        if self.gamePrepare:
            return Message(False, 'Игра не находится в процессе подготовки')
        for i in self.players:
            if i.rid == rid:
                del self.players[i]
                break
        else:
            for i in self.queue:
                if i['rid'] == rid:
                    self.queue.remove(i)
                    break
            else:
                return Message(False, "Игрок {} не найден ".format(str(rid)))
        return Message(True)

    def start_game(self):
        self.gamePrepare = False
        send_broadcast({'action': 'continue'}, 8383)
        self.gamePrepareThread.join(1)

    def __init__(self):
        self.players = {}
        self.queue = []
        self.gamePrepare = False
        self.gamePrepareThread = Thread()
        self.dict = GameDictionary()


class GameServer:
    def __init__(self, players):
        self.players = players


if __name__ == '__main__':
    Matr = Matrix()
    Matr.newkoord = [[None, None], [2, 2], [2, 1], [4, 1]]
    Matr.newletters = ['Д', 'Д', 'У', 'Е']
    Matr.serch()
    print('Hello, world!!!')
    print(Matr.outx)
    print(Matr.outy)