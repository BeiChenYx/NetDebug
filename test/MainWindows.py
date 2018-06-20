from PyQt5 import QtCore, QtGui, QtWidgets

from ui_customerBar import Ui_MainWindow
from basewindow import BaseWindow
from mytitlebar import ButtonType

class MainWindow(BaseWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        # self.setupUi(self)
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.initTitleBar()

    def initTitleBar(self):
        self.m_titleBar.setTitleRoll()        
        self.m_titleBar.setTitleIcon('./Resources/titleicon.png')
        self.m_titleBar.setTitleContent('前行中的小猪-前行之路还需前行')
        self.m_titleBar.setButtonType(ButtonType.ONLY_CLOSE_BUTTON)
        self.m_titleBar.setTitleWidth(self.width())
        self.m_titleBar.loadStyleSheet('MyTitle')

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # widget = QtWidgets.QMainWindow()
    widget = QtWidgets.QWidget()
    ui = MainWindow()
    # ui.setupUi(widget)
    ui.show()
    sys.exit(app.exec_())
