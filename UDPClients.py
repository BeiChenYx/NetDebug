import os
import time
import configparser

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from UI.ui_UDPClients import Ui_Form
from Single import SingleSend
from SendList import SendList
from selector_udp_clients_handle import UdpClientsWorkThread


class UdpClients(QtWidgets.QWidget, Ui_Form):

    status_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        """
        data格式:
        cmd-message
        cmd:
            0: info_status           普通状态信息
            1: clientThreadStart     客户端线程启动
            2: clientThreadClose     客户端线程关闭
            3: clientCreate          客户端创建完成
            4: clientClose           客户端关闭
        """
        super(UdpClients, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_Connect.setText('创建')
        self._config_path = './NetDebug.ini'
        self.initUi()
        self.init_connect()
        self.cmd_status_func_dict = {
            0: self.info_status,
            1: self.clientThreadStart,
            2: self.clientThreadClose,
            3: self.clientCreate,
            4: self.clientClose,
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

    def init_connect(self):
        self.pushButton_Connect.clicked.connect(
            self.on_pushButton_connect
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
                tcp_clients = config['UDPClients']
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

    def on_pushButton_connect(self):
        if self.pushButton_Connect.text() == '创建':
            try:
                self.udp_clients = UdpClientsWorkThread(
                    self.lineEdit_IP.text(),
                    int(self.lineEdit_Port.text()),
                    int(self.lineEdit_Clients_Count.text())
                )
                self.udp_clients.dataSignal.connect(
                    self.on_workData
                )
                self.udp_clients.statusSignal.connect(
                    self.on_workStatus
                )
                self.udp_clients.start()
            except Exception as err:
                self.status_signal.emit(str(err)) 
        else:
            self.udp_clients.exitUdpClientsThread()
            self.udp_clients.quit()
            self.udp_clients.wait(1000)
    
    def on_workData(self, data):
        if self.checkBox_Pause.isChecked():
            return
        if len(self.textEdit.toPlainText()) > 4096:
            self.textEdit.clear()
        self.label_RX.setText(
            str(int(self.label_RX.text()) + len(data))
        )
        
        date_time = '' 
        if self.checkBox_Display_Time.isChecked():
            date_time = self.get_date_time()

        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        if self.checkBox_Display_Hex.isChecked():
            data_list = list(map(lambda x: '%02X' % x, data))
            self.textEdit.insertPlainText(' '.join(data_list) + ' ' + date_time)
            # if self.checkBox_Recv_To_File.isChecked():
            #     self.save_file_name(' '.join(data_list) + ' ' + date_time)
        else:
            self.textEdit.insertPlainText(data.decode('gbk', 'ignore') + date_time)

    def on_workStatus(self, data):
        """
        data格式:
        cmd-message
        cmd:
            0: info_status           普通状态信息
            1: clientThreadStart     客户端线程启动
            2: clientThreadClose     客户端线程关闭
            3: clientCreate          客户端创建完成
            4: clientClose           客户端关闭
        """
        cmd, message = data.split('-')
        self.handle_workStatus(int(cmd), message)
        
    def handle_workStatus(self, cmd, data):
        self.cmd_status_func_dict[cmd](data)

    def on_pushButton_clear_display(self):
        self.textEdit.clear()

    def on_pushButton_clear_count(self):
        self.label_RX.setText('0')
        self.label_TX.setText('0')

    def sendData(self, data):
        try:
            self.udp_clients.sendData(data)
            self.label_TX.setText(
                str(int(self.label_TX.text()) + len(data))
            )
        except Exception as err:
            self.status_signal.emit(str(err))

    def get_date_time(self):
        return time.strftime(' [%Y-%m-%d %H:%M:%S]\n', time.localtime())

    def update_listWidget(self):
        """
        更新listView，如果self._clients为空则全都删除
        """
        self.listWidget.clear()
        self.listWidget.addItems(self._clients)
        self.listWidget.setCurrentRow(0)
    
    def info_status(self, data):
        self.status_signal.emit(data)

    def clientThreadStart(self, data):
        self.status_signal.emit(data)
        self.pushButton_Connect.setText('关闭')

    def clientThreadClose(self, data):
        self.status_signal.emit(data)
        self.pushButton_Connect.setText('创建')
        self._clients.clear()
        self.update_listWidget()
    
    def clientCreate(self, data):
        if data not in self._clients:
            self._clients.append(data)
            self.update_listWidget()
    
    def clientClose(self, data):
        self._clients.remove(data)
        self.update_listWidget()