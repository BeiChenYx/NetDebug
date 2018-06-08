# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\SingleSend.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(385, 281)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_2.addWidget(self.textEdit)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setMinimumSize(QtCore.QSize(120, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(120, 1000))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setMaximumSize(QtCore.QSize(95, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.checkBox_Hex = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_Hex.setObjectName("checkBox_Hex")
        self.verticalLayout.addWidget(self.checkBox_Hex)
        self.checkBox_Times = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_Times.setObjectName("checkBox_Times")
        self.verticalLayout.addWidget(self.checkBox_Times)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_Times = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_Times.setObjectName("lineEdit_Times")
        self.horizontalLayout.addWidget(self.lineEdit_Times)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(20, 151, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "单条数据发送"))
        self.pushButton.setText(_translate("Form", "发送"))
        self.checkBox_Hex.setText(_translate("Form", "十六进制发送"))
        self.checkBox_Times.setText(_translate("Form", "循环发送"))
        self.label.setText(_translate("Form", "间隔"))
        self.label_2.setText(_translate("Form", "毫秒"))

