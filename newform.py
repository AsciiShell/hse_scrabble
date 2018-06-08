import sys
import webbrowser

from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QPushButton, QApplication, \
    QMessageBox, QTextBrowser, QLabel

from server import *
from ui.start import Ui_Form as GameLauncher


class Fishka(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.initUI()

    def initUI(self):
        self.MyLetter = ''
        self.MyPrice = 0
        self.MyKoord = [None, 0]
        self.MyStart = 0


class DragButton(Fishka):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.initUI()
        self.size = SizeSettings()

    def getmass(self, mass, tempmass, dropmass):
        self.mass = mass
        self.tempmass = tempmass
        self.dropmass = dropmass

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)
            self.__mouseMovePos = globalPos

        super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            pos = self.RoundKoord(newPos.x(), newPos.y())
            newPos.setX(pos[0])
            newPos.setY(pos[1])
            self.move(newPos)
            moved = event.globalPos() - self.__mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        super(DragButton, self).mouseReleaseEvent(event)

    def RoundKoord(self, posx, posy):
        nkx = self.size.karta[0][0][0] // 1
        nky = self.size.karta[0][0][1] // 1
        x = int((posx - nkx + (self.size.yi / 2)) // round(self.size.yi + self.size.ot))
        y = int((posy - nky + (self.size.yi / 2)) // round(self.size.yi + self.size.ot))
        if self.MyKoord[0] != None and self.MyKoord[1] != None:
            self.tempmass.remove(self.MyKoord)
        if self.MyKoord[1] == None:
            self.dropmass.remove(self.MyStart)
        if (x < 15) and (x >= 0) and (y < 15) and (y >= 0) and self.mass[y][x] == '' and (
                [y, x] not in self.tempmass and self.dropmass == []):
            self.MyKoord = [y, x]
            self.tempmass.append([y, x])
            return self.size.karta[y][x][0], self.size.karta[y][x][1]
        else:
            if (posx + (self.size.yi / 2) > self.size.letterskoord[0] + 15 * (
                    self.size.ot + self.size.yi) - self.size.ot - self.size.dropx - self.size.ot + 1) and (
                    posx + (self.size.yi / 2) < self.size.letterskoord[0] + 15 * (
                    self.size.ot + self.size.yi) - self.size.ot - self.size.dropx - self.size.ot + 1 + self.size.dropx) and (
                    posy + (self.size.yi / 2) > self.size.letterskoord[1] + self.size.ot + 1) and (
                    posy + (self.size.yi / 2) < self.size.letterskoord[
                1] + self.size.ot + 1 + self.size.dropy) and self.tempmass == []:
                self.MyKoord = [self.MyStart, None]
                self.dropmass.append(self.MyStart)
                return posx, posy
            self.MyKoord = [None, self.MyStart]
            return self.size.StartPosition[self.MyStart][0], self.size.StartPosition[self.MyStart][1]


class Communicate(QObject):
    redrawMe = pyqtSignal()
    redrawEnd = pyqtSignal()
    redrawGameEnd = pyqtSignal()


class SizeSettings:
    def __init__(self):
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
        self.karta = [0] * 15
        self.dropx = 150
        self.dropy = 100
        for i in range(15):
            self.karta[i] = [0] * 15
        for i in range(15):
            for j in range(15):
                xp = self.libw + j * (self.ot + self.yi) + self.ot
                yp = self.ot + i * (self.ot + self.yi)
                self.karta[i][j] = [xp, yp]
        self.StartPosition = []
        for i in range(20):
            self.StartPosition.append(
                [self.letterskoord[0] + (self.yi + self.ot) * i + self.ot, self.letterskoord[1] + self.ot])


class wrinfo():
    def __init__(self, Form, Num, hard, name):
        self.size = SizeSettings()
        self.nameH = 40
        self.timeH = 50
        self.ot = 10
        self.scoreH = 30
        self.hardH = 15
        # Num 1 or 2 or 3 -> Bot; Num == 0 -> player
        s = name
        if Num == 0:
            self.y = int(self.size.ot)
            self.x = int(self.size.ot)
        else:
            self.y = int(self.size.widthtotal * (1 - self.size.k2) + self.size.ot)
            self.x = int(self.size.ot + self.size.libh * (Num - 1))

            self.hard = QLabel("сложность: " + str(hard), Form)
            self.hard.move(self.y + 30, self.x + self.size.libh - self.hardH - self.size.ot - 3 * self.ot)
            self.hard.setFont(QFont("Times", self.hardH))
            self.hard.setMinimumSize(self.size.libw - self.size.ot * 10, self.hardH + self.ot)
            self.hard.setAlignment(Qt.AlignRight)

        self.name = QLabel(s, Form)
        self.name.move(self.y, self.x)
        self.name.setFont(QFont("Times", self.nameH))
        self.name.setMinimumSize(self.size.libw - self.size.ot - self.size.ot, self.nameH + self.ot + 10)
        self.name.setAlignment(Qt.AlignCenter)

        self.time = QLabel("00:00", Form)
        self.time.move(self.y, self.x + int(self.size.libh / 3))
        self.time.setFont(QFont("Times", self.timeH))
        self.time.setMinimumSize(self.size.libw - self.size.ot - self.size.ot, self.timeH + self.ot)
        self.time.setAlignment(Qt.AlignCenter)

        self.score = QLabel("счет: " + str(0), Form)
        self.score.move(self.y + 30, self.x + self.size.libh - self.scoreH - self.size.ot - 3 * self.ot)
        self.score.setFont(QFont("Times", self.scoreH))
        self.score.setMinimumSize(self.size.libw - self.size.ot - self.size.ot, self.scoreH + self.ot)
        self.score.setAlignment(Qt.AlignLeft)

    def setScore(self, score):
        """устанавливает счет
        на вход подаются баллы"""
        self.score.setText("счет:" + str(score))

    def setTime(self, time):
        """устанавливает время
        на вход подаются секунды"""
        min = time // 60
        sek = time % 60
        self.time.setText(str(min) + ":" + str(sek))

    def VisTime(self, flag):
        """устанавливает видимость таймера"""
        self.time.setVisible(flag)


class helpwin():
    def __init__(self):
        pass


class GameForm(object):
    def setupUi(self, Form):
        """основная часть создания элементов формы"""
        # self.list = QListWidget()
        # self.list.setGeometry(self.ot, self.ot + self.libh + 20, self.libw - self.ot,2 * self.libh - self.ot - self.ot - 20)
        """Buttons"""
        self.setAcceptDrops(True)

        self.burttoncollect = QPushButton("Clear", self)
        self.burttoncollect.clicked.connect(self.ClearChanges)
        self.burttoncollect.setGeometry(450, 600, 51, 50)

        self.burttonsave = QPushButton("Save\nChanges", self)
        self.burttonsave.clicked.connect(self.SeveChangesForm)
        self.burttonsave.setGeometry(550, 600, 50, 50)

        self.burttoncheck = QPushButton("Check", self)
        self.burttoncheck.clicked.connect(self.CheckMatrix)
        self.burttoncheck.setGeometry(650, 600, 50, 50)

        # self.burttoncheck = QPushButton("help", self)
        # self.burttoncheck.clicked.connect(self.HelpForm)
        # self.burttoncheck.setGeometry(700, 600, 30, 30)

        self.burttondrop = QPushButton("drop", self)
        self.burttondrop.clicked.connect(self.Drop)
        self.burttondrop.setGeometry(self.letterskoord[0] + 15 * (self.ot + self.yi) - self.ot - self.dropx - self.ot,
                                     self.letterskoord[1] + self.ot + self.dropy,
                                     self.dropx,
                                     self.heighttotal - 15 * (self.ot + self.yi) - 2 * self.ot - self.dropy - 1)

        """расстановка кнопок для перемещения"""
        self.myletters = []
        self.StartPosition = []
        self.Pererisovka()

        """line edit/konsol"""
        # self.konsol = QLineEdit(self)
        # self.konsol.setGeometry(self.ot, self.ot + self.libh, self.libw - self.ot, 20)
        # self.konsol.returnPressed.connect(self.enter)

        """Logs"""
        self.logs = QTextBrowser(self)
        self.logs.setGeometry(self.ot, self.ot + self.libh, self.libw - self.ot, 2 * self.libh - self.ot - self.ot)
        self.logs.setFontPointSize(10)


class GameApp(QMainWindow, GameForm):
    def __init__(self, parent=None):
        super(GameApp, self).__init__(parent)
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

        self.setWindowTitle("GameCreate")
        self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
        # self.setCentralWidget(self.GameCreate)

        self.size = SizeSettings()
        self.koef = self.size.koef
        self.pos = self.size.pos
        self.k2 = self.size.k2
        self.widthtotal = self.size.widthtotal
        self.heighttotal = self.size.heighttotal
        self.ot = self.size.ot
        self.libw = self.size.libw
        self.libh = self.size.libh
        self.yi = self.size.yi
        self.letterskoord = self.size.letterskoord
        self.dropaccept = 1
        self.dropx = self.size.dropx
        self.dropy = self.size.dropy
        """инициализация окна"""
        self.serv = GameServer()
        self.me = None

        self.threadonstart = Thread(target=self._hoddaemon)
        self.progressed = Communicate()
        self.progressed.redrawMe.connect(self.my_hod)
        self.progressed.redrawEnd.connect(self.end_hod)
        self.progressed.redrawGameEnd.connect(self.end_game)
        self.newkoord = []
        self.newletters = []

    def run(self):
        for player in range(len(self.serv.players)):
            if type(self.serv.players[player]) == PlayerLocal:
                self.me = self.serv.players[player]
                # self.me.my_turn = self.my_hod
                break

        self.InitBots()
        self.serv.run_game()
        self.threadonstart.start()
        self.setupUi(self)

    def InitBots(self):
        num = 0
        for i in self.serv.players:
            i.info = wrinfo(self, num, i.diff, i.name)
            num += 1

    def HelpForm(self):
        self.selfHelp = helpwin()

    def CollectLetters(self):
        out = []
        for i in self.myletters:
            if i.MyKoord[0] != None:
                out.append([i.MyKoord[0], i.MyKoord[1], i.MyLetter])

        return out

    def lastLetters(self):
        """Расстановка кнопок, уже имеющихся в таблице"""
        self.ButMap = []
        for i in range(15):
            st = []
            for j in range(15):
                st.append(QPushButton(self.serv.matrix.Mainmap[i][j], self))
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
        out = self.CollectLetters()
        for p in range(len(out)):
            points.append(Point(out[p][0], out[p][1], out[p][2]))

        # self.me.accept_turn(TurnStruct(True, points))
        b = self.me.check_turn(points)
        if b.result:
            a = self.me.accept_turn(TurnStruct(True, points))
            if a.res:
                self.EndMyHod()
                self.add_to_console("Счет за ход: " + a.msg)

        elif b.score == 1:
            self.dobavlenie(b.wordsError)
        else:
            self.Message(b.msg)
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
        self.dropmass = []
        self.tempmap = []
        self.acceptdrop = [0]
        for i in range(len(self.myletters)):
            self.myletters[i].MyKoord = [None, i]
            self.myletters[i].move(self.StartPosition[i][0], self.StartPosition[i][1])
            self.myletters[i].getmass(self.serv.matrix.Mainmap, self.tempmap, self.dropmass)

    def EndMyHod(self):
        # TODO
        pass
        self.DisabledSet(True)
        # self.CheckMatrix()
        # self.SeveChangesForm()

    def Pererisovka(self):
        for i in self.myletters:
            i.deleteLater()
        self.myletters.clear()
        self.tempmap = []
        self.dropmass = []
        self.acceptdrop = [0]
        for i in range(len(self.me.letters)):
            gs = self.me.letters[i]
            self.myletters.append(DragButton(gs, self))
            self.myletters[i].MyLetter = gs
            self.myletters[i].MyPrice = GameConfig.letters[gs]['price']
            self.myletters[i].MyKoord = [None, i]
            self.myletters[i].MyStart = i
            self.myletters[i].getmass(self.serv.matrix.Mainmap, self.tempmap, self.dropmass)
            self.StartPosition.append(
                [self.letterskoord[0] + (self.yi + self.ot) * i + self.ot, self.letterskoord[1] + self.ot])
            self.myletters[i].setGeometry(
                QRect(self.letterskoord[0] + (self.yi + self.ot) * i + self.ot, self.letterskoord[1] + self.ot,
                      self.yi + 1,
                      self.yi + 1))
            self.myletters[i].show()

    def CheckMatrix(self):
        points = []
        out = self.CollectLetters()
        for p in range(len(out)):
            points.append(Point(out[p][0], out[p][1], out[p][2]))
        self.rez = self.me.check_turn(points)
        if self.rez.result:
            # ошибок нет,
            # print('ошибок нет')
            # print('Найденные слова:')
            # for i in self.rez.words:
            #     print(i)
            # print('набранные баллы:')
            # print(self.rez.score)
            self.Message("ошибок нет\n\nНайденные слова:\n" + " ".join(
                self.rez.words) + "\n\nнабранные баллы: " + str(self.rez.score))
        else:
            if self.rez.score == 1:
                # в матрице есть неопозанные слова
                # self.dobavlenie(words)
                self.Message("Ошибка\n\nНе найденные слова:\n" + " ".join(
                    self.rez.wordsError))

            if self.rez.score == 2:
                # матрица заполнена неправильно
                # print(self.rez.msg)
                self.Message(self.rez.msg)
            if self.rez.score == 3:
                # Дубликат
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
        QMessageBox.question(self, 'Scrabble', text, QMessageBox.Ok, QMessageBox.Ok)

    def Drop(self):
        if self.dropmass != []:
            drlet = []
            for i in self.dropmass:
                drlet.append(self.myletters[int(i)].MyLetter)
            a = self.me.accept_turn(TurnStruct(False, drlet))
            if a.res:
                self.add_to_console(a.msg)
                self.EndMyHod()

    def DisabledSet(self, t):
        # self.konsol.setDisabled(t)
        pass

    def my_hod(self):
        self.add_to_console("Ваш ход!")
        self.DisabledSet(False)
        self.lastLetters()
        self.Pererisovka()

    def end_hod(self):
        self.add_to_console("Окончен ход")
        self.lastLetters()
        self.Pererisovka()

    def end_game(self):
        self.add_to_console("Игра закончена")
        self.lastLetters()
        self.Pererisovka()

    def add_to_console(self, text, score=False):
        text += "\n"
        if score:
            for pl in self.serv.players:
                text += pl.name + ": " + str(pl.score) + "\n"
        self.logs.setText(text + "\n" + self.logs.toPlainText())

    def _hoddaemon(self):
        last_tick = -1
        while self.serv.playStatus:
            if last_tick != self.serv.playerIndex:
                last_tick = self.serv.playerIndex
                for i in self.serv.players:
                    i.info.VisTime(False)
                    i.info.setScore(i.score)

            if self.me.alertMe:
                self.progressed.redrawMe.emit()
                self.me.alertMe = False
                self.me.alertEnd = False
            if self.me.alertEnd:
                self.progressed.redrawEnd.emit()
                self.me.alertEnd = False

            self.serv.players[self.serv.playerIndex].info.VisTime(True)
            self.serv.players[self.serv.playerIndex].info.setTime(self.serv.players[self.serv.playerIndex].timeout)
            time.sleep(0.5)
        for i in self.serv.players:
            i.info.VisTime(False)
            i.info.setScore(i.score)
        self.progressed.redrawGameEnd.emit()
        # self.add_to_console("Игра окончена")

    def paintEvent(self, e):
        # Мб приклеить на другое событие?
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
        # Drop place
        background.setBrush(QColor(255, 0, 0))
        background.drawRect(self.letterskoord[0] + 15 * (self.ot + self.yi) - self.ot - self.dropx - self.ot - 1,
                            self.letterskoord[1] + self.ot - 1, self.dropx + 1,
                            self.dropy + 1 + self.heighttotal - 15 * (self.ot + self.yi) - 2 * self.ot - self.dropy - 1)
        background.setBrush(QColor(200, 200, 200))
        background.drawRect(self.letterskoord[0] + 15 * (self.ot + self.yi) - self.ot - self.dropx - self.ot + 1,
                            self.letterskoord[1] + self.ot + 1, self.dropx - 3, self.dropy)
        # 15 * (self.ot + self.yi) - self.ot,
        # self.heighttotal - 15 * (self.ot + self.yi) - 2 * self.ot)

        """for i in range(15):
            for j in range(15):
                background.setPen(QColor(255, 255, 255))
                background.setFont(QFont('Decorative', 10))
                background.drawText(self.karta[i][j][0][0],self.karta[i][j][1][0], self.yi,self.yi,Qt.AlignCenter, Point.info[GameConfig.map[i][j]]['multi'])"""

    def closeEvent(self, event):
        if QMessageBox.question(self, 'Предупреждение', "Закрыть игру?", QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No) == QMessageBox.Yes:
            self.serv.playStatus = False
            self.serv.thread.join(0)
            for p in self.serv.players:
                if p.type == "bot":
                    p.botEnable = False
                    p.thread.join(0)
            event.accept()
        else:
            event.ignore()


class StartApp(QMainWindow, GameLauncher):
    def __init__(self, parent=None):
        super(StartApp, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run_game)

    def run_game(self):
        if (not self.checkBox_1.checkState() or self.validate_float(self.lineEdit_1.text())) and \
                (not self.checkBox_2.checkState() or self.validate_float(self.lineEdit_2.text())) and (
                not self.checkBox_3.checkState() or self.validate_float(self.lineEdit_3.text())) and \
                self.validate_int(self.lineEdit_Start.text(), 1, 9) and \
                self.validate_int(self.lineEdit_time.text(), 10, 600):
            if self.checkBox_Multi.checkState():
                if self.lineEdit_Multi.text() != "" and not self.checkBox_3.checkState():
                    GameConfig.startCount = int(self.lineEdit_Start.text())
                    GameConfig.turnTime = int(self.lineEdit_time.text())
                    self.game = GameApp(self)
                    self.game.serv.add_player(Player(self.lineEdit_Name.text(), "local"))
                    if self.checkBox_1.checkState():
                        self.game.serv.add_player(Player("BOT1", "bot", diff=float(self.lineEdit_1.text())))
                    if self.checkBox_2.checkState():
                        self.game.serv.add_player(Player("BOT2", "bot", diff=float(self.lineEdit_2.text())))
                    if self.checkBox_3.checkState():
                        self.game.serv.add_player(Player("BOT3", "bot", diff=float(self.lineEdit_3.text())))
                    webbrowser.get().open("https://money.yandex.ru/to/410015332771446", new=2)

                    self.game2 = GameApp(self)
                    self.game2.serv = self.game.serv
                    self.game.serv.add_player(Player(self.lineEdit_Multi.text(), "local"))
                    self.game.run()
                    self.game2.me = self.game.serv.players[-1]
                    self.game2.threadonstart.start()
                    self.game2.setupUi(self.game2)

                    self.game.show()
                    self.game2.show()
                    self.game.add_to_console("Поддержать проект\nhttps://money.yandex.ru/to/410015332771446")
                    self.game2.add_to_console("Поддержать проект\nhttps://money.yandex.ru/to/410015332771446")

            else:
                GameConfig.startCount = int(self.lineEdit_Start.text())
                GameConfig.turnTime = int(self.lineEdit_time.text())
                self.game = GameApp(self)
                self.game.serv.add_player(Player(self.lineEdit_Name.text(), "local"))
                if self.checkBox_1.checkState():
                    self.game.serv.add_player(Player("BOT1", "bot", diff=float(self.lineEdit_1.text())))
                if self.checkBox_2.checkState():
                    self.game.serv.add_player(Player("BOT2", "bot", diff=float(self.lineEdit_2.text())))
                if self.checkBox_3.checkState():
                    self.game.serv.add_player(Player("BOT3", "bot", diff=float(self.lineEdit_3.text())))
                self.game.run()
                self.game.show()

    @staticmethod
    def validate_float(text):
        try:
            return 0 < float(text) <= 1
        except ValueError:
            return False

    @staticmethod
    def validate_int(i, a, b):
        try:
            return a <= int(i) <= b
        except ValueError:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = StartApp()
    form.show()
    app.exec_()
