class GameConfig:
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


# Класс ячейки поля
class Point:
    info = [{'color': 'white', 'multi': 'letter', 'value': 1},
            {'color': 'green', 'multi': 'letter', 'value': 2},
            {'color': 'blue', 'multi': 'word', 'value': 2},
            {'color': 'yellow', 'multi': 'letter', 'value': 3},
            {'color': 'red', 'multi': 'word', 'value': 3}, ]

    def get_info(self):
        return self.info[self.t]

    def __init__(self, x, y, t, letter=None):
        self.x = x
        self.y = y
        self.t = t
        self.letter = letter


# Класс игрового поля
class Matrix:
    def __init__(self):
        self.map = [[Point(j,i,GameConfig.map[i][j]) for i in range(15)] for j in range(15)]


a = Matrix()
print(a.map[1][5].t)
