from PyQt5 import QtWidgets
from PyQt5 import QtGui
from UI.ui_MainWindows import Ui_MainWindow

from TCPServer import TcpServer
from TCPClients import TcpClients


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.tcp_server = TcpServer(self)
        self.tcp_clients = TcpClients(self)

        self.tcp_server.status_signal.connect(
            self.status_show
        )

        self.initUi()
        self.setWindowTitle("网络调试助手")
        self.initConfig()

    def initUi(self):
        self.tabWidget.clear()
        self.tabWidget.addTab(self.tcp_server, 'TCP服务器')
        self.tabWidget.addTab(self.tcp_clients, 'TCP客户端')

        self.setWindowIcon(QtGui.QIcon('./images/ico.png'))
        self.resize(760, 600)

    def initConfig(self):
        self.tcp_server.initConfig()

    def closeEvent(self, event):
        # self.tcp_server.update_config()
        self.tcp_server.on_pushButton_Connect()
        event.accept()

    def status_show(self, msg):
        self.statusBar().showMessage(msg, 5000)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(widget)
    ui.show()
    sys.exit(app.exec_())
