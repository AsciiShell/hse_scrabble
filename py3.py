# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '3.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(456, 575)
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 40, 441, 531))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setHorizontalSpacing(20)
        self.gridLayout_3.setVerticalSpacing(50)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_3.addWidget(self.pushButton_3, 0, 1, 1, 1)
        self.name2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.name2.setObjectName("name2")
        self.gridLayout_3.addWidget(self.name2, 1, 0, 1, 1)
        self.name1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.name1.setMouseTracking(False)
        self.name1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name1.setObjectName("name1")
        self.gridLayout_3.addWidget(self.name1, 0, 0, 1, 1)
        self.name4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.name4.setObjectName("name4")
        self.gridLayout_3.addWidget(self.name4, 3, 0, 1, 1)
        self.name3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.name3.setObjectName("name3")
        self.gridLayout_3.addWidget(self.name3, 2, 0, 1, 1)
        self.PushButton2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.PushButton2.setObjectName("PushButton2")
        self.gridLayout_3.addWidget(self.PushButton2, 1, 1, 1, 1)
        self.PushButton4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.PushButton4.setObjectName("PushButton4")
        self.gridLayout_3.addWidget(self.PushButton4, 3, 1, 1, 1)
        self.PushButton3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.PushButton3.setObjectName("PushButton3")
        self.gridLayout_3.addWidget(self.PushButton3, 2, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 1, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_5.addWidget(self.label_6, 2, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_5.addWidget(self.pushButton_7, 0, 1, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_5.addWidget(self.pushButton_8, 1, 1, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_5.addWidget(self.pushButton_9, 2, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_5, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 171, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(240, 10, 81, 23))
        self.pushButton.setObjectName("pushButton")
        self.ButtonReturn = QtWidgets.QPushButton(Form)
        self.ButtonReturn.setGeometry(QtCore.QRect(334, 10, 101, 23))
        self.ButtonReturn.setObjectName("ButtonReturn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
