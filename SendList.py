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

    def initConfig(self, msg):
        try:
            self.checkBox_Hex.setChecked(
                msg['listhex'] == 'True'
            )
            self.lineEdit_Times.setText(msg['listtimes'])

            self.checkBoxs1.setChecked(msg['listc1'] == 'True')
            self.checkBoxs2.setChecked(msg['listc2'] == 'True')
            self.checkBoxs3.setChecked(msg['listc3'] == 'True')
            self.checkBoxs4.setChecked(msg['listc4'] == 'True')
            self.checkBoxs5.setChecked(msg['listc5'] == 'True')
            self.checkBoxs6.setChecked(msg['listc6'] == 'True')
            self.checkBoxs7.setChecked(msg['listc7'] == 'True')
            self.checkBoxss8.setChecked(msg['listc8'] == 'True')
            self.checkBoxs9.setChecked(msg['listc9'] == 'True')
            self.checkBoxs10.setChecked(msg['listc10'] == 'True')
            self.checkBoxs11.setChecked(msg['listc11'] == 'True')
            self.checkBoxs12.setChecked(msg['listc12'] == 'True')
            self.checkBoxs13.setChecked(msg['listc13'] == 'True')
            self.checkBoxs14.setChecked(msg['listc14'] == 'True')
            self.checkBoxs15.setChecked(msg['listc15'] == 'True')
            self.checkBoxs16.setChecked(msg['listc16'] == 'True')
            self.checkBoxs17.setChecked(msg['listc17'] == 'True')
            self.checkBoxs18.setChecked(msg['listc18'] == 'True')
            self.checkBoxs19.setChecked(msg['listc19'] == 'True')
            self.checkBoxs20.setChecked(msg['listc20'] == 'True')

            self.lineEdits1.setText(msg['line1'])
            self.lineEdits2.setText(msg['line2'])
            self.lineEdits3.setText(msg['line3'])
            self.lineEdits4.setText(msg['line4'])
            self.lineEdits5.setText(msg['line5'])
            self.lineEdits6.setText(msg['line6'])
            self.lineEdits7.setText(msg['line7'])
            self.lineEdits8.setText(msg['line8'])
            self.lineEdits9.setText(msg['line9'])
            self.lineEdits10.setText(msg['line10'])
            self.lineEdits11.setText(msg['line11'])
            self.lineEdits12.setText(msg['line12'])
            self.lineEdits13.setText(msg['line13'])
            self.lineEdits14.setText(msg['line14'])
            self.lineEdits15.setText(msg['line15'])
            self.lineEdits16.setText(msg['line16'])
            self.lineEdits17.setText(msg['line17'])
            self.lineEdits18.setText(msg['line18'])
            self.lineEdits19.setText(msg['line19'])
            self.lineEdits20.setText(msg['line20'])
        except Exception as err:
            self.status_signal.emit(str(err))

    def update_config(self):
        config = {
            'listhex': str(self.checkBox_Hex.isChecked()),
            'listtimes': self.lineEdit_Times.text(),

            'listc1': str(self.checkBoxs1.isChecked()),
            'listc2': str(self.checkBoxs2.isChecked()),
            'listc3': str(self.checkBoxs3.isChecked()),
            'listc4': str(self.checkBoxs4.isChecked()),
            'listc5': str(self.checkBoxs5.isChecked()),
            'listc6': str(self.checkBoxs6.isChecked()),
            'listc7': str(self.checkBoxs7.isChecked()),
            'listc8': str(self.checkBoxss8.isChecked()),
            'listc9': str(self.checkBoxs9.isChecked()),
            'listc10': str(self.checkBoxs10.isChecked()),
            'listc11': str(self.checkBoxs11.isChecked()),
            'listc12': str(self.checkBoxs12.isChecked()),
            'listc13': str(self.checkBoxs13.isChecked()),
            'listc14': str(self.checkBoxs14.isChecked()),
            'listc15': str(self.checkBoxs15.isChecked()),
            'listc16': str(self.checkBoxs16.isChecked()),
            'listc17': str(self.checkBoxs17.isChecked()),
            'listc18': str(self.checkBoxs18.isChecked()),
            'listc19': str(self.checkBoxs19.isChecked()),
            'listc20': str(self.checkBoxs20.isChecked()),

            'line1': self.lineEdits1.text(),
            'line2': self.lineEdits2.text(),
            'line3': self.lineEdits3.text(),
            'line4': self.lineEdits4.text(),
            'line5': self.lineEdits5.text(),
            'line6': self.lineEdits6.text(),
            'line7': self.lineEdits7.text(),
            'line8': self.lineEdits8.text(),
            'line9': self.lineEdits9.text(),
            'line10': self.lineEdits10.text(),
            'line11': self.lineEdits11.text(),
            'line12': self.lineEdits12.text(),
            'line13': self.lineEdits13.text(),
            'line14': self.lineEdits14.text(),
            'line15': self.lineEdits15.text(),
            'line16': self.lineEdits16.text(),
            'line17': self.lineEdits17.text(),
            'line18': self.lineEdits18.text(),
            'line19': self.lineEdits19.text(),
            'line20': self.lineEdits20.text(),
        }
        return config

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
            try:
                self.timer.start(int(self.lineEdit_Times.text()))
            except Exception as err:
                self.status_signal.emit(str(err))
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
