import os
import configparser

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from UI.ui_Single import Ui_Form


class SingleSend(QtWidgets.QWidget, Ui_Form):

    status_signal = QtCore.pyqtSignal(str)
    def __init__(self, parent):
        super(SingleSend, self).__init__(parent)
        self.setupUi(self)

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