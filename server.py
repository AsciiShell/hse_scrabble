import time
from threading import Thread

from scrabblelib import *


class Player:
    """Абстрактный класс игрока"""
    lastID = 0

    def __init__(self, name, t, rid=None, diff=None, ip=None):
        """Создает нового игрока с указанным именем"""
        self.name = name
        self.type = t
        self.id = Player.lastID
        Player.lastID += 1
        self.rid = rid
        self.diff = diff
        self.ip = ip


class TurnStruct:
    def __init__(self, changed=False, letters=None, score=0, words=None):
        if letters is None:
            letters = []
        if words is None:
            words = []
        self.changed = changed
        self.letters = letters
        self.score = score
        self.words = words


class GamePlayer(Player):
    def __init__(self, name, game, rid=None, diff=None, ip=None):
        self.score = 0
        self.game = game
        self.letters = []
        self.isTurn = False
        self.timeout = 0
        self.input = None
        self.result = None
        super().__init__(name, None, rid, diff, ip)

    def turn_end(self):
        """Срабатывает при завершении хода любого игрока. Перерисовка"""
        pass

    def my_turn(self):
        """Предупреждает игрока о начале его хода. Активирует игровой интерфейс"""
        pass

    def action(self):
        """Посылает игроку команду на начало действий и ожидает прекращения"""
        self.timeout = GameConfig.turnTime
        self.result = None
        self.my_turn()
        self.isTurn = True
        while self.isTurn:
            time.sleep(1)
            self.timeout -= 1
            if self.timeout <= 0:
                self.isTurn = False
        if self.result is None:
            self.accept_turn()
        return self.result

    def check_turn(self, turn):
        """Проверяет правильность ввода новых букв"""
        self.game.matrix.reject_temp()
        for _ in turn:
            self.game.matrix.newkoord.append([_.y, _.x])
            self.game.matrix.newletters.append(_.letter)
        return self.game.matrix.serch()

    def accept_turn(self, turn=TurnStruct()):
        """Проверяет правильность ввода новых букв и завершает ход"""
        if self.isTurn:
            if turn.changed:
                res = self.check_turn(turn.letters)
                if res.result:
                    for i in turn.letters:
                        self.game.matrix.Mainmap[i.x][i.y] = i.letter
                        if i.letter in self.letters:
                            self.letters.remove(i.letter)
                        else:
                            self.letters.remove('*')
                    self.score += res.score
                    self.result = turn
                    self.result.words = res.words.copy()
                    # Останавливает ход
                    self.isTurn = False
                    return Message(True, str(res.score))
                else:
                    return Message(False, res.msg)
            else:
                for i in turn.letters:
                    self.letters.remove(i)
                self.result = turn
                self.isTurn = False

                return Message(True, "Пропуск")
        else:
            self.result = TurnStruct(False, [])
            return Message(True, "Время вышло")


class PlayerLocal(GamePlayer):
    def __init__(self, name, game):
        self.alertMe = False
        self.alertEnd = False
        super().__init__(name, game)

    def my_turn(self):
        self.alertMe = True

    def turn_end(self):
        self.alertEnd = True


class PlayerBot(GamePlayer):
    def __init__(self, name, game, diff=None):
        self.botEnable = True
        self.thread = Thread(target=self._daemon)
        super().__init__(name, game)
        if diff is None:
            self.diff = 0.5
        else:
            self.diff = diff
        self.thread.start()

    def __del__(self):
        print("Deleting BOT " + self.name)
        self.botEnable = False
        self.thread.join(1)

    def _empty(self, x, y):
        if not 0 <= x < len(self.game.matrix.Mainmap):
            return True
        if not 0 <= y < len(self.game.matrix.Mainmap[0]):
            return True
        if self.game.matrix.Mainmap[x][y] == '':
            return True
        return False

    def _available(self, word, ind):
        res = []
        for line in self.game.matrix.Mainmap:
            for point in line:
                if point != '':
                    break
            else:
                continue
            break
        else:
            turn = []
            if random.randint(0, 2) == 0:
                for let in range(len(word)):
                    if 0 <= 7 - ind + let < len(self.game.matrix.Mainmap):
                        turn.append(Point(7 - ind + let, 7, word[let]))
                    else:
                        break
            else:
                for let in range(len(word)):
                    if 0 <= 7 - ind + let < len(self.game.matrix.Mainmap):
                        turn.append(Point(7, 7 - ind + let, word[let]))
                    else:
                        break
            check = self.check_turn(turn)
            if check.result and check.score != 0:
                return [TurnStruct(True, turn, check.score)]
            else:
                return []

        for i in range(len(self.game.matrix.Mainmap)):
            for j in range(len(self.game.matrix.Mainmap[0])):
                if self.game.matrix.Mainmap[i][j] == word[ind]:
                    # Проверка по горизонтали
                    let = self.letters.copy()
                    turn = []
                    if self._empty(i, j - ind - 1) and self._empty(i, j - ind + len(word)):
                        for x in range(len(word)):
                            if not 0 <= j - ind + x < len(self.game.matrix.Mainmap):
                                break
                            if self.game.matrix.Mainmap[i][j - ind + x] != word[x]:
                                if self.game.matrix.Mainmap[i][j - ind + x] != '':
                                    break
                                elif word[x] in let:
                                    turn.append(Point(i, j - ind + x, word[x]))
                                    let.remove(word[x])
                                elif '*' in let:
                                    turn.append(Point(i, j - ind + x, word[x]))
                                    let.remove('*')
                                else:
                                    break
                        else:
                            check = self.check_turn(turn)
                            if check.result and check.score != 0:
                                res.append(TurnStruct(True, turn, check.score))
                    # Проверка по вертикали
                    let = self.letters.copy()
                    turn = []
                    if self._empty(i - ind - 1, j) and self._empty(i - ind + len(word), j):
                        for x in range(len(word)):
                            if not 0 <= i - ind + x < len(self.game.matrix.Mainmap):
                                break
                            if self.game.matrix.Mainmap[i - ind + x][j] != word[x]:
                                if self.game.matrix.Mainmap[i - ind + x][j] != '':
                                    break
                                elif word[x] in let:
                                    turn.append(Point(i - ind + x, j, word[x]))
                                    let.remove(word[x])
                                elif '*' in let:
                                    turn.append(Point(i, j - ind + x, word[x]))
                                    let.remove('*')
                                else:
                                    break
                        else:
                            check = self.check_turn(turn)
                            if check.result and check.score != 0:
                                res.append(TurnStruct(True, turn, check.score))
        return res

    def cpu(self):
        """Вычисляет информацию для хода"""
        letters = ""
        newlet = ""
        for i in self.game.matrix.Mainmap:
            for j in i:
                newlet += j
                if letters.count(j) == 0:
                    letters += j
        for i in self.letters:
            newlet += i
            if letters.count(i) == 0:
                letters += i
        if '*' in letters:
            print("Hi")
        words = self.game.matrix.dict.prepare(letters, newlet)
        res = []
        for word in words:
            for char in range(len(word)):
                temp = self._available(word, char)
                if temp:
                    res += temp
                    break  # SOME optimize
            if self.timeout < 30:
                break

        if res:
            res = sorted(res, key=lambda item: item.score)
            index = round(len(res) * self.diff)
            if index > 0:
                index -= 1
            # print(res[index].score)
            # for x in range(len(self.game.matrix.Mainmap)):
            #     for y in range(len(self.game.matrix.Mainmap[0])):
            #         for let in res[index].letters:
            #             if let.x == x and let.y == y:
            #                 print(let.letter, end='\t')
            #                 break
            #         else:
            #             print(self.game.matrix.Mainmap[x][y], end='\t')
            #     print()
            # print('\n---------\n')
            self.accept_turn(TurnStruct(True, res[index].letters))
        else:
            # Reject all letters
            self.accept_turn(TurnStruct(False, self.letters.copy()))

    def _daemon(self):
        """Демон бота"""
        while self.botEnable:
            if self.isTurn:
                self.cpu()
            time.sleep(1)


class GameServer:
    def __init__(self):
        self.players = []
        self.playStatus = False
        self.alphabet = ""
        self.matrix = Matrix()
        self.playerIndex = -1
        for key, value in GameConfig.letters.items():
            self.alphabet += key * value["count"]
        self.thread = Thread(target=self._game_loop)

    def add_player(self, player):
        if player.type == "local":
            self.players.append(PlayerLocal(player.name, self))
        elif player.type == "bot":
            self.players.append(PlayerBot(player.name, self, player.diff))
        else:
            warnings.warn("Тип не найден" + player.type)

    def run_game(self):
        self.playStatus = True
        self.thread.start()

    def __del__(self):
        del self.players
        self.playStatus = False
        self.thread.join(1)

    def _give_letter(self, player):
        """Выдает игроку недостающие фишки"""
        while len(player.letters) < GameConfig.startCount and len(self.alphabet) > 0:
            i = self.alphabet[random.randrange(len(self.alphabet))]
            player.letters.append(i)
            self.alphabet = self.alphabet.replace(i, "", 1)

    def _game_loop(self):
        skip = 0
        while self.playStatus:
            for player in range(len(self.players)):
                self.playerIndex = player
                self._give_letter(self.players[player])
                result = self.players[player].action()
                self.matrix.acceptedWords.extend(result.words)
                if result.changed and result.score != 0:
                    skip = 0
                    for i in result.letters:
                        GameConfig.map[i.x][i.y] = 0
                else:
                    skip += 1
                if result.changed and len(result.letters) == GameConfig.startCount:
                    self.players[player].score += GameConfig.fullBonus
                print("Игрок {} закончил ход {}. Набрал {} очков".format(self.players[player].name,
                                                                         "Активно" if result.changed else "Пассивно",
                                                                         self.players[player].score))
                print("Осталось в руке {} букв. В мешке - {} букв".format(str(len(self.players[player].letters)),
                                                                          str(len(self.alphabet))))
                print("-" * 64)
                for i in self.players:
                    i.turn_end()
                if len(self.alphabet) == 0 or skip >= GameConfig.skipEnd * len(self.players):
                    self.playStatus = False
                    break
        print("Игра окончена")
        for i in self.players:
            print("Игрок {} набрал {} очков".format(i.name, i.score))


if __name__ == '__main__':
    game_server = GameServer()
    game_server.add_player(Player("BOT1", "bot", diff=0.5))
    game_server.add_player(Player("BOT2", "bot", diff=1))
    game_server.matrix.Mainmap[7][7] = "П"
    game_server.matrix.Mainmap[7][8] = "Р"
    game_server.matrix.Mainmap[7][9] = "И"
    game_server.matrix.Mainmap[7][10] = "В"
    game_server.matrix.Mainmap[7][11] = "Е"
    game_server.run_game()
    # game_server.players[0].letters = ["Т"]
