import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QGridLayout, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QHBoxLayout, QFrame, QSplitter, QStyleFactory, QApplication, QMainWindow, QPushButton, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon, QBrush
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QCoreApplication
from server import *

class FirstWindow(object):
    def setupUI(self, MainWindow):
        MainWindow.setGeometry(300, 300, 290, 150)

        MainWindow.setWindowTitle("FirstWindow")
        self.centralwidget = QWidget(MainWindow)
        # mainwindow.setWindowIcon(QtGui.QIcon('PhotoIcon.png'))
        #self.ToolsBTN = QPushButton('text', self.centralwidget)
        #self.ToolsBTN.move(50, 350)
        self.btncreate = QPushButton("Create game", self.centralwidget)
        self.btncreate.move(30, 50)
        self.btnConnect = QPushButton("Connect game", self.centralwidget)
        self.btnConnect.move(150, 50)
        MainWindow.setCentralWidget(self.centralwidget)


class SecondWindow(object):
    def setupUI(self, MainWindow):
        self.koef = 0.8
        self.k2 = 0.3
        self.widthtotal = self.koef * QDesktopWidget().availableGeometry().width() * 0.5
        self.heighttotal = self.koef * QDesktopWidget().availableGeometry().height() - 30
        self.ot = QDesktopWidget().availableGeometry().width() / 100
        self.libw = self.widthtotal * self.k2
        self.libh = self.heighttotal / 3
        self.yi = self.widthtotal * (1 - 2 * self.k2) / 15 - self.ot
        """инициализация окна"""

        MainWindow.setGeometry(300, 300, self.widthtotal, self.heighttotal)
        MainWindow.setWindowTitle("Подключение к игрэ")
        self.centralwidget = QWidget(MainWindow)

        MainWindow.setCentralWidget(self.centralwidget)

        self.btnConCreate = QPushButton("Подключиться", self.centralwidget)
        self.btnFirst = QPushButton("Вернуться назад", self.centralwidget)

        self.title = QLabel('Title')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("QLabel {background-color: red;}")
        self.status = QLineEdit('')
        self.title2 = QLabel('Title2')
        self.title2.setAlignment(Qt.AlignCenter)
        self.title2.setStyleSheet("QLabel {background-color: yellow;}")

        self.grid = QGridLayout()
        self.grid.setSpacing(8)



        self.grid.addWidget(self.title, 0, 0, 2, 3)
        self.grid.addWidget(self.title2, 4, 0, 1, 3)
        self.grid.addWidget(self.status, 2, 0, 1, 3)

        self.grid.addWidget(self.btnFirst, 1, 4, 1, 1)
        self.grid.addWidget(self.btnConCreate, 0, 4, 1, 1)
        MainWindow.setLayout(self.grid)
        MainWindow.setCentralWidget(self.centralwidget)

class Window(object):
    def setupUI(self, MainWindow):
        MainWindow.setGeometry(300, 300, 290, 150)

        MainWindow.setWindowTitle("FirsfghjtWindow")
        self.centralwidget = QWidget(MainWindow)
        # mainwindow.setWindowIcon(QtGui.QIcon('PhotoIcon.png'))
        #self.ToolsBTN = QPushButton('text', self.centralwidget)
        #self.ToolsBTN.move(50, 350)
        self.btncreate = QPushButton("Create game", self.centralwidget)
        self.btncreate.move(30, 50)
        self.btnConnect = QPushButton("Connect game", self.centralwidget)
        self.btnConnect.move(150, 50)
        MainWindow.setCentralWidget(self.centralwidget)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.uiFirst = FirstWindow()
        self.uiSecond = SecondWindow()
        self.uiSecond = Window()
        self.startFirstWindow()
        #self.startSecondWindow()

    def startSecondWindow(self):
        self.uiSecond.setupUI(self)
        self.uiSecond.btnFirst.clicked.connect(self.startFirstWindow)
        self.show()

    def startFirstWindow(self):
        self.uiFirst.setupUI(self)
        self.uiFirst.btnConnect.clicked.connect(self.startSecondWindow)
        self.show()

    def startWindow(self):
        self.uiSecond.setupUI(self)
        self.uiSecond.btnConCreate.clicked.connect(self.startFirstWindow)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())