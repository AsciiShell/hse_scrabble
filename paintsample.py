import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QGridLayout, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QHBoxLayout, QFrame, QSplitter, QStyleFactory, QApplication, QMainWindow, QPushButton, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon, QBrush
from PyQt5.QtCore import *
from server import *

class GameWindow(QWidget):

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

class ScreenSet():
    def __init__(self):
        self.koef = 0.8
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
        self.btnFirst = QPushButton("Вернуться назад", self)
        """hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.btnconnect)
        hbox.addWidget(self.btncreate)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)"""
        #self.setLayout(vbox)

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

        self.startThirdCreate()
    def startThirdCreate(self):
        self.ThirdCreate = ThirdWindowCreate(self)
        self.setWindowTitle("ThirdWindowCreate")
        self.setGeometry(self.widthtotal / 4, 30, self.widthtotal / 2, self.heighttotal)
        self.setCentralWidget(self.ThirdCreate)

        self.ThirdCreate.btnFirst.clicked.connect(self.startFirst)
        self.show()

    def startSecond(self):
        self.Second = SecondWindow(self)
        self.setWindowTitle("SecondWindow")
        self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
        self.setCentralWidget(self.Second)
        self.Second.btnfirst.clicked.connect(self.startFirst)
        self.Second.btnconcreate.clicked.connect(self.startThirdEx1)

        self.show()

    def startFirst(self):
        self.First = FirstWindow(self)
        self.setWindowTitle("FirstWindow")
        self.setGeometry(300, 300, 260, 150)
        self.setCentralWidget(self.First)
        self.First.btnconnect.clicked.connect(self.startSecond)
        self.First.btncreate.clicked.connect(self.startThirdCreate)
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