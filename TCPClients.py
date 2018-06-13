import os
import configparser
import time


from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from UI.ui_TCPClients import Ui_Form

from selector_clients_handle import TcpClientsWorkThread


class TcpClients(QtWidgets.QWidget, Ui_Form):

    status_signal = QtCore.pyqtSignal(str)
    def __init__(self, parent):
        super(TcpClients, self).__init__(parent)
        self.setupUi(self)
        self._config_path = './NetDebug.ini'
        self.initUi()
        self.initConnect()

        self.cmd_status_func_dict = {
            0: self.clientConnect,
            1: self.clientClose,
            2: self.clientConnectErr,
            3: self.info_status,
        }

    def initUi(self):
        pass

    def initConnect(self):
        self.pushButton_Connect.clicked.connect(
            self.on_pushButton_Connect_cliecked
        )

    def initConfig(self):
        config = configparser.ConfigParser()
        try:
            if os.path.exists(self._config_path):
                config.read(self._config_path)
                tcp_clients = config['TCPClients']
                self.lineEdit_IP.setText(tcp_clients['serverip'])
                self.lineEdit_Port.setText(tcp_clients['serverport'])
                self.checkBox_Display_Time.setChecked(
                    tcp_clients['displayrecvetime'] == 'True'
                )
                self.checkBox_Display_Hex.setChecked(
                    tcp_clients['hexdisplay'] == 'True'
                )
                self.checkBox_Pause.setChecked(
                    tcp_clients['pause'] == 'True'
                )
                self.lineEdit_Clients_Count.setText(
                    tcp_clients['count']
                )

        except Exception as err:
            self.status_signal.emit(str(err))
        
    def update_config(self):
        config = {
            'serverip': self.lineEdit_IP.text(),
            'serverport': self.lineEdit_Port.text(),
            'displayrecvetime': str(self.checkBox_Display_Time.isChecked()),
            'hexdisplay': str(self.checkBox_Display_Hex.isChecked()),
            'pause': str(self.checkBox_Pause.isChecked()),
            'count': self.lineEdit_Clients_Count.text(),
        }
        return config

    def on_pushButton_Connect_cliecked(self):
        if self.pushButton_Connect.text() == '连接':
            self.tcp_clients = TcpClientsWorkThread(
                self.lineEdit_IP.text(),
                int(self.lineEdit_Port.text()),
                int(self.lineEdit_Clients_Count.text())
            )
            self.tcp_clients.dataSignal.connect(
                self.on_workData
            )
            self.tcp_clients.statusSignal.connect(
                self.on_workStatus
            )
            self.tcp_clients.start()
        else:
            self.tcp_clients.exitTcpClientsThread()
            self.tcp_clients.terminate()
            self.tcp_clients.wait(1000)

    def on_workData(self, msg):
        print(msg)

    def on_workStatus(self, msg):
        """
        msg格式:
        cmd-message
        cmd:
            0: ClientConnect         客户端已连接
            1: ClientClose           客户端断开
            2: ClientConnectErr      客户端连接错误
            3: info_status           普通状态信息
        """
        cmd, message = msg.split('-')
        self.handle_workStatus(int(cmd), message)

    def handle_workStatus(self, cmd, msg):
        self.cmd_status_func_dict[cmd](msg)

    def clientConnect(self, msg):
        print(msg)
        self.status_signal.emit(msg)
        self.pushButton_Connect.setText('关闭')

    def clientClose(self, msg):
        print(msg)

    def clientConnectErr(self, msg):
        print(msg)
    
    def info_status(self, msg):
        print(msg)