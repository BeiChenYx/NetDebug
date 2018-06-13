import os
import configparser


from PyQt5 import QtWidgets
from PyQt5 import QtCore
from UI.ui_SendList import Ui_Form


class SendList(QtWidgets.QWidget, Ui_Form):

    status_signal = QtCore.pyqtSignal(str)
    data_signal = QtCore.pyqtSignal(bytes)

    def __init__(self, parent):
        super(SendList, self).__init__(parent)
        self.setupUi(self)
        # self.init_connect()

    def handle_data(self, msg):
        if self.checkBox_Hex.isChecked():
            try:
                data = msg.split(' ')
                return bytes(list(map(lambda x: int(x, 16), data)))
            except Exception:
                self.status_signal.emit(
                    '16进制正确格式: 0A 0B 0C 15'
                )
                return None
        else:
            return msg.encode('gbk')

    def send_data(self, msg):
        msg = self.handle_data(msg)
        if msg == None:
            return
        self.data_signal.emit(msg)

    def on_pushButtons1_clicked(self):
        self.send_data(self.lineEdits1.text())

    # def on_pushButtons2_clicked(self):
    #     self.send_data(self.lineEdits2.text())

    # def on_pushButtons3_clicked(self):
    #     self.send_data(self.lineEdits3.text())

    # def on_pushButtons4_clicked(self):
    #     self.send_data(self.lineEdits4.text())

    # def on_pushButtons5_clicked(self):
    #     self.send_data(self.lineEdits5.text())

    # def on_pushButtons6_clicked(self):
    #     self.send_data(self.lineEdits6.text())

    # def on_pushButtons7_clicked(self):
    #     self.send_data(self.lineEdits7.text())

    # def on_pushButtons8_clicked(self):
    #     self.send_data(self.lineEdits8.text())

    # def on_pushButtons9_clicked(self):
    #     self.send_data(self.lineEdits9.text())

    # def on_pushButtons10_clicked(self):
    #     self.send_data(self.lineEdits10.text())

    # def on_pushButtons11_clicked(self):
    #     self.send_data(self.lineEdits11.text())

    # def on_pushButtons12_clicked(self):
    #     self.send_data(self.lineEdits12.text())

    # def on_pushButtons13_clicked(self):
    #     self.send_data(self.lineEdits13.text())

    # def on_pushButtons14_clicked(self):
    #     self.send_data(self.lineEdits14.text())

    # def on_pushButtons15_clicked(self):
    #     self.send_data(self.lineEdits15.text())

    # def on_pushButtons16_clicked(self):
    #     self.send_data(self.lineEdits16.text())

    # def on_pushButtons17_clicked(self):
    #     self.send_data(self.lineEdits17.text())

    # def on_pushButtons18_clicked(self):
    #     self.send_data(self.lineEdits18.text())

    # def on_pushButtons19_clicked(self):
    #     self.send_data(self.lineEdits19.text())

    # def on_pushButtons20_clicked(self):
    #     self.send_data(self.lineEdits20.text())

    def init_connect(self):
        self.pushButtons1.clicked.connect(
            self.on_pushButtons1_clicked
        )
        # self.pushButtons2.clicked.connect(
        #     self.on_pushButtons2_clicked
        # )
        # self.pushButtons3.clicked.connect(
        #     self.on_pushButtons3_clicked
        # )
        # self.pushButtons4.clicked.connect(
        #     self.on_pushButtons4_clicked
        # )
        # self.pushButtons5.clicked.connect(
        #     self.on_pushButtons5_clicked
        # )
        # self.pushButtons6.clicked.connect(
        #     self.on_pushButtons6_clicked
        # )
        # self.pushButtons7.clicked.connect(
        #     self.on_pushButtons7_clicked
        # )
        # self.pushButtons8.clicked.connect(
        #     self.on_pushButtons8_clicked
        # )
        # self.pushButtons9.clicked.connect(
        #     self.on_pushButtons9_clicked
        # )
        # self.pushButtons10.clicked.connect(
        #     self.on_pushButtons10_clicked
        # )
        # self.pushButtons11.clicked.connect(
        #     self.on_pushButtons11_clicked
        # )
        # self.pushButtons12.clicked.connect(
        #     self.on_pushButtons12_clicked
        # )
        # self.pushButtons13.clicked.connect(
        #     self.on_pushButtons13_clicked
        # )
        # self.pushButtons14.clicked.connect(
        #     self.on_pushButtons14_clicked
        # )
        # self.pushButtons15.clicked.connect(
        #     self.on_pushButtons15_clicked
        # )
        # self.pushButtons16.clicked.connect(
        #     self.on_pushButtons16_clicked
        # )
        # self.pushButtons17.clicked.connect(
        #     self.on_pushButtons17_clicked
        # )
        # self.pushButtons18.clicked.connect(
        #     self.on_pushButtons18_clicked
        # )
        # self.pushButtons19.clicked.connect(
        #     self.on_pushButtons19_clicked
        # )
        # self.pushButtons20.clicked.connect(
        #     self.on_pushButtons20_clicked
        # )