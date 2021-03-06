import os
import configparser


from PyQt5 import QtWidgets
from PyQt5 import QtCore
from UI.ui_SingleSend import Ui_Form


class SingleSend(QtWidgets.QWidget, Ui_Form):

    status_signal = QtCore.pyqtSignal(str)
    data_signal = QtCore.pyqtSignal(bytes)

    def __init__(self, parent):
        super(SingleSend, self).__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(
            self.on_push_button_clicked
        )
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(
            self.on_timer_out
        )
        self.checkBox_Times.stateChanged.connect(
            self.on_check_Timers
        )
        self.checkBox_Hex.stateChanged.connect(
            self.on_check_hex
        )

    def initConfig(self, msg):
        try:
            self.checkBox_Hex.setChecked(msg['singlehex'] == 'True')
            self.textEdit.insertPlainText(msg['singlesenddata'])
            self.lineEdit_Times.setText(msg['singletimes'])
        except Exception as err:
            self.status_signal.emit(str(err))

    def update_config(self):
        config = {
            'singlehex': str(self.checkBox_Hex.isChecked()),
            'singlesenddata': self.textEdit.toPlainText(),
            'singletimes': self.lineEdit_Times.text()
        }
        return config

    def handle_data(self):
        """
        生成需要发送的数据
        """
        msg = self.textEdit.toPlainText()
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

    def on_push_button_clicked(self):
        msg = self.handle_data()
        if msg == None:
            return

        self.data_signal.emit(msg)

    def on_timer_out(self):
        self.on_push_button_clicked()

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

    def on_check_hex(self):
        try:
            data = self.textEdit.toPlainText().strip()
            if not data:
                return
            if self.checkBox_Hex.isChecked():
                data_temp = ' '.join('%02X' % ord(c) for c in data)
            else:
                data_temp = ''.join(chr(int(h, 16)) for h in data.split(' '))
            self.textEdit.clear()
            self.textEdit.insertPlainText(data_temp)
        except Exception as err:
            self.status_signal.emit(str(err))

