from PyQt5 import QtWidgets
from PyQt5 import QtGui

from UI.ui_help import Ui_help


class Help(QtWidgets.QWidget, Ui_help):

    def __init__(self, parent=None):
        super(Help, self).__init__(parent)
        self.setupUi(self)
        with open('./help.html', 'r', encoding='utf-8') as fi:
            text = fi.read()
            self.textBrowser.setHtml(text)
            self.textBrowser.setOpenExternalLinks(True)