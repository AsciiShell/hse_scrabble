# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget,QDesktopWidget, QPushButton,QHBoxLayout, QFrame,QSplitter, QStyleFactory, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon, QBrush
from PyQt5.QtCore import Qt


class painter(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        """инициализация окна"""
        #создаем окно
        self.koef = 1
        self.k2 = 0.3
        self.widthtotal = self.koef * QDesktopWidget().availableGeometry().width()
        self.heighttotal = self.koef * QDesktopWidget().availableGeometry().height() - 30
        self.ot = QDesktopWidget().availableGeometry().width() / 300
        self.libw = self.widthtotal * self.k2
        self.libh = self.heighttotal / 3
        self.yi = self.widthtotal * (1 - 2* self.k2) / 15 - self.ot
        self.setGeometry(0, 30, self.widthtotal, self.heighttotal)
               
        #self.square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())
        #self.setWindowTitle('Icon')
        #self.setWindowIcon(QIcon('web.png'))
        #QToolTip.setFont(QFont('SansSerif', 10))

        self.show()
    def paintEvent(self, e):
        background = QPainter()
        background.begin(self)
        self.drawBackground(background)
        background.end()
        
    def drawBackground(self, background):
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        background.setPen(col)
        #background
        background.setBrush(QColor(220, 220, 220))
        background.drawRect(0, 0, self.widthtotal * 5, self.heighttotal * 5)
        #iam
        background.setBrush(QColor(255, 255, 255))
        background.drawRect(self.ot,self.ot,self.libw - self.ot,self.libh - self.ot)
        #matrix
        for i in range(15):
            for j in range(15):
                background.drawRect(self.libw + j * (self.ot + self.yi) + self.ot ,self.ot + i * (self.ot + self.yi),self.yi , self.yi )
        #history
        background.drawRect(self.ot,self.ot + self.libh,self.libw - self.ot,2 * self.libh - self.ot - self.ot)
        #letters
        background.drawRect(self.libw + self.ot,15 * (self.ot + self.yi) + self.ot,15 * (self.ot + self.yi) - self.ot,self.heighttotal - 15 * (self.ot + self.yi) - 2* self.ot)
        #p1
        background.drawRect(self.widthtotal * (1 - self.k2) + self.ot,self.ot,self.libw - self.ot- self.ot,self.libh - self.ot)
        #p2
        background.drawRect(self.widthtotal * (1 - self.k2) + self.ot,self.ot + self.libh,self.libw - self.ot- self.ot,self.libh - self.ot)
        #p3
        background.drawRect(self.widthtotal * (1 - self.k2) + self.ot,self.ot + self.libh * 2,self.libw - self.ot- self.ot,self.libh - self.ot - self.ot)   
       
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = painter()
    sys.exit(app.exec_())
