import os
import random
import warnings
import time
from threading import Thread

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
               '*': {'count': 0, 'price': None}}
    """Начальное число фишек"""
    startCount = 10
    """Бонус за полное использование фишек"""
    fullBonus = 15
    """Количество пропусков для завершения игры"""
    skipEnd = 2
    """Время хода"""
    turnTime = 120

class Point:
    """Класс ячейки поля
    TODO переделать"""
    info = [{'color': 'white', 'multi': 'letter', 'value': 1},
            {'color': 'green', 'multi': 'letter', 'value': 2},
            {'color': 'blue', 'multi': 'word', 'value': 2},
            {'color': 'yellow', 'multi': 'letter', 'value': 3},
            {'color': 'red', 'multi': 'word', 'value': 3}, ]

    def get_info(self):
        """Возвращает информацию о текущей точке"""
        return self.info[self.t]

    def __init__(self, x, y, letter, t=None):
        """Создает точку
        x, y - координаты
        t - числовой тип
        letter - буква
        """
        self.x = x
        self.y = y
        self.letter = letter
        if t is None:
            try:
                self.t = GameConfig.map[x][y]
            except Exception:
                print("Error")
        else:
            self.t = t
        self.color = Point.info[self.t]["color"]
        self.multi = Point.info[self.t]["multi"]
        self.value = Point.info[self.t]["value"]
        if self.multi == "letter":
            self.score = GameConfig.letters[self.letter]['price'] * (self.value)
            self.multi = 1
        else:
            self.score = GameConfig.letters[self.letter]['price']
            self.multi = self.multi

class Message:
    """Класс возвращаемых сообщений"""

    def __init__(self, res=False, msg=""):
        self.res = res
        self.msg = msg


class MatrixResult:
    """Результат проверки матрицы"""

    def __init__(self, stat, score=0, words=None, errmsg=""):
        """Из функции выводится:
        self.result - успешность заполнения матрицы
        self.words - проверенные слова, найденные в матрице
        self.score - сумма очков за правильные слова
        self.wordsError - слова, которых нет в словаре
        self.msg - причина ошибки
        """
        self.score = score
        self.result = stat
        if stat:
            if words is None:
                warnings.warn("Слова не найдены")
            self.words = words
        else:
            self.msg = errmsg
            self.wordsError = words


class GamePlayer:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.letters = []
        self.isTurn = False
        self.timeout = 0
        self.input = None
        self.result = None
        self.list_call_end = []
        self.list_call_start = []

    def event_end(self, callback):
        """Срабатывает при завершении хода любого игрока. Перерисовка"""
        self.list_call_end.append(callback)

    def event_start(self, callback):
        """Предупреждает игрока о начале его хода. Активирует игровой интерфейс"""
        self.list_call_start.append(callback)

    def call_end(self, *args, **kwargs):
        """Оповещает все события о конце хода"""
        for i in self.list_call_end:
            i(args, kwargs)

    def call_start(self, *args, **kwargs):
        """Оповещает игрока о начале хода"""
        for i in self.list_call_start:
            i(args, kwargs)

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