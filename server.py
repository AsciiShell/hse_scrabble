import time
import warnings
from threading import Thread

from scrabblelib import *



class Letter:
    def __init__(self, letter):
        self.letter = letter
        self.price = GameConfig.letters[letter]["price"]


class Point(Letter):
    """Класс ячейки поля"""
    info = [{'color': 'white', 'multi': 'letter', 'value': 1},
            {'color': 'green', 'multi': 'letter', 'value': 2},
            {'color': 'blue', 'multi': 'word', 'value': 2},
            {'color': 'yellow', 'multi': 'letter', 'value': 3},
            {'color': 'red', 'multi': 'word', 'value': 3}, ]

    def get_info(self):
        """Возвращает информацию о текущей точке"""
        return self.info[self.t]

    def __init__(self, x, y, letter, t=None):
        super().__init__(letter)
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
        self.tempmap = [["" for i in range(15)] for j in range(15)]
        self.matrvalid = [[ 0 for i in range(15)] for j in range(15)]

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
        """ищет слова в матрице"""

        # n = 0
        # for i in self.temp:
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
        if self.ValidationKoord():
            self.map = self.tempmap
            for i in range(len(self.map)):
                for j in range(len(self.map[i])):
                    if (self.map[i][j] != ''):
                        slx = self.prov(j, i, 1)
                        sly = self.prov(j, i, 2)
                        if (slx[1] == 1):
                            self.outx.append(slx[0])
                        if (sly[1] == 1):
                            self.outy.append(sly[0])
                        """if (slx[0] != ''):
                            print(slx[0])
                        if (sly[0] != ''):
                            print(sly[0])"""
            return True
        else:
            return False

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
        #poisk sverhy
        if self.matrvalid[koord[0]][koord[1]] == 0:
            self.count += 1
            self.matrvalid[koord[0]][koord[1]] += 1
            if koord[0] != 0:
                if self.tempmap[koord[0] - 1][koord[1]] != "":
                    #self.matrvalid[koord[0]][koord[1]] = 1

                    self.ValidationCheck([koord[0] - 1,koord[1]])
            #poisk sleva
            if koord[1] != 0:
                if self.tempmap[koord[0]][koord[1] - 1] != "":
                    #self.matrvalid[koord[0]][koord[1]] = 1
                    #self.count += 1
                    self.ValidationCheck([koord[0] ,koord[1] - 1])
            #poisk vnizy
            if koord[0] != 14:
                if self.tempmap[koord[0] + 1][koord[1]] != "":
                    #self.matrvalid[koord[0]][koord[1]] = 1
                    #self.count += 1
                    self.ValidationCheck([koord[0] + 1,koord[1]])
            #poisk sprava
            if koord[1] != 14:
                if self.tempmap[koord[0]][koord[1] + 1] != "":
                    #self.matrvalid[koord[0]][koord[1]] = 1
                    #self.count += 1
                    self.ValidationCheck([koord[0] ,koord[1] + 1])

    def ValidationKoord(self):
        self.count = 0
        self.FirstFish = [7,7]
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
        self.matrvalid = [[ 0 for i in range(15)] for j in range(15)]


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


def send_broadcast(data, port=8384, ip='255.255.255.255'):
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if ip == '255.255.255.255':
        cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    cs.sendto(_encode(data), (ip, port))


def _encode(b):
    return json.dumps(b).encode("utf-8")


def _convert_type(b):
    """Преобразует байтовую строку в массив"""
    return json.loads(b.decode("utf-8"))


def rand(length=4):
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join([alphabet[random.randrange(len(alphabet))] for _ in range(length)])


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


class GamePlayer(Player):
    def __init__(self, name, game, rid=None, dif=None, ip=None):
        self.score = 0
        self.game = game
        self.letters = []
        self.isTurn = False
        self.isComplete = False
        self.timeout = 0
        self.input = None
        self.result = None
        super().__init__(name, None, rid, dif, ip)

    def turn_end(self):
        """Срабатывает при завершении хода любого игрока. Перерисовка"""
        pass

    def my_turn(self):
        """Предупреждает игрока о начале его хода. Активирует игровой интерфейс"""
        pass

    def action(self):
        """Посылает игроку команду на начало действий и ожидает прекращения"""
        self.isTurn = True
        self.isComplete = False
        self.timeout = GameConfig.turnTime
        self.my_turn()
        while not self.isComplete:
            time.sleep(1)
            self.timeout -= 1
            if self.timeout <= 0:
                self.isComplete = True
        self.isTurn = False
        return self.result

    def check_turn(self, *args):
        """Проверяет правильность ввода новых букв"""
        # TODO andrsolo21 вызов функций класса матрицы
        # TODO на вход массив буков с координатами
        self.game.matrix.check_temp()
        return Message(True)  # + слова/очки и проч

    def accept_turn(self, *args):
        """Проверяет правильность ввода новых букв и завершает ход"""
        # TODO andrsolo21
        # TODO на вход массив буков с координатами/сброс букв
        self.check_turn(args)
        # TODO спец переменная для возврата результата в главнуб функцию
        self.result = "something"
        # Останавливает ход
        self.isComplete = True
        return Message(True)  # + the same


class PlayerLocal(GamePlayer):
    def my_turn(self):
        # TODO andrsolo21 перерисовываем интерфес
        # мб эту функцию переопределить в Form.py?
        pass

    def turn_end(self):
        # TODO andrsolo21 перерисовываем интерфес
        # мб эту функцию переопределить в Form.py?
        pass


class PlayerBot(GamePlayer):
    def __init__(self, name, game):
        self.botEnable = True
        self.thread = Thread(target=self._daemon)
        super().__init__(name, game)
        self.thread.start()

    def __del__(self):
        self.botEnable = False
        self.thread.join(1)

    @staticmethod
    def _is_replaceable(a, b):
        return b == '' or a == b

    def cpu(self):
        """Вычисляет информацию для хода"""
        letters = ""
        for i in self.game.matrix.map:
            for j in i:
                if letters.count(j) == 0:
                    letters += j
        for i in self.letters:
            if letters.count(i) == 0:
                letters += i
        words = self.game.dict.prepare(letters)
        pass

    def _daemon(self):
        """Демон бота"""
        while self.botEnable:
            if self.isTurn:
                self.cpu()
            time.sleep(1)


class GameServerPrepare:
    """Основной класс игры"""

    def create_game_async(self):
        """Асинхронный метод для ожидания информации"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", 8383))
        server_id = rand(8)
        while self.gamePrepare:
            data, address = sock.recvfrom(1024)
            data = convert_type(data)
            if data["action"] == "getStatus":
                send_broadcast({"game": [value.__dict__ for key, value in self.players.items()], "queue": self.queue,
                                "id": server_id})
            elif data["action"] == "connectGame":
                for i in self.queue:
                    if i['rid'] == data['rid']:
                        break
                else:
                    self.queue.append({"ip": address, "name": data["name"], "rid": data["rid"], "add": False})
            elif data["action"] == 'continue':
                pass
            else:
                warnings.warn("Неизвестное действие " + data["action"])
            print(data)
        sock.close()

    def create_game(self, player_name):
        """Создает игру с указанными параметрами"""
        self.gamePrepare = True
        self.players = {}
        self.queue = []
        me = Player(player_name, "local")
        self.players[me.id] = me
        self.gamePrepareThread = Thread(target=self.create_game_async)
        self.gamePrepareThread.start()

    def get_status(self):
        if self.gamePrepare:
            return {"game": self.players, "queue": self.queue}
        else:
            return False

    def add_player(self, t, rid=None):
        if not self.gamePrepare:
            return Message(False, 'Игра не находится в процессе подготовки')
        if len(self.players) >= 4:
            return Message(False, 'Достаточно игроков')
        if t == 'bot':
            p = Player('BOT_' + str(random.randint(1000, 9999)), 'bot')
            self.players[p.id] = p
        elif t == 'net':
            for i in self.queue:
                if i['rid'] == rid:
                    for key, value in self.players.items():
                        if rid == value.rid:
                            return Message(False, "Игрок {} не найден ".format(str(rid)))
                    p = Player(i['name'], 'net', rid, ip=i['ip'])
                    self.players[p.id] = p
                    i["add"] = True
                    break
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
        self.players = []
        for player in players:
            if player.type == "local":
                self.players.append(PlayerLocal(player.name, self))
            elif player.type == "bot":
                self.players.append(PlayerBot(player.name, self))
            else:
                warnings.warn("Тип не найден" + player.type)
        self.playStatus = True
        self.alphabet = ""
        self.matrix = Matrix()
        self.dict = GameDictionary()
        for key, value in GameConfig.letters.items():
            self.alphabet += key * value["count"]
        self.thread = Thread(target=self._game_loop)
        self.thread.start()

    def _give_letter(self, player):
        """Выдает игроку недостающие фишки"""
        while len(player.letters) < GameConfig.startCount and len(self.alphabet) > 0:
            i = self.alphabet[random.randrange(len(self.alphabet))]
            player.letters.append(i)
            self.alphabet = self.alphabet.replace(i, "", 1)

    def _game_loop(self):
        while self.playStatus:
            for player in self.players:
                self._give_letter(player)
                result = player.action()
                if result:
                    # TODO Какая то обработка резульатата и измененние значений
                    pass
                for i in self.players:
                    i.turn_end()


# send_broadcast({'action': 'connectGame', 'rid': 'qwмty', 'name': 'BOSS'}, 8383)


if __name__ == '__main__':
    Matr = Matrix()
    """Matr.newkoord = [[None, None], [2, 2], [2, 1], [4, 1]]
    Matr.newletters = ['Д', 'Д', 'У', 'Е']
    Matr.serch()
    print('Hello, world!!!')
    print(Matr.outx)
    print(Matr.outy)
    x = GameServer([Player("ADMIN", "local")])
