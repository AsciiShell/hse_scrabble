import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QGridLayout, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QHBoxLayout, QFrame, QSplitter, QStyleFactory, QApplication, QMainWindow, QPushButton, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon, QBrush
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QCoreApplication
from server import *




class MAIN_painter(QWidget):

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
        self.yi = self.widthtotal * (1 - 2 * self.k2) / 15 - self.ot
        """инициализация окна"""
        self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
        self.show()
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
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        background.setPen(col)
        """background"""
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
                self.karta[i][j] = [xp], [yp]
                background.setBrush(QColor(Point.info[GameConfig.map[i][j]]['color']))
                background.drawRect(xp, yp, self.yi, self.yi)
        background.setBrush(QColor(255, 255, 255))
        """history"""
        background.drawRect(self.ot, self.ot + self.libh, self.libw - self.ot, 2 * self.libh - self.ot - self.ot)
        """letters"""
        background.drawRect(self.libw + self.ot, 15 * (self.ot + self.yi) + self.ot, 15 * (self.ot + self.yi) - self.ot,
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
        background.drawRect(self.karta[7][7][0][0], self.karta[7][7][1][0], self.yi, self.yi)
        """for i in range(15):
            for j in range(15):
                background.setPen(QColor(255, 255, 255))
                background.setFont(QFont('Decorative', 10))
                background.drawText(self.karta[i][j][0][0],self.karta[i][j][1][0], self.yi,self.yi,Qt.AlignCenter, Point.info[GameConfig.map[i][j]]['multi'])"""


class FIRST_painter(QMainWindow):

    def __init__(self):
        """первое окно\nдве кнопки: подключиться и создать игру"""
        super().__init__()
        self.st = ''

        self.initUI()

    def initUI(self):
        btncreate = QPushButton("Create game", self)
        btncreate.move(30, 50)

        btnconnect = QPushButton("Connect game", self)
        btnconnect.move(150, 50)

        btncreate.clicked.connect(self.buttoncreate)
        btnconnect.clicked.connect(self.buttonconnect)

        self.statusBar()

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Event sender')
        self.show()

    def buttoncreate(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')

    def buttonconnect(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')
        createnewform(2)


class CONNECT_painter(QWidget):

    def __init__(self):
        super().__init__()
        self.st = ''

        self.initUI()

    def initUI(self):
        self.koef = 0.8
        self.k2 = 0.3
        self.widthtotal = self.koef * QDesktopWidget().availableGeometry().width() * 0.5
        self.heighttotal = self.koef * QDesktopWidget().availableGeometry().height() - 30
        self.ot = QDesktopWidget().availableGeometry().width() / 100
        self.libw = self.widthtotal * self.k2
        self.libh = self.heighttotal / 3
        self.yi = self.widthtotal * (1 - 2 * self.k2) / 15 - self.ot
        """инициализация окна"""
        self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
        self.setWindowTitle('Event sender')
        self.show()

        btnconcreate = QPushButton("Подключиться", self)
        btnfirst = QPushButton("Вернуться назад", self)

        title = QLabel('Title')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("QLabel {background-color: red;}")
        status = QLineEdit('')
        title2 = QLabel('Title2')
        title2.setAlignment(Qt.AlignCenter)
        title2.setStyleSheet("QLabel {background-color: yellow;}")

        grid = QGridLayout()
        grid.setSpacing(8)

        btnconcreate.clicked.connect(self.buttonconcreate)
        btnfirst.clicked.connect(self.buttonfirst)

        grid.addWidget(title, 0, 0, 2, 3)
        grid.addWidget(title2, 4, 0, 1, 3)
        grid.addWidget(status, 2, 0, 1, 3)

        grid.addWidget(btnfirst, 1, 4, 1, 1)
        grid.addWidget(btnconcreate, 0, 4, 1, 1)

        self.setLayout(grid)

        # btnfirst.clicked.connect(QCoreApplication.instance().quit)
        '''vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addWidget(btnconcreate)
        vbox.addWidget(btnfirst)
        hbox = QHBoxLayout()
        hbox.addStretch(3)
        hbox.addLayout(vbox)
        self.setLayout(hbox)'''

        # self.statusBar()

    def buttonconcreate(self):
        pass

    def buttonfirst(self):
        createnewform(1)


def createnewform(number):
    global ex1
    global ex2
    global ex3
    app = QApplication(sys.argv)
    if number == 1:
        ex1 = FIRST_painter()
    elif number == 2:
        ex2 = CONNECT_painter()
    elif number == 3:
        ex3 = MAIN_painter()
    sys.exit(app.exec_())


if __name__ == '__main__':
    createnewform(2)
