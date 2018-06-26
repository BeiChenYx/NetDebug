# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_help(object):
    def setupUi(self, help):
        help.setObjectName("help")
        help.resize(594, 465)
        self.gridLayout = QtWidgets.QGridLayout(help)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(help)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.retranslateUi(help)
        QtCore.QMetaObject.connectSlotsByName(help)

    def retranslateUi(self, help):
        _translate = QtCore.QCoreApplication.translate
        help.setWindowTitle(_translate("help", "Form"))

