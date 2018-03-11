from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QMainWindow, QPushButton, QApplication, \
    QGroupBox, QMessageBox, QHBoxLayout

from client import *
from server import *


class Fishka(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.initUI()

    def initUI(self):
        self.MyLetter = ''
        self.MyPrice = 0
        self.MyKoord = [None, 0]
        self.MyStart = 0


class Communicate(QObject):
    redrawMe = pyqtSignal()
    redrawEnd = pyqtSignal()


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
        self.btnconcreateret.move(self.widthtotal - 120, 50)

        self.serv = GameServer([Player("BOT", "bot", 0.2), Player("Admin", "local")])
        self.serv.matrix.Mainmap[7][7] = "П"
        self.serv.matrix.Mainmap[7][8] = "Р"
        self.serv.matrix.Mainmap[7][9] = "И"
        self.serv.matrix.Mainmap[7][10] = "В"
        self.serv.matrix.Mainmap[7][11] = "Е"
        self.serv.matrix.Mainmap[7][12] = "Т"
        for player in range(len(self.serv.players)):
            if self.serv.players[player].name == "Admin":
                self.me = self.serv.players[player]
                # self.me.my_turn = self.my_hod
                break
        self.threadonstart = Thread(target=self._hoddaemon)
        self.threadonstart.start()
        self.progressed = Communicate()
        self.progressed.redrawMe.connect(self.my_hod)
        self.progressed.redrawEnd.connect(self.end_hod)
        self.newkoord = []
        self.newletters = []
        self.initUI()

    def initUI(self):
        """основная часть создания элементов формы"""
        # self.list = QListWidget()
        # self.list.setGeometry(self.ot, self.ot + self.libh + 20, self.libw - self.ot,2 * self.libh - self.ot - self.ot - 20)
        """Buttons"""
        self.btnconcreateret = QPushButton("назад", self)
        self.btnconcreateret.move(self.widthtotal - 120, 50)
        self.setAcceptDrops(True)

        # for i in range(5):
        #   self.serv.matrix.map[i + 3][7] = self.getletter()

        """расстановка кнопок для перемещения"""
        self.myletters = []
        self.StartPosition = []
        self.Pererisovka()

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
            if len(ch) == 3:
                self.ProverkaKoordinat(int(ch[0]), int(ch[1]), int(ch[2]))
        if name[0] == 'help' or name[0] == 'SOS':
            self.Help()
        if name[0] == 'clear':
            self.ClearChanges()
        if name[0] == 'lastletters':
            self.lastLetters()
        if name[0] == 'check':
            self.CheckMatrix()
        if name[0] == 'save':
            self.SeveChangesForm()
        if name[0] == 'endhod':
            self.EndMyHod()
        if name[0] == 'drop':
            self.Drop(name[1].split(','))
        self.konsol.clear()

    def lastLetters(self):
        """Расстановка кнопок, уже имеющихся в таблице"""
        self.ButMap = []
        for i in range(15):
            st = []
            for j in range(15):
                st.append(Fishka(self.serv.matrix.Mainmap[i][j], self))
            self.ButMap.append(st)
            for j in range(15):
                self.ButMap[i][j].setGeometry(self.karta[i][j][0], self.karta[i][j][1], self.yi, self.yi)
                self.ButMap[i][j].MyLetter = self.serv.matrix.Mainmap[i][j]
                if self.serv.matrix.Mainmap[i][j] != '':
                    self.ButMap[i][j].show()
                self.ButMap[i][j].MyKoord = [j, i]
                # self.ButMap[i][j].MyPrice = GameConfig.letters[self.ButMap[i][j].MyLetter]['price']

    def SeveChangesForm(self):
        points = []
        for p in range(len(self.newletters)):
            points.append(Point(self.newkoord[p][1], self.newkoord[p][0], self.newletters[p]))

        #self.me.accept_turn(TurnStruct(True, points))
        b = self.me.check_turn( points)
        if b.result:
            a = self.me.accept_turn(TurnStruct(True, points))
            if a.res:
                self.Message(a.msg)
                self.EndMyHod()
        elif b.score == 1:
            self.dobavlenie(b.wordsError)
        # if self.rez.result:
        #     self.serv.matrix.SaveChangesMatr()
        #     self.lastLetters()
        #     for i in self.myletters:
        #         if i.MyKoord[0] != None:
        #             i.MyKoord = [None, i.MyStart]
        #             i.move(self.StartPosition[i.MyStart][0], self.StartPosition[i.MyStart][1])
        #             gs = self.getletter()
        #             i.MyLetter = gs я занят
        #             i.MyPrice = GameConfig.letters[gs]['price']
        #             i.setText(gs + ' ' + str(i.MyStart))

    def ClearChanges(self):
        self.newletters = []
        self.newkoord = []
        for i in range(len(self.myletters)):
            self.myletters[i].MyKoord = [None, i]
            self.myletters[i].move(self.StartPosition[i][0], self.StartPosition[i][1])

    def EndMyHod(self):
        # TODO
        pass
        self.DisabledSet(True)
        # self.CheckMatrix()
        # self.SeveChangesForm()

    def Pererisovka(self):
        self.myletters.clear()
        for i in range(len(self.me.letters)):
            gs = self.me.letters[i]
            self.myletters.append(Fishka((gs + ' ' + str(i)), self))
            self.myletters[i].MyLetter = gs
            self.myletters[i].MyPrice = GameConfig.letters[gs]['price']
            self.myletters[i].MyKoord = [None, i]
            self.myletters[i].MyStart = i
            self.StartPosition.append(
                [self.letterskoord[0] + (self.yi + self.ot) * i + self.ot, self.letterskoord[1] + self.ot])
            self.myletters[i].setGeometry(
                QRect(self.letterskoord[0] + (self.yi + self.ot) * i + self.ot, self.letterskoord[1] + self.ot,
                      self.yi + 1,
                      self.yi + 1))
            self.myletters[i].show()

    def Help(self):
        s = ''
        print('переместить кнопку - move i,x,y (i - номер кнопки,(x, y) - координаты)')
        s += 'переместить кнопку - move i,x,y (i - номер кнопки,(x, y) - координаты)' + '\n'
        print('clear - очистить поле и временные данные')
        s += 'clear - очистить поле и временные данные' + '\n'
        print('lastletters - отрисовывает буквы, которые проверены')
        s += 'lastletters - отрисовывает буквы, которые проверены' + '\n'
        print('check - проверить матрицу и отобразить результат проверки')
        s += 'check - проверить матрицу и отобразить результат проверки' + '\n'
        print('save - сохраняет введенные данные и передает ход (при положительном результате функци check)')
        s += 'save - сохраняет введенные данные и передает ход (при положительном результате функци check)' + '\n'
        print('endhod - комбинация функций check и save')
        s += 'endhod - комбинация функций check и save' + '\n'
        self.Message(s)
        print(self.newletters)
        print(self.newkoord)
        for i in self.serv.matrix.Mainmap:
            print(i)

    def CheckMatrix(self):
        points = []
        for p in range(len(self.newletters)):
            points.append(Point(self.newkoord[p][1], self.newkoord[p][0], self.newletters[p]))
        self.rez = self.me.check_turn(points)
        if self.rez.result:
            # ошибок нет,
            print('ошибок нет')
            print('Найденные слова:')
            for i in self.rez.words:
                print(i)
            print('набранные баллы:')
            print(self.rez.score)
            self.Message("ошибок нет\n\nНайденные слова:\n" + " ".join(
                self.rez.words) + "\n\nнабранные баллы: " + str(self.rez.score))
        else:
            if self.rez.score == 1:
                # в матрице есть неопозанные слова
                self.dobavlenie(words)

            if self.rez.score == 2:
                # матрица заполнена неправильно
                print(self.rez.msg)
                self.Message(self.rez.msg)

    def getletter(self):
        """выбирает случайную букву"""
        random.seed()
        genletter = random.choice(GameConfig.let)
        while GameConfig.letters[genletter]['count'] < 0:
            genletter = random.choice(GameConfig.let)
        GameConfig.letters[genletter]['count'] -= 1
        return (genletter)

    def ProverkaKoordinat(self, i, x, y):
        r = [y, x]
        # проверяем, была ли занята эта ячейка до этого хода
        if self.serv.matrix.Mainmap[x][y] == '':
            # проверяем, откуда перетаскиваем букву, тк могут остаться хвосты
            if self.myletters[i].MyKoord[0] is not None:
                for j in range(len(self.newkoord)):
                    print(self.newkoord[j])
                    print(self.myletters[i].MyKoord)
                    if self.newkoord[j][0] == self.myletters[i].MyKoord[0]:
                        self.newkoord[j] = [None, None]
            # проверяем, ставили ли мы букву на новое место на этом ходу
            if r in self.newkoord:
                # да, ставили, освобождаем для нее место
                for j in range(len(self.myletters)):
                    # ищем какую букву сьавили
                    if self.myletters[j].MyKoord == r:
                        self.myletters[j].move(self.StartPosition[j][0], self.StartPosition[j][1])
                        self.myletters[j].MyKoord = [None, j]
                for j in range(len(self.newkoord)):
                    # ищем на какую позицию записана старая буква
                    if r == self.newkoord[j]:
                        self.newletters[j] = self.myletters[i].MyLetter
            else:
                self.newletters.append(self.myletters[i].MyLetter)
                self.newkoord.append([y, x])
            # перемещаем новую кнопкуна новое место
            self.myletters[i].move(self.karta[x][y][0], self.karta[x][y][1])
            self.myletters[i].MyKoord = [y, x]
        else:
            pass

    def dobavlenie(self, words):
        flag = 1
        # print(self.rez.msg)
        buttonReply = QMessageBox.question(self, 'Bad Words',
                                           "Вы хотите внести новые слова в словарь: " + " ".join(
                                               words),
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            for i in words:
                buttonReply1 = QMessageBox.question(self, 'Bad Words',
                                                    "Вы хотите внести это слово в словарь: " + i,
                                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply1 == QMessageBox.Yes:
                    self.serv.matrix.dict.append(i)
                else:
                    flag = 0
        if flag == 1:
            pass
            # self.CheckMatrix()

    def Message(self, text):
        buttonReply = QMessageBox.question(self, 'Scrabble',
                                           text,
                                           QMessageBox.Ok, QMessageBox.Ok)

    def Drop(self, dr):
        drlet = []
        for i in dr:
            drlet.append(self.myletters[int(i)].MyLetter)
        a = self.me.accept_turn(TurnStruct(False, drlet))
        if a.res:
            self.Message(a.msg)
            self.EndMyHod()

    def DisabledSet(self,t):
        #self.konsol.setDisabled(t)
        pass

    def my_hod(self):
        self.Message("твой ход!!!")
        # TODO andrsolo21 Перерисовку вызывай здес
        self.DisabledSet(False)
        self.lastLetters()
        self.Pererisovka()

    def end_hod(self):
        self.Message("Окончен ход")
        # TODO andrsolo21 Перерисовку вызывай здес
        self.lastLetters()
        self.Pererisovka()

    def _hoddaemon(self):
        while 1:
            if self.me.alertMe:
                self.progressed.redrawMe.emit()
                self.me.alertMe = False
                self.me.alertEnd = False
            if self.me.alertEnd:
                self.progressed.redrawEnd.emit()
                self.me.alertEnd = False
            time.sleep(1)

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
                self.karta[i][j] = [xp, yp]
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
        # self.setWindowTitle('Event sender')
        #
        # self.btnconcreate = QPushButton("Подключиться", self)
        self.btnBack = QPushButton("Вернуться назад", self)
        self.btnBack.move(400, 50)
        #
        # title = QLabel('Title')
        # title.setAlignment(Qt.AlignCenter)
        # title.setStyleSheet("QLabel {background-color: red;}")
        #
        # title2 = QLabel('Title2')
        # title2.setAlignment(Qt.AlignCenter)
        # title2.setStyleSheet("QLabel {background-color: yellow;}")
        #
        # self.grid = QGridLayout()
        # self.grid.setSpacing(8)
        #
        # self.grid.addWidget(title, 0, 0, 2, 3)
        # self.grid.addWidget(title2, 4, 0, 1, 3)
        #
        # self.grid.addWidget(self.btnfirst, 1, 4, 1, 1)
        # self.grid.addWidget(self.btnconcreate, 0, 4, 1, 1)
        #
        # self.setLayout(self.grid)
        self.setupUi(self)
        self.serverInit()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.groupBoxServers = QGroupBox(Form)
        self.groupBoxServers.setGeometry(QRect(10, 0, 291, 361))
        self.groupBoxServers.setObjectName("groupBoxServers")

        self.horizontalLayoutWidgets = []
        self.horizontalLayouts = []
        self.labels = []
        self.pushButtons = []
        for i in range(10):
            self.horizontalLayoutWidgets.append(QWidget(self.groupBoxServers))
            self.horizontalLayoutWidgets[-1].setGeometry(QRect(0, 20 + i * 30, 291, 21))
            self.horizontalLayoutWidgets[-1].setObjectName("horizontalLayoutWidget")
            self.horizontalLayouts.append(QHBoxLayout(self.horizontalLayoutWidgets[-1]))
            self.horizontalLayouts[-1].setContentsMargins(0, 0, 0, 0)
            self.horizontalLayouts[-1].setObjectName("horizontalLayout")
            self.labels.append(QLabel(self.horizontalLayoutWidgets[-1]))
            self.labels[-1].setText("Сервер такой то")
            self.horizontalLayouts[-1].addWidget(self.labels[-1])
            self.pushButtons.append(QPushButton(self.horizontalLayoutWidgets[-1]))
            self.pushButtons[-1].setMouseTracking(False)
            self.pushButtons[-1].setCheckable(False)
            self.pushButtons[-1].setEnabled(False)
            self.pushButtons[-1].setText("Подключиться")
            self.horizontalLayouts[-1].addWidget(self.pushButtons[-1])
            self.horizontalLayouts[-1].setStretch(0, 2)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBoxServers.setTitle(_translate("Form", "Сервера"))

    def connect_server(self):
        res = self.game.connect_server(self.sender().server_id)
        if not res.res:
            QMessageBox.question(self.sender(), 'Ошибка', res.msg, QMessageBox.Ok, QMessageBox.Ok)

    def redraw(self):
        i = 0
        while i < len(self.labels):
            if i < len(self.game.servers):
                self.labels[i].setText(self.game.servers[i]["id"] + " Игроков: " + str(
                    len(self.game.servers[i]["game"])) + ". Ожидание: " + str(len(self.game.servers[i]["queue"])))
                self.pushButtons[i].server_id = self.game.servers[i]["id"]
                self.pushButtons[i].clicked.connect(self.connect_server)
                self.pushButtons[i].setEnabled(True)
            else:
                self.labels[i].setText("")
                self.pushButtons[i].setEnabled(False)
            i += 1

    def serverInit(self):
        self.game = GameClientPrepare()
        self.game.callback = self.redraw


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
        # self.gamePrepare.game.start_game()
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
        self.setWindowTitle("Подключение к серверу")
        self.setGeometry(0, 30, self.widthtotal / 2, self.heighttotal / 2)
        self.setCentralWidget(self.Second)
        self.Second.btnBack.clicked.connect(self.startFirst)

        self.show()

    def startFirst(self):
        self.First = FirstWindow(self)
        self.setWindowTitle("FirstWindow")
        self.setGeometry(300, 300, 260, 150)
        self.setCentralWidget(self.First)
        self.First.btnconnect.clicked.connect(self.startSecond)
        self.First.btncreate.clicked.connect(self.startGamePrepare)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
