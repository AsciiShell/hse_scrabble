import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QGridLayout, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QHBoxLayout, QFrame, QSplitter, QStyleFactory, QApplication, QMainWindow, QPushButton, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon, QBrush
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QCoreApplication
from server import *


class FirstWindow(QWidget):
    def __init__(self, parent=None):
        super(FirstWindow, self).__init__(parent)
        self.btncreate = QPushButton("Create game", self)
        self.btncreate.move(30, 50)

        self.btnconnect = QPushButton("Connect game", self)
        self.btnconnect.move(150, 50)

        self.setGeometry(300, 300, 290, 150)
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
        self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
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


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 400, 450)

        self.startSecond()

    def startSecond(self):
        self.ToolTab = SecondWindow(self)
        self.setWindowTitle("UIToolTab")
        self.setCentralWidget(self.ToolTab)
        self.ToolTab.btnfirst.clicked.connect(self.startFirst)
        self.show()

    def startFirst(self):
        self.Window = FirstWindow(self)
        self.setWindowTitle("UIWindow")
        self.setCentralWidget(self.Window)
        self.Window.btnconnect.clicked.connect(self.startSecond)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())