import os
import configparser
import time


from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from UI.ui_TCPClients import Ui_Form


class TcpClients(QtWidgets.QWidget, Ui_Form):

    def __init__(self, parent):
        super(TcpClients, self).__init__(parent)
        self.setupUi(self)