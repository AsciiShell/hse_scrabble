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

    def get_temporary(self):
        """Возвращает предварительную версию матрицы"""
        temp_map = self.map.copy()
        for i in self.temp:
            temp_map[i.x][i.y] = i
        return temp_map

    def accept_temp(self):
        """Принимает временные изменения"""
        for i in self.temp:
            self.map[i.x][i.y] = i
        self.reject_temp()

    def reject_temp(self):
        """Отклоняет временные изменения"""
        self.temp.clear()

    def check_temp(self):
        """Возвращает True, если временная матрица правильная"""
        # TODO andrsolo21
        return True

    def get(self, x, y):
        """Возвращает точку по адресу"""
        return self.map[x][y]

    def __init__(self):
        """Создает новую игровую карту"""
        self.map = [[Point(j, i) for i in range(15)] for j in range(15)]
        self.temp = []


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
        # TODO test
        alphabet = alphabet.upper()
        if len(alphabet) >= 32:
            return self.dict

        temp_dict = []
        for i in self.dict:
            for j in alphabet:
                if i.count(j) > 0:
                    temp_dict.append(i)
                    break
        return temp_dict

    def __init__(self):
        """Инициализирует словарь начальным списком слов"""
        with open(self.filename, "r", encoding="utf-8") as f:
            self.dict = f.read().lower().split("\n")
