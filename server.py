from scrabblelib import *


class GamePlayer:
    def __init__(self, name: str) -> None:
        self.name = name
        self.score = 0
        self.letters = []
        self.isTurn = False
        self.timeout = 0
        self.input = None
        self.result = None
        self.list_call_end = []
        self.list_call_start = []

    def event_end(self, callback: function) -> None:
        """Срабатывает при завершении хода любого игрока. Перерисовка"""
        self.list_call_end.append(callback)

    def event_start(self, callback: function) -> None:
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
