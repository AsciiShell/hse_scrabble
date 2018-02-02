import sys
from PyQt5.QtWidgets import QWidget,QDesktopWidget, QPushButton,QHBoxLayout, QFrame,QSplitter, QStyleFactory, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon, QBrush
from PyQt5.QtCore import Qt
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

    def prov(words,x,y,napr,newkoord):
        """проверяет, начие слова в этой ячейке (начало слова)"""
        flag = 0
        if (napr == 2) and (y != 14) :
            if (y != 0):
                if (words[y-1][x] == '') and (words[y+1][x] != ''):
                    flag = 1
            else:
                if (words[y+1][x] != ''):
                    flag = 1
        if (napr == 1) and (x != 14):
            if (x != 0):
                if (words[y][x-1] == '') and (words[y][x+1] != ''):
                    flag = 1
            else:
                if (words[y][x+1] != ''):
                    flag = 1
        if (flag == 1):
            return(schit(words,x,y,napr,newkoord))
        else:
            return(['',0])

    def schit(words,x,y,napr,newkoord):
        """считывает слово"""
        s = ''
        newword = 0
        if (napr == 2):
            a=1
            while (a != 0):
                koord = [x,y]
                if (koord in newkoord):
                    newword = 1
                s = s + words[y][x]
                if (y == 14):
                    a = 0
                else:
                    if (words[y+1][x] == ''):
                        a = 0
                y = y + 1
        else:
            a=1
            while (a != 0):
                koord = [x,y]
                if (koord in newkoord):
                    newword = 1
                s = s + words[y][x]
                if (x == 14):
                    a = 0
                else:
                    if (words[y][x+1] == ''):
                        a = 0
                x = x + 1
        return([s,newword])
    def pasteletters(words, newkoord, newletters):
        """вставляет буквы в матрицу"""
        for i in range(len(newkoord)):
            words[newkoord[i][1]][newkoord[i][0]] = newletters[i]
        return(words)
                    

    def serch(self):
        """ищет слова в матрице"""
        newkoord = []
        newletters = []
        words  = self.map
        n = 0
        for i in self.temp:
            newleters.append([[i.x],[i.y]])
            newkoord.append(i.letter)
        #newkoord = [[4,6],[4,8],[4,9],[4,10]]
        #newletters = ['б','т','о','н']
        #движение по оси x = 1
        #движение по оси y = 2
        outx = []
        outy = []
        words = pasteletters(words, newkoord, newletters)
        for i in range(len(words)):
            for j in range(len(words[i])):
                if (words[i][j] != ''):
                    slx = prov(words,j,i,1,newkoord)
                    sly = prov(words,j,i,2,newkoord)
                    if (slx[1] == 1):
                        outx.append(slx)
                    if (sly[1] == 1):
                        outx.append(sly)
                    """if (slx[0] != ''):
                        print(slx[0])
                    if (sly[0] != ''):
                        print(sly[0])"""

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
            self.dict = f.readlines()

class painter(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        
        self.koef = 0.8
        self.k2 = 0.3
        self.widthtotal = self.koef * QDesktopWidget().availableGeometry().width()
        self.heighttotal = self.koef * QDesktopWidget().availableGeometry().height() - 30
        self.ot = QDesktopWidget().availableGeometry().width() / 300
        self.libw = self.widthtotal * self.k2
        self.libh = self.heighttotal / 3
        self.yi = self.widthtotal * (1 - 2* self.k2) / 15 - self.ot
        """инициализация окна"""
        self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
        self.show()    
        #self.square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())
        #self.setWindowTitle('Icon')
        #self.setWindowIcon(QIcon('web.png'))
        #QToolTip.setFont(QFont('SansSerif', 10))

        
    def paintEvent(self, e):
        background = QPainter()
        background.begin(self)
        self.drawBackground(background)
        background.end()
        
        
    def drawBackground(self, background):
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        background.setPen(col)
        """background"""
        background.setBrush(QColor(220, 220, 220))
        background.drawRect(0, 0, self.widthtotal * 5, self.heighttotal * 5)
        """iam"""
        background.setBrush(QColor(255, 255, 255))
        background.drawRect(self.ot,self.ot,self.libw - self.ot,self.libh - self.ot)
        """matrix"""
        self.karta = [0] * 15
        for i in range(15):
            self.karta[i] = [0] * 15
        for i in range(15):
            for j in range(15):
                xp = self.libw + j * (self.ot + self.yi) + self.ot
                yp = self.ot + i * (self.ot + self.yi)
                self.karta[i][j] = [xp],[yp]
                background.setBrush(QColor(Point.info[GameConfig.map[i][j]]['color']))
                background.drawRect(xp ,yp,self.yi , self.yi )
        background.setBrush(QColor(255, 255, 255))
        """history"""
        background.drawRect(self.ot,self.ot + self.libh,self.libw - self.ot,2 * self.libh - self.ot - self.ot)
        """letters"""
        background.drawRect(self.libw + self.ot,15 * (self.ot + self.yi) + self.ot,15 * (self.ot + self.yi) - self.ot,self.heighttotal - 15 * (self.ot + self.yi) - 2* self.ot)
        """p1"""
        background.drawRect(self.widthtotal * (1 - self.k2) + self.ot,self.ot,self.libw - self.ot- self.ot,self.libh - self.ot)
        """p2"""
        background.drawRect(self.widthtotal * (1 - self.k2) + self.ot,self.ot + self.libh,self.libw - self.ot- self.ot,self.libh - self.ot)
        """p3"""
        background.drawRect(self.widthtotal * (1 - self.k2) + self.ot,self.ot + self.libh * 2,self.libw - self.ot- self.ot,self.libh - self.ot - self.ot)
        """закрашивает квадратик по координатам"""
        background.setBrush(QColor(200, 200, 200))
        background.drawRect(self.karta[7][7][0][0] ,self.karta[7][7][1][0],self.yi , self.yi )
        """for i in range(15):
            for j in range(15):
                background.setPen(QColor(255, 255, 255))
                background.setFont(QFont('Decorative', 10))
                background.drawText(self.karta[i][j][0][0],self.karta[i][j][1][0], self.yi,self.yi,Qt.AlignCenter, Point.info[GameConfig.map[i][j]]['multi'])"""
        
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = painter()
    sys.exit(app.exec_())
