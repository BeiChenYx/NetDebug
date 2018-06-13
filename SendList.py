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
        self.timer = QtCore.QTimer(self)
        self.init_connect()

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

    def on_pushButtons_1_clicked(self):
        self.send_data(self.lineEdits1.text())

    def on_pushButtons_2_clicked(self):
        self.send_data(self.lineEdits2.text())

    def on_pushButtons_3_clicked(self):
        self.send_data(self.lineEdits3.text())

    def on_pushButtons_4_clicked(self):
        self.send_data(self.lineEdits4.text())

    def on_pushButtons_5_clicked(self):
        self.send_data(self.lineEdits5.text())

    def on_pushButtons_6_clicked(self):
        self.send_data(self.lineEdits6.text())

    def on_pushButtons_7_clicked(self):
        self.send_data(self.lineEdits7.text())

    def on_pushButtons_8_clicked(self):
        self.send_data(self.lineEdits8.text())

    def on_pushButtons_9_clicked(self):
        self.send_data(self.lineEdits9.text())

    def on_pushButtons_10_clicked(self):
        self.send_data(self.lineEdits10.text())

    def on_pushButtons_11_clicked(self):
        self.send_data(self.lineEdits11.text())

    def on_pushButtons_12_clicked(self):
        self.send_data(self.lineEdits12.text())

    def on_pushButtons_13_clicked(self):
        self.send_data(self.lineEdits13.text())

    def on_pushButtons_14_clicked(self):
        self.send_data(self.lineEdits14.text())

    def on_pushButtons_15_clicked(self):
        self.send_data(self.lineEdits15.text())

    def on_pushButtons_16_clicked(self):
        self.send_data(self.lineEdits16.text())

    def on_pushButtons_17_clicked(self):
        self.send_data(self.lineEdits17.text())

    def on_pushButtons_18_clicked(self):
        self.send_data(self.lineEdits18.text())

    def on_pushButtons_19_clicked(self):
        self.send_data(self.lineEdits19.text())

    def on_pushButtons_20_clicked(self):
        self.send_data(self.lineEdits20.text())

    def init_connect(self):
        self.pushButtons1.clicked.connect(
            self.on_pushButtons_1_clicked
        )
        self.pushButtons2.clicked.connect(
            self.on_pushButtons_2_clicked
        )
        self.pushButtons3.clicked.connect(
            self.on_pushButtons_3_clicked
        )
        self.pushButtons4.clicked.connect(
            self.on_pushButtons_4_clicked
        )
        self.pushButtons5.clicked.connect(
            self.on_pushButtons_5_clicked
        )
        self.pushButtons6.clicked.connect(
            self.on_pushButtons_6_clicked
        )
        self.pushButtons7.clicked.connect(
            self.on_pushButtons_7_clicked
        )
        self.pushButtons8.clicked.connect(
            self.on_pushButtons_8_clicked
        )
        self.pushButtons9.clicked.connect(
            self.on_pushButtons_9_clicked
        )
        self.pushButtons10.clicked.connect(
            self.on_pushButtons_10_clicked
        )
        self.pushButtons11.clicked.connect(
            self.on_pushButtons_11_clicked
        )
        self.pushButtons12.clicked.connect(
            self.on_pushButtons_12_clicked
        )
        self.pushButtons13.clicked.connect(
            self.on_pushButtons_13_clicked
        )
        self.pushButtons14.clicked.connect(
            self.on_pushButtons_14_clicked
        )
        self.pushButtons15.clicked.connect(
            self.on_pushButtons_15_clicked
        )
        self.pushButtons16.clicked.connect(
            self.on_pushButtons_16_clicked
        )
        self.pushButtons17.clicked.connect(
            self.on_pushButtons_17_clicked
        )
        self.pushButtons18.clicked.connect(
            self.on_pushButtons_18_clicked
        )
        self.pushButtons19.clicked.connect(
            self.on_pushButtons_19_clicked
        )
        self.pushButtons20.clicked.connect(
            self.on_pushButtons_20_clicked
        )
        self.timer.timeout.connect(self.on_timer_out)
        self.checkBox_Times.stateChanged.connect(
            self.on_check_Timers
        )

    def on_check_Timers(self):
        if self.lineEdit_Times.text() == '':
            self.status_signal.emit('循环间隔不能为空')
            return
        if self.checkBox_Times.isChecked():
            self.timer.start(int(self.lineEdit_Times.text()))
        else:
            self.timer.stop()

    def on_timer_out(self):
        if self.checkBoxs1.isChecked():
            self.on_pushButtons_1_clicked()

        if self.checkBoxs2.isChecked():
            self.on_pushButtons_2_clicked()

        if self.checkBoxs3.isChecked():
            self.on_pushButtons_3_clicked()

        if self.checkBoxs4.isChecked():
            self.on_pushButtons_4_clicked()

        if self.checkBoxs5.isChecked():
            self.on_pushButtons_5_clicked()

        if self.checkBoxs6.isChecked():
            self.on_pushButtons_6_clicked()

        if self.checkBoxs7.isChecked():
            self.on_pushButtons_7_clicked()

        if self.checkBoxss8.isChecked():
            self.on_pushButtons_8_clicked()

        if self.checkBoxs9.isChecked():
            self.on_pushButtons_9_clicked()

        if self.checkBoxs10.isChecked():
            self.on_pushButtons_10_clicked()

        if self.checkBoxs11.isChecked():
            self.on_pushButtons_11_clicked()

        if self.checkBoxs12.isChecked():
            self.on_pushButtons_12_clicked()

        if self.checkBoxs13.isChecked():
            self.on_pushButtons_13_clicked()

        if self.checkBoxs14.isChecked():
            self.on_pushButtons_14_clicked()

        if self.checkBoxs15.isChecked():
            self.on_pushButtons_15_clicked()

        if self.checkBoxs16.isChecked():
            self.on_pushButtons_16_clicked()

        if self.checkBoxs17.isChecked():
            self.on_pushButtons_17_clicked()

        if self.checkBoxs18.isChecked():
            self.on_pushButtons_18_clicked()

        if self.checkBoxs19.isChecked():
            self.on_pushButtons_19_clicked()

        if self.checkBoxs20.isChecked():
            self.on_pushButtons_20_clicked()
