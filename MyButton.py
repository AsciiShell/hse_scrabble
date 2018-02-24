"""
from forms1 import *
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel,QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from server import *


class fishka(QPushButton):
    def GivePrice(self):
        self.let = self.text()
        self.price = GameConfig.letters[self.text()]
        self.setBut = ScreenSet()
        self.pr = QLabel(self)
        self.pr.setFont(QFont(self.price, 4, QFont.Bold))
        self.resize(self.setBut.yi, self.setBut.yi)
        self.pr.setGeometry(0, self.setBut.yi / 3,self.setBut.yi, self.setBut.yi)




class win(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.button = fishka("А",self)
        self.button.GivePrice()
        self.setGeometry(0, 30,500, 500)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = win()
    sys.exit(app.exec_())

import sys
import time
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication
from PyQt5.QtCore import Qt, QMimeData, pyqtSlot
from PyQt5.QtGui import QDrag,QCursor

class Button(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)


    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)


    def mousePressEvent(self, e):

        QPushButton.mousePressEvent(self, e)

        if e.button() == Qt.LeftButton:
            print('press')


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.pres = [0,0]


    def initUI(self):

        self.setAcceptDrops(True)

        self.button = QPushButton('Button', self)
        self.button.move(100, 65)
        self.button.clicked.connect()

        self.button2 = QPushButton('Button2', self)
        self.button2.move(200, 65)
        self.button2.clicked.connect()

        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 300, 280, 150)
        #self.draganddrop()

    def draganddrop(self):
        while 1:
            time.sleep(0.1)
            if self.button2.isChecked():
                self.button2.move(QCursor.pos())



    def dragEnterEvent(self, e):

        e.accept()


    def dropEvent(self, e):

        position = e.pos()
        if self.pres[0] == 1:
            self.button.move(position)
            self.pres[0] =0
        if self.pres[1] == 1:
            self.button2.move(position)
            self.pres[1] =0

        e.setDropAction(Qt.MoveAction)
        e.accept()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 30
        self.top = 30
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This is an example button')
        button.move(100,70)
        button.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())"""
from PyQt5 import QtWidgets
import sys

def click():
    label.setText(lineEdit.text())

app = QtWidgets.QApplication(sys.argv)

window = QtWidgets.QWidget()
window.setWindowTitle("Enter")
window.resize(300, 70)

label = QtWidgets.QLabel("Результат")

lineEdit = QtWidgets.QLineEdit()
lineEdit.returnPressed.connect(click)

vbox = QtWidgets.QVBoxLayout()
vbox.addWidget(label)
vbox.addWidget(lineEdit)
window.setLayout(vbox)

window.show()
sys.exit(app.exec())