import os
import time
import configparser

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from UI.ui_UDPClients import Ui_Form
from Single import SingleSend
from SendList import SendList


class UdpClients(QtWidgets.QWidget, Ui_Form):

    status_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(UdpClients, self).__init__(parent)
        self.setupUi(self)
