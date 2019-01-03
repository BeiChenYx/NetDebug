# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SingleSend.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(385, 281)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setMaximumSize(QtCore.QSize(95, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.checkBox_Hex = QtWidgets.QCheckBox(Form)
        self.checkBox_Hex.setObjectName("checkBox_Hex")
        self.horizontalLayout.addWidget(self.checkBox_Hex)
        self.checkBox_Times = QtWidgets.QCheckBox(Form)
        self.checkBox_Times.setObjectName("checkBox_Times")
        self.horizontalLayout.addWidget(self.checkBox_Times)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_Times = QtWidgets.QLineEdit(Form)
        self.lineEdit_Times.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_Times.setObjectName("lineEdit_Times")
        self.horizontalLayout.addWidget(self.lineEdit_Times)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "单条数据发送"))
        self.textEdit.setPlaceholderText(_translate("Form", "发送输入区"))
        self.pushButton.setText(_translate("Form", "发送"))
        self.checkBox_Hex.setText(_translate("Form", "Hex"))
        self.checkBox_Times.setText(_translate("Form", "循环发送"))
        self.label.setText(_translate("Form", "间隔"))
        self.label_2.setText(_translate("Form", "毫秒"))

