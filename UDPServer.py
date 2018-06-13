import os
import time
import configparser

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from UI.ui_UDPServer import Ui_Form
from Single import SingleSend


class UdpServer(QtWidgets.QWidget, Ui_Form):

    status_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(UdpServer, self).__init__(parent)
        self.setupUi(self)
