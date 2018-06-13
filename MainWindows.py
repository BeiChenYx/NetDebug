import configparser

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from UI.ui_MainWindows import Ui_MainWindow

from TCPServer import TcpServer
from TCPClients import TcpClients
from UDPServer import UdpServer
from UDPClients import UdpClients


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.tcp_server = TcpServer(self)
        self.tcp_clients = TcpClients(self)
        self.udp_server = UdpServer(self)
        self.udp_clients = UdpClients(self)

        self._config_path = './NetDebug.ini'
        self.tcp_server.status_signal.connect(
            self.status_show
        )
        self.tcp_clients.status_signal.connect(
            self.status_show
        )

        self.initUi()
        self.setWindowTitle("网络调试助手")
        self.initConfig()

    def initUi(self):
        self.tabWidget.clear()
        self.tabWidget.addTab(self.tcp_server, 'TCP服务器')
        self.tabWidget.addTab(self.tcp_clients, 'TCP客户端')
        self.tabWidget.addTab(self.udp_server, 'UDP服务器')
        self.tabWidget.addTab(self.udp_clients, 'UDP客户端')

        self.setWindowIcon(QtGui.QIcon('./images/ico.png'))
        self.resize(760, 600)

    def initConfig(self):
        self.tcp_server.initConfig()
        self.tcp_clients.initConfig()
    
    def update_config(self):
        config = configparser.ConfigParser()
        config['TCPServer'] = self.tcp_server.update_config()
        config['TCPClients'] = self.tcp_clients.update_config()

        with open(self._config_path, 'w', encoding='utf-8') as fi:
            config.write(fi)


    def closeEvent(self, event):
        self.update_config()
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
