import time
import warnings
from threading import Thread

from scrabblelib import *


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
    def __init__(self, name, t, callback=lambda *args: None, rid=None, dif=None, ip=None):
        super().__init__(name, t, rid, dif, ip)
        self.score = 0
        self.letters = []
        self.isTurn = False
        self.isComplete = False
        # TODO функция должна зависеть от типа игрока
        # TODO возможно следует создать еще несколько дочерних классов для каждого типа пользователя
        self.callback = callback
        self.timeout = 0
        self.input = None
        self.result = None

    def action(self, game):
        """Посылает игроку команду на начало действий и ожидает прекращения"""
        self.isTurn = True
        self.isComplete = False
        self.timeout = GameConfig.turnTime
        self.input = game
        self.callback()
        while not self.isComplete:
            time.sleep(1)
            self.timeout -= 1
            if self.timeout <= 0:
                self.isComplete = True
        self.isTurn = False
        return self.result


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
        self.players = players
        self.playStatus = True
        self.alphabet = ""
        for key, value in GameConfig.letters.items():
            self.alphabet += key * value["count"]
        self.thread = Thread(target=self._game_loop)
        self.thread.start()

    def _game_loop(self):
        while self.playStatus:
            for i in self.players:
                result = i.action(self)
                if result:
                    # TODO Какая то обработка резульатата и измененние значений
                    pass


# send_broadcast({'action': 'connectGame', 'rid': 'qwмty', 'name': 'BOSS'}, 8383)


if __name__ == '__main__':
    Matr = Matrix()
    Matr.newkoord = [[None, None], [2, 2], [2, 1], [4, 1]]
    Matr.newletters = ['Д', 'Д', 'У', 'Е']
    Matr.serch()
    print('Hello, world!!!')
    print(Matr.outx)
    print(Matr.outy)
    x = GameServer([GamePlayer("ADMIN", "local"), GamePlayer("BOT", "bot")])
