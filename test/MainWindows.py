from PyQt5 import QtCore, QtGui, QtWidgets

from ui_customerBar import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(widget)
    ui.show()
    sys.exit(app.exec_())
