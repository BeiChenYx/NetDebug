# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\TCPClients.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(488, 470)
        self.gridLayout_4 = QtWidgets.QGridLayout(Form)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setMaximumSize(QtCore.QSize(137, 16777215))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.lineEdit_IP = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_IP.setObjectName("lineEdit_IP")
        self.verticalLayout_2.addWidget(self.lineEdit_IP)
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.lineEdit_Port = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_Port.setObjectName("lineEdit_Port")
        self.verticalLayout_2.addWidget(self.lineEdit_Port)
        self.checkBox_Display_Time = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_Display_Time.setObjectName("checkBox_Display_Time")
        self.verticalLayout_2.addWidget(self.checkBox_Display_Time)
        self.checkBox_Display_Hex = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_Display_Hex.setObjectName("checkBox_Display_Hex")
        self.verticalLayout_2.addWidget(self.checkBox_Display_Hex)
        self.checkBox_Pause = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_Pause.setObjectName("checkBox_Pause")
        self.verticalLayout_2.addWidget(self.checkBox_Pause)
        self.pushButton_Connect = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_Connect.setObjectName("pushButton_Connect")
        self.verticalLayout_2.addWidget(self.pushButton_Connect)
        self.pushButton_Clear_Display = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_Clear_Display.setObjectName("pushButton_Clear_Display")
        self.verticalLayout_2.addWidget(self.pushButton_Clear_Display)
        self.pushButton_Send_File = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_Send_File.setObjectName("pushButton_Send_File")
        self.verticalLayout_2.addWidget(self.pushButton_Send_File)
        self.pushButton_Clear_Count = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_Clear_Count.setObjectName("pushButton_Clear_Count")
        self.verticalLayout_2.addWidget(self.pushButton_Clear_Count)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.label_RX = QtWidgets.QLabel(self.groupBox_3)
        self.label_RX.setObjectName("label_RX")
        self.horizontalLayout.addWidget(self.label_RX)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.label_TX = QtWidgets.QLabel(self.groupBox_3)
        self.label_TX.setObjectName("label_TX")
        self.horizontalLayout_2.addWidget(self.label_TX)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_3, 0, 0, 2, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(0, 6, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 0, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 150))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox_2)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 1, 1, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "TCP/IP_Clients"))
        self.label.setText(_translate("Form", "目标地址:"))
        self.label_2.setText(_translate("Form", "目标端口:"))
        self.checkBox_Display_Time.setText(_translate("Form", "显示接收时间"))
        self.checkBox_Display_Hex.setText(_translate("Form", "十六进制显示"))
        self.checkBox_Pause.setText(_translate("Form", "暂停接收显示"))
        self.pushButton_Connect.setText(_translate("Form", "连接"))
        self.pushButton_Clear_Display.setText(_translate("Form", "清空显示"))
        self.pushButton_Send_File.setText(_translate("Form", "发送文件"))
        self.pushButton_Clear_Count.setText(_translate("Form", "清空计数"))
        self.label_3.setText(_translate("Form", "RX"))
        self.label_RX.setText(_translate("Form", "0"))
        self.label_5.setText(_translate("Form", "TX"))
        self.label_TX.setText(_translate("Form", "0"))
        self.groupBox.setTitle(_translate("Form", "网络数据接收"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Tab 2"))

