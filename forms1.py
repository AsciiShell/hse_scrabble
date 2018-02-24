import sys
import random
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QGridLayout, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QHBoxLayout, QFrame, QSplitter, QStyleFactory, QApplication, QMainWindow, QPushButton, QApplication,QListWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon, QBrush, QDrag
from PyQt5.QtCore import *
from server import *

class Fishka(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.initUI()

    def initUI(self):
        self.MyLetter = ''
        self.MyPrice = 0
        self.MyKoord = [None , 0]





class GameWindow(QWidget):

    def __init__(self, parent=None):
        super(GameWindow, self).__init__(parent)
        self.koef = 1
        self.pos = 0
        self.k2 = 0.3
        self.widthtotal = self.koef * QDesktopWidget().availableGeometry().width()
        self.heighttotal = self.koef * QDesktopWidget().availableGeometry().height() - 30
        self.ot = QDesktopWidget().availableGeometry().width() / 300
        self.libw = self.widthtotal * self.k2
        self.libh = self.heighttotal / 3
        self.yi = self.widthtotal * (1 - 2 * self.k2) / 15 - self.ot
        self.letterskoord = [self.libw + self.ot, 15 * (self.ot + self.yi) + self.ot]
        """инициализация окна"""
        self.btnconcreateret = QPushButton("назад", self)
        self.btnconcreateret.move( self.widthtotal - 120, 50)
        #self.stolfishki =


        #CreateFishka(self.let,self.poi,100 + (self.yi + self.ot) * self.pos, 90,self.fishka1,1)

        self.initUI()

    def initUI(self):
        self.matr = Matrix()
        """основная часть создания элементов формы"""
        #self.list = QListWidget()
        #self.list.setGeometry(self.ot, self.ot + self.libh + 20, self.libw - self.ot,2 * self.libh - self.ot - self.ot - 20)
        """Buttons"""
        self.btnconcreateret = QPushButton("назад", self)
        self.btnconcreateret.move( self.widthtotal - 120, 50)
        self.setAcceptDrops(True)

        for i in range(10):
            self.matr.map[i][i+2] = self.getletter()
        """Расстановка кнопок, уже имеющихся в таблице"""
        self.ButMap = [[]]

        """for i in range(15):
            l = []
            for j in range(15):
                l.append(Fishka(self.matr.map[j][i], self))
            self.ButMap.append(l)
            for j in range(15):
                self.ButMap[i][j].MyLetter = self.matr.map[j][i]
                self.ButMap[i][j].MyPrice = GameConfig.letters[self.matr.map[i][j]]['price']
                self.ButMap[i][j].MyKoord = [j , i]
                self.ButMap[i][j].setGeometry(self.karta[i][j][0], self.karta[i][j][0] , self.yi, self.yi)"""

        """расстановка кнопок для перемещения"""
        self.myletters = []
        for i in range(GameConfig.startCount):
            gs = self.getletter()
            self.myletters.append(Fishka((gs + '(' + str(i) + ')'), self))
            self.myletters[i].MyLetter = gs
            self.myletters[i].MyPrice = GameConfig.letters[gs]['price']
            self.myletters[i].MyKoord = [None , i]
            self.myletters[i].setGeometry(QRect(self.letterskoord[0] + (self.yi + self.ot)* i + self.ot, self.letterskoord[1] + self.ot, self.yi, self.yi))

        """line edit/konsol"""
        self.konsol = QLineEdit(self)
        self.konsol.setGeometry(self.ot, self.ot + self.libh, self.libw - self.ot, 20)
        self.konsol.returnPressed.connect(self.enter)

    def enter(self):
        """функция обработки строки консоли"""
        """move i,x,y"""
        l = self.konsol.text()
        name = l.split(" ")
        if name[0] == "move":
            ch = name[1].split(",")
            i = int(ch[0])
            x = int(ch[1])
            y = int(ch[2])
            if self.myletters[i].MyKoord[0] != None:
                t = self.myletters[i].MyKoord
                ii = 0
                while t != self.matr.newkoord[ii] and ii < len(self.matr.newkoord):
                    ii += 1
                if ii < len(self.matr.newkoord):
                    self.matr.newkoord[ii]= [None,None]
            self.myletters[i].move(self.karta[x][y][0], self.karta[x][y][1])
            self.myletters[i].MyKoord = [y,x]
            self.matr.newletters.append(self.myletters[i].MyLetter)
            self.matr.newkoord.append([y,x])
        if name[0] == 'show':
            self.ShowWords()
        if name[0] == 'help' or name[0] == 'SOS':
            self.Help()
        self.konsol.clear()

    def Help(self):

        print('переместить кнопку - move i,x,y (i - номер кнопки,(x, y) - координаты)')
        print('поиск новых слов - show')
        for i in self.matr.map:
            print(i)
    def ShowWords(self):
        """выводит новые слова"""
        self.matr.pasteletters()
        self.matr.serch()
        print (self.matr.outx)
        print (self.matr.outy)
        for i in self.matr.map:
            print(i)

    def getletter(self):
        """выбирает случайную букву"""
        random.seed()
        genletter = random.choice(GameConfig.let)
        while GameConfig.letters[genletter]['count'] < 0:
            genletter = random.choice(GameConfig.let)
        GameConfig.letters[genletter]['count'] -= 1
        return (genletter)


    #self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
        # self.square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())
        # self.setWindowTitle('Icon')
        # self.setWindowIcon(QIcon('web.png'))
        # QToolTip.setFont(QFont('SansSerif', 10))





    def paintEvent(self, e):
        background = QPainter()
        background.begin(self)
        self.drawBackground(background)
        background.end()

    def drawBackground(self, background):
        """background)"""

        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        background.setPen(col)

        background.setBrush(QColor(220, 220, 220))
        background.drawRect(0, 0, self.widthtotal * 5, self.heighttotal * 5)
        """iam"""
        background.setBrush(QColor(255, 255, 255))
        background.drawRect(self.ot, self.ot, self.libw - self.ot, self.libh - self.ot)
        """matrix"""
        self.karta = [0] * 15
        for i in range(15):
            self.karta[i] = [0] * 15
        for i in range(15):
            for j in range(15):
                xp = self.libw + j * (self.ot + self.yi) + self.ot
                yp = self.ot + i * (self.ot + self.yi)
                self.karta[i][j] = [xp , yp]
                background.setBrush(QColor(Point.info[GameConfig.map[i][j]]['color']))
                background.drawRect(xp, yp, self.yi, self.yi)
        background.setBrush(QColor(255, 255, 255))
        """history"""
        background.drawRect(self.ot, self.ot + self.libh, self.libw - self.ot, 2 * self.libh - self.ot - self.ot)
        """letters"""

        background.drawRect(self.letterskoord[0], self.letterskoord[1], 15 * (self.ot + self.yi) - self.ot,
                            self.heighttotal - 15 * (self.ot + self.yi) - 2 * self.ot)

        """p1"""
        background.drawRect(self.widthtotal * (1 - self.k2) + self.ot, self.ot, self.libw - self.ot - self.ot,
                            self.libh - self.ot)
        """p2"""
        background.drawRect(self.widthtotal * (1 - self.k2) + self.ot, self.ot + self.libh,
                            self.libw - self.ot - self.ot, self.libh - self.ot)
        """p3"""
        background.drawRect(self.widthtotal * (1 - self.k2) + self.ot, self.ot + self.libh * 2,
                            self.libw - self.ot - self.ot, self.libh - self.ot - self.ot)
        """закрашивает квадратик по координатам"""
        background.setBrush(QColor(200, 200, 200))
        background.drawRect(self.karta[7][7][0], self.karta[7][7][1], self.yi, self.yi)
        """for i in range(15):
            for j in range(15):
                background.setPen(QColor(255, 255, 255))
                background.setFont(QFont('Decorative', 10))
                background.drawText(self.karta[i][j][0][0],self.karta[i][j][1][0], self.yi,self.yi,Qt.AlignCenter, Point.info[GameConfig.map[i][j]]['multi'])"""




class ScreenSet():
    def __init__(self):
        self.koef = 1
        self.k2 = 0.3
        self.widthtotal = self.koef * QDesktopWidget().availableGeometry().width()
        self.heighttotal = self.koef * QDesktopWidget().availableGeometry().height() - 30
        self.ot = QDesktopWidget().availableGeometry().width() / 300
        self.libw = self.widthtotal * self.k2
        self.libh = self.heighttotal / 3
        self.yi = self.widthtotal * (1 - 2 * self.k2) / 15 - self.ot


class FirstWindow(QWidget):
    def __init__(self, parent=None):
        super(FirstWindow, self).__init__(parent)
        self.btncreate = QPushButton("Create game", self)
        self.btncreate.move(30, 50)

        self.btnconnect = QPushButton("Connect game", self)
        self.btnconnect.move(150, 50)

        #hbox = QHBoxLayout()
        #hbox.addStretch(1)
        #hbox.addWidget(self.btnconnect)
        #hbox.addWidget(self.btncreate)
        #vbox = QVBoxLayout()
        #vbox.addStretch(1)
        #vbox.addLayout(hbox)

        #self.setLayout(vbox)

        #self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Event sender')

class SecondWindow(QWidget):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        self.koef = 0.8
        self.k2 = 0.3
        self.widthtotal = self.koef * QDesktopWidget().availableGeometry().width() * 0.5
        self.heighttotal = self.koef * QDesktopWidget().availableGeometry().height() - 30
        self.ot = QDesktopWidget().availableGeometry().width() / 100
        self.libw = self.widthtotal * self.k2
        self.libh = self.heighttotal / 3
        self.yi = self.widthtotal * (1 - 2 * self.k2) / 15 - self.ot
        """инициализация окна"""
        #self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
        self.setWindowTitle('Event sender')

        self.btnconcreate = QPushButton("Подключиться", self)
        self.btnfirst = QPushButton("Вернуться назад", self)

        title = QLabel('Title')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("QLabel {background-color: red;}")

        title2 = QLabel('Title2')
        title2.setAlignment(Qt.AlignCenter)
        title2.setStyleSheet("QLabel {background-color: yellow;}")

        self.grid = QGridLayout()
        self.grid.setSpacing(8)

        self.grid.addWidget(title, 0, 0, 2, 3)
        self.grid.addWidget(title2, 4, 0, 1, 3)


        self.grid.addWidget(self.btnfirst, 1, 4, 1, 1)
        self.grid.addWidget(self.btnconcreate, 0, 4, 1, 1)

        self.setLayout(self.grid)

class ThirdWindowCreate(QWidget):
    def __init__(self, parent=None):
        super(ThirdWindowCreate, self).__init__(parent)
        self.koef = 1
        self.k2 = 0.3
        self.widthtotal = self.koef * QDesktopWidget().availableGeometry().width()/2
        self.heighttotal = self.koef * QDesktopWidget().availableGeometry().height() - 30
        self.ot = QDesktopWidget().availableGeometry().width() / 300
        self.libw = self.widthtotal * self.k2
        self.libh = self.heighttotal / 3
        self.yi = self.widthtotal * (1 - 2 * self.k2) / 15 - self.ot

        """инициализация окна"""
        #self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
        self.setWindowTitle('Event sender')

        self.btnconcreate = QPushButton("Подключиться", self)
        self.btnconcreate.move( self.widthtotal - 120, 50)
        self.btnFirst = QPushButton("Вернуться назад", self)
        self.btnFirst.move( self.widthtotal - 120, 100)

    """hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.btnconnect)
        hbox.addWidget(self.btncreate)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)"""
        #self.setLayout(vbox)







class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.koef = 1
        self.k2 = 0.3
        self.widthtotal = self.koef * QDesktopWidget().availableGeometry().width()
        self.heighttotal = self.koef * QDesktopWidget().availableGeometry().height() - 30
        self.ot = QDesktopWidget().availableGeometry().width() / 300
        self.libw = self.widthtotal * self.k2
        self.libh = self.heighttotal / 3
        self.yi = self.widthtotal * (1 - 2 * self.k2) / 15 - self.ot
        """инициализация окна"""
        self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
        self.startGame()

    def startGame(self):
        self.GameCreate = GameWindow(self)
        self.setWindowTitle("GameCreate")
        self.setGeometry(0 , 30, self.widthtotal , self.heighttotal)
        self.setCentralWidget(self.GameCreate)
        #self.GameCreate.btnFirst.clicked.connect(self.startFirst)
        self.GameCreate.btnconcreateret.clicked.connect(self.startThirdCreate)
        self.show()

    def startThirdCreate(self):
        self.ThirdCreate = ThirdWindowCreate(self)
        self.setWindowTitle("ThirdWindowCreate")
        self.setGeometry(self.widthtotal / 4, 30, self.widthtotal / 2, self.heighttotal)
        self.setCentralWidget(self.ThirdCreate)
        self.ThirdCreate.btnFirst.clicked.connect(self.startFirst)
        self.ThirdCreate.btnconcreate.clicked.connect(self.startGame)
        self.show()

    def startSecond(self):
        self.Second = SecondWindow(self)
        self.setWindowTitle("SecondWindow")
        self.setGeometry(0, 30, self.widthtotal/2, self.heighttotal/2)
        self.setCentralWidget(self.Second)
        self.Second.btnfirst.clicked.connect(self.startFirst)
        #self.Second.btnconcreate.clicked.connect(self.startThirdEx1)

        self.show()

    def startFirst(self):
        self.First = FirstWindow(self)
        self.setWindowTitle("FirstWindow")
        self.setGeometry(300, 300, 260, 150)
        self.setCentralWidget(self.First)
        self.First.btnconnect.clicked.connect(self.startSecond)
        self.First.btncreate.clicked.connect(self.startThirdCreate)
        self.show()








if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())