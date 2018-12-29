import configparser
import sys
import os

base_dir=os.path.dirname(__file__)
sys.path.append(base_dir)
sys.path.append('./UI')

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from UI.ui_MainWindows import Ui_MainWindow

from TCPServer import TcpServer
from TCPClients import TcpClients
from UDPServer import UdpServer
# from UDPClients import UdpClients


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.tcp_server = TcpServer(self)
        self.tcp_clients = TcpClients(self)
        self.udp_server = UdpServer(self)
        # self.udp_clients = UdpClients(self)

        self._config_path = './NetDebug.ini'
        self.tcp_server.status_signal.connect(
            self.status_show
        )
        self.tcp_clients.status_signal.connect(
            self.status_show
        )
        self.udp_server.status_signal.connect(
            self.status_show
        )
        # self.udp_clients.status_signal.connect(
            # self.status_show
        # )

        self.initUi()
        self.setWindowTitle("网络调试助手")
        self.initConfig()
        self.stackedWidget.insertWidget(0, self.tcp_server)
        self.stackedWidget.insertWidget(1, self.tcp_clients)
        self.stackedWidget.insertWidget(2, self.udp_server)

        self.stackedWidget.setCurrentIndex(0)
        self.listWidget.setCurrentRow(0)
        self.listWidget.currentRowChanged.connect(
            self.stackedWidget.setCurrentIndex
        )

    def initUi(self):
        self.setWindowIcon(QtGui.QIcon(':/img/images/ico.png'))
        self.resize(760, 600)

    def initConfig(self):
        self.tcp_server.initConfig()
        self.tcp_clients.initConfig()
        self.udp_server.initConfig()
        # self.udp_clients.initConfig()
    
    def update_config(self):
        config = configparser.ConfigParser()
        config['TCPServer'] = self.tcp_server.update_config()
        config['TCPClients'] = self.tcp_clients.update_config()
        config['UDPServer'] = self.udp_server.update_config()
        # config['UDPClients'] = self.udp_clients.update_config()

        with open(self._config_path, 'w', encoding='utf-8') as fi:
            config.write(fi)

    def closeEvent(self, event):
        self.update_config()
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
