# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'customerBar.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(480, 296)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.toolButton_Min = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_Min.setObjectName("toolButton_Min")
        self.horizontalLayout.addWidget(self.toolButton_Min)
        self.toolButton_Max = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_Max.setObjectName("toolButton_Max")
        self.horizontalLayout.addWidget(self.toolButton_Max)
        self.toolButton_Close = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_Close.setObjectName("toolButton_Close")
        self.horizontalLayout.addWidget(self.toolButton_Close)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 249, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolButton_Min.setText(_translate("MainWindow", "最小化"))
        self.toolButton_Max.setText(_translate("MainWindow", "最大化"))
        self.toolButton_Close.setText(_translate("MainWindow", "关闭"))

