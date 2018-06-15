import os
import configparser
import time


from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from UI.ui_TCPClients import Ui_Form
from Single import SingleSend
from SendList import SendList

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
            4: self.clientThreadStart,
            5: self.clientThreadClose,
        }
        self._clients = list()

    def initUi(self):
        self.tabWidget.clear()

        self.single_send = SingleSend(self)
        self.send_list = SendList(self)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidget(self.send_list)
        self.tabWidget.addTab(self.single_send, '数据发送')
        self.tabWidget.addTab(self.scrollArea, '多条发送')

    def initConnect(self):
        self.pushButton_Connect.clicked.connect(
            self.on_pushButton_Connect_cliecked
        )
        self.pushButton_Clear_Display.clicked.connect(
            self.on_pushButton_clear_display        
        )
        self.pushButton_Clear_Count.clicked.connect(
            self.on_pushButton_clear_count
        )
        self.single_send.data_signal.connect(
            self.sendData
        )
        self.single_send.status_signal.connect(
            self.status_signal
        )
        self.send_list.data_signal.connect(
            self.sendData
        )
        self.send_list.status_signal.connect(
            self.status_signal
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
                self.single_send.initConfig(tcp_clients)
                self.send_list.initConfig(tcp_clients)
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
        config.update(self.single_send.update_config())
        config.update(self.send_list.update_config())
        return config

    def on_pushButton_clear_display(self):
        self.textEdit.clear()

    def on_pushButton_clear_count(self):
        self.label_RX.setText('0')
        self.label_TX.setText('0')

    def on_pushButton_Connect_cliecked(self):
        if self.pushButton_Connect.text() == '连接':
            try:
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
            except Exception as err:
                self.status_signal.emit(str(err))
        else:
            self.tcp_clients.exitTcpClientsThread()
            self.tcp_clients.quit()
            self.tcp_clients.wait(1000)

    def on_workData(self, msg):
        if self.checkBox_Pause.isChecked():
            return
        if len(self.textEdit.toPlainText()) > 4096:
            self.textEdit.clear()
        self.label_RX.setText(
            str(int(self.label_RX.text()) + len(msg))
        )
        
        date_time = '' 
        if self.checkBox_Display_Time.isChecked():
            date_time = self.get_date_time()

        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        if self.checkBox_Display_Hex.isChecked():
            data_list = list(map(lambda x: '%02X' % x, msg))
            self.textEdit.insertPlainText(' '.join(data_list) + ' ' + date_time)
            if self.checkBox_Recv_To_File.isChecked():
                self.save_file_name(' '.join(data_list) + ' ' + date_time)
        else:
            self.textEdit.insertPlainText(msg.decode('gbk', 'ignore') + date_time)

    def on_workStatus(self, msg):
        """
        msg格式:
        cmd-message
        cmd:
            0: ClientConnect         客户端已连接
            1: ClientClose           客户端断开
            2: ClientConnectErr      客户端连接错误
            3: info_status           普通状态信息
            4: clientThreadStart
            5: clientThreadClose
        """
        cmd, message = msg.split('-')
        self.handle_workStatus(int(cmd), message)

    def handle_workStatus(self, cmd, msg):
        self.cmd_status_func_dict[cmd](msg)

    def clientConnect(self, msg):
        self._clients.append(msg)
        self.update_listWidget()

    def clientClose(self, msg):
        self._clients.remove(msg)
        self.update_listWidget()

    def clientConnectErr(self, msg):
        self.status_signal.emit(msg)
    
    def info_status(self, msg):
        self.status_signal.emit(msg)

    def clientThreadStart(self, msg):
        self.status_signal.emit(msg)
        self.pushButton_Connect.setText('关闭')

    def clientThreadClose(self, msg):
        self.status_signal.emit(msg)
        self.pushButton_Connect.setText('连接')

    def update_listWidget(self):
        """
        更新listView，如果self._clients为空则全都删除
        """
        self.listWidget.clear()
        self.listWidget.addItems(self._clients)
        self.listWidget.setCurrentRow(0)

    def sendData(self, msg):
        try:
            self.tcp_clients.sendData(msg)
            self.label_TX.setText(
                str(int(self.label_TX.text()) + len(msg))
            )
        except Exception as err:
            self.status_signal.emit(str(err))

    def get_date_time(self):
        return time.strftime(' [%Y-%m-%d %H:%M:%S]\n', time.localtime())