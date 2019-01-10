import configparser
import sys
import os

base_dir = os.path.dirname(__file__)
sys.path.append(base_dir)
sys.path.append('./UI')

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from UI.ui_MainWindows import Ui_MainWindow

from TCPServer import TcpServer
from TCPClients import TcpClients
from UDPServer import UdpServer
from help import Help


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.tcp_server = TcpServer(self)
        self.tcp_clients = TcpClients(self)
        self.udp_server = UdpServer(self)
        self.help = Help(self)

        self.init_ui()
        self.init_connect()
        self.init_config()

    def init_ui(self):
        self.setWindowIcon(QtGui.QIcon(':/img/images/ico.png'))
        self.resize(760, 600)
        self.setWindowTitle("网络调试助手")

        self.stackedWidget.insertWidget(0, self.tcp_server)
        self.stackedWidget.insertWidget(1, self.tcp_clients)
        self.stackedWidget.insertWidget(2, self.udp_server)
        self.stackedWidget.insertWidget(3, self.help)

        self.stackedWidget.setCurrentIndex(0)
        self.listWidget.setCurrentRow(0)

    def init_connect(self):
        self.tcp_server.status_signal.connect(self.status_show)
        self.tcp_clients.status_signal.connect(self.status_show)
        self.udp_server.status_signal.connect(self.status_show)
        self.listWidget.currentRowChanged.connect(
            self.stackedWidget.setCurrentIndex
        )

    def init_config(self):
        self._config_path = './NetDebug.ini'
        self.tcp_server.initConfig()
        self.tcp_clients.initConfig()
        self.udp_server.initConfig()
    
    def update_config(self):
        config = configparser.ConfigParser()
        config['TCPServer'] = self.tcp_server.update_config()
        config['TCPClients'] = self.tcp_clients.update_config()
        config['UDPServer'] = self.udp_server.update_config()

        with open(self._config_path, 'w', encoding='gbk') as fi:
            config.write(fi)

    def closeEvent(self, event):
        self.update_config()
        event.accept()

    def status_show(self, msg):
        self.statusBar().showMessage(msg, 5000)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    if sys.platform == 'win32':
        font = QtGui.QFont('微软雅黑', 10)
    else:
        fontid = QtGui.QFontDatabase.addApplicationFont('./Inconsolata.otf')
        font_famliy = QtGui.QFontDatabase.applicationFontFamilies(fontid)
        font = QtGui.QFont('Inconsolata', 12)
    app.setFont(font)
    widget = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(widget)
    ui.show()
    sys.exit(app.exec_())
