from PyQt5 import QtWidgets
from UI.ui_SendList import Ui_Form


class SendList(QtWidgets.QWidget, Ui_Form):

    def __init__(self, parent):
        super(SendList, self).__init__(parent)
        self.setupUi(self)