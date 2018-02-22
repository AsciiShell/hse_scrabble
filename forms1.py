import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QGridLayout, QMainWindow, QPushButton, QApplication, \
    QGroupBox, QMessageBox

from server import *


class GameWindow(QWidget):

    def __init__(self, parent=None):
        super(GameWindow, self).__init__(parent)
        self.let = "A"
        self.poi = 5
        self.koef = 1
        self.pos = 0
        self.k2 = 0.3
        self.widthtotal = self.koef * QDesktopWidget().availableGeometry().width()
        self.heighttotal = self.koef * QDesktopWidget().availableGeometry().height() - 30
        self.ot = QDesktopWidget().availableGeometry().width() / 300
        self.libw = self.widthtotal * self.k2
        self.libh = self.heighttotal / 3
        self.yi = self.widthtotal * (1 - 2 * self.k2) / 15 - self.ot
        """инициализация окна"""
        self.btnconcreateret = QPushButton("назад", self)
        self.btnconcreateret.move(self.widthtotal - 120, 50)
        # self.stolfishki =
        self.fishka1 = QPushButton(self.let, self)
        self.fishka1.setGeometry(QRect(100 + (self.yi + self.ot) * 1, 90, self.yi, self.yi))
        self.fishka2 = QPushButton(self.let, self)
        self.fishka2.setGeometry(QRect(100 + (self.yi + self.ot) * 2, 90, self.yi, self.yi))
        # CreateFishka(self.let,self.poi,100 + (self.yi + self.ot) * self.pos, 90,self.fishka1,1)

        # self.initUI()

    # def initUI(self):

    # self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
    # self.square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())
    # self.setWindowTitle('Icon')
    # self.setWindowIcon(QIcon('web.png'))
    # QToolTip.setFont(QFont('SansSerif', 10))
    def CreateFishka(self, letter, points, x, y, but, pos):
        if pos > 0:
            but.setGeometry(QRect(x, y, self.yi, self.yi))

    def paintEvent(self, e):
        background = QPainter()
        background.begin(self)
        self.drawBackground(background)
        background.end()

    def drawBackground(self, background):
        self.btnconcreateret = QPushButton("назад", self)
        self.btnconcreateret.move(self.widthtotal - 120, 50)
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

        # hbox = QHBoxLayout()
        # hbox.addStretch(1)
        # hbox.addWidget(self.btnconnect)
        # hbox.addWidget(self.btncreate)
        # vbox = QVBoxLayout()
        # vbox.addStretch(1)
        # vbox.addLayout(hbox)

        # self.setLayout(vbox)

        # self.setGeometry(300, 300, 290, 150)
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
        # self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
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
        self.widthtotal = self.koef * QDesktopWidget().availableGeometry().width() / 2
        self.heighttotal = self.koef * QDesktopWidget().availableGeometry().height() - 30
        self.ot = QDesktopWidget().availableGeometry().width() / 300
        self.libw = self.widthtotal * self.k2
        self.libh = self.heighttotal / 3
        self.yi = self.widthtotal * (1 - 2 * self.k2) / 15 - self.ot

        """инициализация окна"""
        # self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
        self.setWindowTitle('Event sender')

        self.btnconcreate = QPushButton("Подключиться", self)
        self.btnconcreate.move(self.widthtotal - 120, 50)
        self.btnFirst = QPushButton("Вернуться назад", self)
        self.btnFirst.move(self.widthtotal - 120, 100)
        self.setupUi(self)
        self.serverInit()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(509, 300)
        self.groupBoxConnected = QGroupBox(Form)
        self.groupBoxConnected.setGeometry(QRect(10, 10, 341, 101))
        self.groupBoxConnected.setObjectName("groupBoxConnected")
        self.readyLabels = [QLabel(self.groupBoxConnected) for _ in range(4)]
        for i in range(len(self.readyLabels)):
            self.readyLabels[i].setGeometry(QRect(10, (i + 1) * 20, 200, 13))
            self.readyLabels[i].setText("Свободно")

        self.groupBoxQueue = QGroupBox(Form)
        self.groupBoxQueue.setGeometry(QRect(10, 120, 341, 500))
        self.groupBoxQueue.setObjectName("groupBoxQueue")
        self.queueItem = [QPushButton(self.groupBoxQueue) for _ in range(16)]
        for i in range(len(self.queueItem)):
            self.queueItem[i].setGeometry(QRect(10, (i + 1) * 23, 321, 20))
            self.queueItem[i].setText("Свободно")
            self.queueItem[i].rid = ""
            self.queueItem[i].clicked.connect(self.add_player)
        self.btnBack = QPushButton(Form)
        self.btnBot = QPushButton(Form)
        self.btnBot.setGeometry(QRect(370, 20, 75, 23))
        self.btnBot.setText("Добавить бота")
        self.btnBot.clicked.connect(self.add_bot)
        self.btnBack.setGeometry(QRect(370, 50, 75, 23))
        self.btnBack.setObjectName("btnBack")
        self.btnBack.clicked.connect(self.stop)
        self.btnStart = QPushButton(Form)

        self.btnStart.setGeometry(QRect(370, 70, 75, 23))
        self.btnStart.setObjectName("btnStart")
        self.btnStart.clicked.connect(self.stop)
        self.retranslateUi(Form)
        self.Form = Form
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBoxConnected.setTitle(_translate("Form", "Подключены"))

        self.groupBoxQueue.setTitle(_translate("Form", "Очередь"))
        self.btnBack.setText(_translate("Form", "Отмена"))
        self.btnStart.setText(_translate("Form", "Старт"))

    def stop(self):
        # TODO
        # Метод start_game в будущем будет возвращать информацию для запуска игры
        # При отмене нужно просто подавить выход
        # А при создании передать в создание другого класса
        # Как вариант, сделать все серверные класс статичными и глобальными
        self.game.start_game()
        self.gameThread.join(1)

    def add_player(self):
        res = self.game.add_player("net", self.sender().rid)
        if not res.res:
            QMessageBox.question(self.sender(), 'Ошибка', res.msg, QMessageBox.Ok, QMessageBox.Ok)

    def add_bot(self):
        res = self.game.add_player("bot")
        if not res.res:
            QMessageBox.question(self.sender(), 'Ошибка', res.msg, QMessageBox.Ok, QMessageBox.Ok)

    def server_redraw(self):
        while self.game.gamePrepare:
            i = 0
            for key, value in self.game.players.items():
                self.readyLabels[i].setText(value.name)
                i += 1
            while i < 4:
                self.readyLabels[i].setText("Свободно")
                i += 1

            i = 0
            while i < len(self.game.queue):
                name = str(self.game.queue[i]['add']) + self.game.queue[i]['ip'][0] + ":" + str(
                    self.game.queue[i]['ip'][1]) + " " + self.game.queue[i][
                           "name"]
                self.queueItem[i].rid = self.game.queue[i]["rid"]
                self.queueItem[i].setText(name)
                i += 1
            while i < 16:
                self.queueItem[i].setText("Свободно")
                self.queueItem[i].rid = ""
                i += 1
            # self.Form.setLayout(self.queueItem[-1])
            time.sleep(1)

    def serverInit(self):
        self.game = GameServerPrepare()
        self.game.create_game("Модератор")
        self.gameThread = Thread(target=self.server_redraw)
        self.gameThread.start()

    def __delete__(self, instance):
        self.game.start_game()

    """hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.btnconnect)
        hbox.addWidget(self.btncreate)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)"""
    # self.setLayout(vbox)


class ThirdWindowEx1(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(456, 575)
        self.gridLayoutWidget = QWidget(Form)
        self.gridLayoutWidget.setGeometry(QRect(10, 40, 441, 531))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setHorizontalSpacing(20)
        self.gridLayout_3.setVerticalSpacing(50)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_3 = QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_3.addWidget(self.pushButton_3, 0, 1, 1, 1)
        self.name2 = QLabel(self.gridLayoutWidget)
        self.name2.setObjectName("name2")
        self.gridLayout_3.addWidget(self.name2, 1, 0, 1, 1)
        self.name1 = QLabel(self.gridLayoutWidget)
        self.name1.setMouseTracking(False)
        self.name1.setLayoutDirection(Qt.LeftToRight)
        self.name1.setObjectName("name1")
        self.gridLayout_3.addWidget(self.name1, 0, 0, 1, 1)
        self.name4 = QLabel(self.gridLayoutWidget)
        self.name4.setObjectName("name4")
        self.gridLayout_3.addWidget(self.name4, 3, 0, 1, 1)
        self.name3 = QLabel(self.gridLayoutWidget)
        self.name3.setObjectName("name3")
        self.gridLayout_3.addWidget(self.name3, 2, 0, 1, 1)
        self.PushButton2 = QPushButton(self.gridLayoutWidget)
        self.PushButton2.setObjectName("PushButton2")
        self.gridLayout_3.addWidget(self.PushButton2, 1, 1, 1, 1)
        self.PushButton4 = QPushButton(self.gridLayoutWidget)
        self.PushButton4.setObjectName("PushButton4")
        self.gridLayout_3.addWidget(self.PushButton4, 3, 1, 1, 1)
        self.PushButton3 = QPushButton(self.gridLayoutWidget)
        self.PushButton3.setObjectName("PushButton3")
        self.gridLayout_3.addWidget(self.PushButton3, 2, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 1, 1, 1)
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_7 = QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_5.addWidget(self.label_6, 2, 0, 1, 1)
        self.pushButton_7 = QPushButton(self.gridLayoutWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_5.addWidget(self.pushButton_7, 0, 1, 1, 1)
        self.pushButton_8 = QPushButton(self.gridLayoutWidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_5.addWidget(self.pushButton_8, 1, 1, 1, 1)
        self.pushButton_9 = QPushButton(self.gridLayoutWidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_5.addWidget(self.pushButton_9, 2, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_5, 1, 1, 1, 1)
        self.label = QLabel(Form)
        self.label.setGeometry(QRect(20, 10, 171, 16))
        self.label.setObjectName("label")
        self.pushButton = QPushButton(Form)
        self.pushButton.setGeometry(QRect(240, 10, 81, 23))
        self.pushButton.setObjectName("pushButton")
        self.ButtonReturn = QPushButton(Form)
        self.ButtonReturn.setGeometry(QRect(334, 10, 101, 23))
        self.ButtonReturn.setObjectName("ButtonReturn")

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_3.setText(_translate("Form", "i am"))
        self.name2.setText(_translate("Form", "name2"))
        self.name1.setText(_translate("Form", "name1"))
        self.name4.setText(_translate("Form", "name4"))
        self.name3.setText(_translate("Form", "name3"))
        self.PushButton2.setText(_translate("Form", "добавить бота"))
        self.PushButton4.setText(_translate("Form", "добавить бота"))
        self.PushButton3.setText(_translate("Form", "добавить бота"))
        self.label_7.setText(_translate("Form", "player1"))
        self.label_8.setText(_translate("Form", "player2"))
        self.label_6.setText(_translate("Form", "player3"))
        self.pushButton_7.setText(_translate("Form", "добавить"))
        self.pushButton_8.setText(_translate("Form", "добавить"))
        self.pushButton_9.setText(_translate("Form", "добавить"))
        self.label.setText(_translate("Form", "Создание игры"))
        self.pushButton.setText(_translate("Form", "начать игру"))
        self.ButtonReturn.setText(_translate("Form", "вернуться назад"))


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
        self.startFirst()

    def startGame(self):
        self.gamePrepare.game.start_game()
        self.GameCreate = GameWindow(self)
        self.setWindowTitle("GameCreate")
        self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
        self.setCentralWidget(self.GameCreate)
        # self.GameCreate.btnFirst.clicked.connect(self.startFirst)
        self.GameCreate.btnconcreateret.clicked.connect(self.startGamePrepare)
        self.show()

    def startGamePrepare(self):
        self.gamePrepare = ThirdWindowCreate(self)
        self.setWindowTitle("Создание игры")
        self.setGeometry(self.widthtotal / 4, 30, self.widthtotal / 2, self.heighttotal)
        self.setCentralWidget(self.gamePrepare)
        self.gamePrepare.btnBack.clicked.connect(self.startFirst)
        self.gamePrepare.btnStart.clicked.connect(self.startGame)
        self.show()

    def startSecond(self):
        self.Second = SecondWindow(self)
        self.setWindowTitle("SecondWindow")
        self.setGeometry(0, 30, self.widthtotal / 2, self.heighttotal / 2)
        self.setCentralWidget(self.Second)
        self.Second.btnfirst.clicked.connect(self.startFirst)
        # self.Second.btnconcreate.clicked.connect(self.startThirdEx1)

        self.show()

    def startFirst(self):
        self.First = FirstWindow(self)
        self.setWindowTitle("FirstWindow")
        self.setGeometry(300, 300, 260, 150)
        self.setCentralWidget(self.First)
        self.First.btnconnect.clicked.connect(self.startSecond)
        self.First.btncreate.clicked.connect(self.startGamePrepare)
        self.show()

    def startThirdEx1(self):
        self.ThirdEx1 = ThirdWindowEx1(self)
        Form = QWidget()
        self.ThirdEx1.setupUi(Q)
        self.setWindowTitle("ThirdWindowEx1")
        self.setGeometry(self.widthtotal / 4, 30, self.widthtotal / 2, self.heighttotal)
        self.setCentralWidget(self.ThirdEx1)
        self.ThirdEx1.ButtonReturn.clicked.connect(self.startFirst)

        Form.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
