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
        MainWindow.resize(526, 405)
        MainWindow.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        MainWindow.setAcceptDrops(True)
        MainWindow.setStyleSheet("padding: 5px;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.myBar = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.myBar.sizePolicy().hasHeightForWidth())
        self.myBar.setSizePolicy(sizePolicy)
        self.myBar.setStyleSheet("/*最小化按钮*/\n"
"QPushButton#ButtonMin\n"
"{\n"
"    border-image:url(:/Resources/MyTitle/min.png) 0 81 0 0 ;\n"
"}\n"
"\n"
"QPushButton#ButtonMin:hover\n"
"{\n"
"    border-image:url(:/Resources/MyTitle/min.png) 0 54 0 27 ;\n"
"}\n"
"\n"
"QPushButton#ButtonMin:pressed\n"
"{\n"
"    border-image:url(:/Resources/MyTitle/min.png) 0 27 0 54 ;\n"
"}\n"
"\n"
"/*最大化按钮*/\n"
"QPushButton#ButtonMax\n"
"{\n"
"    border-image:url(:/Resources/MyTitle/max.png) 0 81 0 0 ;\n"
"}\n"
"\n"
"QPushButton#ButtonMax:hover\n"
"{\n"
"    border-image:url(:/Resources/MyTitle/max.png) 0 54 0 27 ;\n"
"}\n"
"\n"
"QPushButton#ButtonMax:pressed\n"
"{\n"
"    border-image:url(:/Resources/MyTitle/max.png) 0 27 0 54 ;\n"
"}\n"
"\n"
"/*还原按钮*/\n"
"QPushButton#ButtonRestore\n"
"{\n"
"    border-image:url(:/Resources/MyTitle/restore.png) 0 81 0 0 ;\n"
"}\n"
"\n"
"QPushButton#ButtonRestore:hover\n"
"{\n"
"    border-image:url(:/Resources/MyTitle/restore.png) 0 54 0 27 ;\n"
"}\n"
"\n"
"QPushButton#ButtonRestore:pressed\n"
"{\n"
"    border-image:url(:/Resources/MyTitle/restore.png) 0 27 0 54 ;\n"
"}\n"
"\n"
"/*关闭按钮*/\n"
"QPushButton#ButtonClose\n"
"{\n"
"    border-image:url(:/Resources/MyTitle/close.png) 0 81 0 0 ;\n"
"    border-top-right-radius:3 ;\n"
"}\n"
"\n"
"QPushButton#ButtonClose:hover\n"
"{\n"
"    border-image:url(:/Resources/MyTitle/close.png) 0 54 0 27 ;\n"
"    border-top-right-radius:3 ;\n"
"}\n"
"\n"
"QPushButton#ButtonClose:pressed\n"
"{\n"
"    border-image:url(:/Resources/MyTitle/close.png) 0 27 0 54 ;\n"
"    border-top-right-radius:3 ;\n"
"}\n"
"QWidget#myBar{\n"
"background-color: rgb(153, 153, 153);\n"
"}")
        self.myBar.setObjectName("myBar")
        self.gridLayout = QtWidgets.QGridLayout(self.myBar)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.ButtonMax = QtWidgets.QPushButton(self.myBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(30)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.ButtonMax.sizePolicy().hasHeightForWidth())
        self.ButtonMax.setSizePolicy(sizePolicy)
        self.ButtonMax.setText("")
        self.ButtonMax.setObjectName("ButtonMax")
        self.gridLayout.addWidget(self.ButtonMax, 0, 2, 1, 1)
        self.ButtonMin = QtWidgets.QPushButton(self.myBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(30)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.ButtonMin.sizePolicy().hasHeightForWidth())
        self.ButtonMin.setSizePolicy(sizePolicy)
        self.ButtonMin.setText("")
        self.ButtonMin.setObjectName("ButtonMin")
        self.gridLayout.addWidget(self.ButtonMin, 0, 1, 1, 1)
        self.ButtonClose = QtWidgets.QPushButton(self.myBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(30)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.ButtonClose.sizePolicy().hasHeightForWidth())
        self.ButtonClose.setSizePolicy(sizePolicy)
        self.ButtonClose.setText("")
        self.ButtonClose.setObjectName("ButtonClose")
        self.gridLayout.addWidget(self.ButtonClose, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.myBar)
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setObjectName("calendarWidget")
        self.verticalLayout.addWidget(self.calendarWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

import customtitle_rc
