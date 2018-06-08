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
            self.on_pushButton_clicked
        )

    def initConfig(self):
        config = configparser.ConfigParser()
        try:
            if os.path.exists(self._config_path):
                config.read(self._config_path) 
                tcp_server = config['TCPServer']
                self.textEdit.insertPlainText(
                    tcp_server['senddata']
                )
        except Exception as err:
            self.status_signal.emit(str(err))

    def handle_data(self):
        """
        生成需要发送的数据
        """
        msg = self.textEdit.toPlainText()
        if self.checkBox_Hex.isChecked():
            data = msg.split(' ')
            return bytes(list(map(int, data)))
        else:
            return msg.encode('gbk')


    def on_pushButton_clicked(self):
        msg = self.handle_data()
        self.data_signal.emit(msg)