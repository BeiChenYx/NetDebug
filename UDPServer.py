import os
import time
import configparser

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from UI.ui_UDPServer import Ui_Form
from Single import SingleSend
from selector_udp_server_handle import UDPServerWorkThread


class UdpServer(QtWidgets.QWidget, Ui_Form):

    status_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(UdpServer, self).__init__(parent)
        self.setupUi(self)
        self._config_path = './NetDebug.ini'
        self.initUi() 
        self.init_connect()
        self._clients = list()
        self.cmd_status_func_dict = {
            0: self.info_status,
            1: self.server_start,
            2: self.server_close,
        }

    def initUi(self):
        self.tabWidget.clear()
        self.single_send = SingleSend(self)
        self.tabWidget.addTab(self.single_send, '数据发送')

    def init_connect(self):
        self.pushButton_Connect.clicked.connect(
            self.on_pushButton_Connect
        )
        self.pushButton_Clear_Recv.clicked.connect(
            self.on_pushButton_Clear_display
        )
        self.pushButton_Clear_Count.clicked.connect(
            self.on_pushButton_clear_count
        )
        self.checkBox_Recv_To_File.stateChanged.connect(
            self.on_to_file
        )
        self.single_send.data_signal.connect(
            self.sendData
        )
        self.single_send.status_signal.connect(
            self.status_signal
        )

    def initConfig(self):
        config = configparser.ConfigParser()
        try:
            if os.path.exists(self._config_path):
                config.read(self._config_path) 
                tcp_server = config['UDPServer']
                self.lineEdit_IP.setText(tcp_server['localip'])
                self.lineEdit_Port.setText(tcp_server['localport'])
                self.checkBox_Display_Time.setChecked(
                    tcp_server['displayrecvetime'] == 'True'
                )
                self.checkBox_Display_Hex.setChecked(
                    tcp_server['hexdisplay'] == 'True'
                )
                self.checkBox_Pause_Display.setChecked(
                    tcp_server['pause'] == 'True'
                )
                # self.checkBox_Recv_To_File.setChecked(
                #     tcp_server['readtofile'] == 'True'
                # )
                self.lineEdit_Recv_File_Path.setText(
                    tcp_server['readtofilepath']
                )
                # self.checkBox_Input_Hex.setChecked(
                #     tcp_server['hexinput'] == 'True'
                # )
                # self.lineEdit_Input_File_Path.setText(
                #     tcp_server['inputFromfile']
                # )
                self.single_send.initConfig(tcp_server)
        except Exception as err:
            self.status_signal.emit(str(err))

    def update_config(self):
        config = {
            'localip': self.lineEdit_IP.text(),
            'localport': self.lineEdit_Port.text(),
            'displayrecvetime': str(self.checkBox_Display_Time.isChecked()),
            'hexdisplay': str(self.checkBox_Display_Hex.isChecked()),
            'pause': str(self.checkBox_Pause_Display.isChecked()),
            # 'readtofile': str(self.checkBox_Recv_To_File.isChecked()),
            'readtofilepath': self.lineEdit_Recv_File_Path.text(),
            # 'hexinput': str(self.checkBox_Input_Hex.isChecked()),
            # 'inputFromfile': self.lineEdit_Input_File_Path.text(),
        }
        config.update(self.single_send.update_config())
        return config

    def on_pushButton_Connect(self):
        if self.pushButton_Connect.text() == '连接':
            self.udp_server = UDPServerWorkThread(
                self.lineEdit_IP.text(),
                int(self.lineEdit_Port.text())
            )
            self.udp_server.dataSignal.connect(
                self.on_workData
            )
            self.udp_server.statusSignal.connect(
                self.on_workStatus
            )
            self.udp_server.start()
        else:
            self.udp_server.exitUdpWorkThread()
            self.udp_server.quit()
            self.udp_server.wait(1000)

    def on_workData(self, addr, data):
        if addr not in self._clients:
            self._clients.append(addr)
            self.update_listWidget()
            
        if self.pushButton_Connect.text() == '连接':
            return
        if self.checkBox_Pause_Display.isChecked():
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
            self.textEdit.insertPlainText(
                '[Receiving the data coming to' +
                str(addr) + ']:\n' + ' '.join(data_list) + ' ' + date_time
            )
            if self.checkBox_Recv_To_File.isChecked():
                self.save_file_name(
                    '[Receiving the data coming to' +
                    str(addr) + ']:\n' + ' '.join(data_list) + ' ' + date_time
                )
        else:
            self.textEdit.insertPlainText(
                '[Receiving the data coming to' +
                str(addr) + ']:\n' + data.decode('gbk', 'ignore') + date_time
            )
            if self.checkBox_Recv_To_File.isChecked():
                self.save_file_name(
                    '[Receiving the data coming to' +
                    str(addr) + ']:\n' + data.decode('gbk', 'ignore') + date_time
                )

    def on_workStatus(self, msg):
        try:
            cmd, message = msg.split('-')
            self.handle_workStatus(int(cmd), message)
        except Exception as err:
            self.status_signal.emit(str(err))

    def on_pushButton_Clear_display(self):
        self.textEdit.clear()

    def on_pushButton_clear_count(self):
        self.label_RX.setText('0')
        self.label_TX.setText('0')

    def on_to_file(self):
        if self.checkBox_Recv_To_File.isChecked():
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                '文件保存',
                'c:/',
                'All Files (*);;Text Files (*.txt)'
            )
            self.lineEdit_Recv_File_Path.setText(file_name)

    def info_status(self, msg):
        self.status_signal.emit(msg)

    def handle_workStatus(self, cmd, msg):
        self.cmd_status_func_dict[cmd](msg)

    def server_start(self, msg):
        self.status_signal.emit(msg)
        self.pushButton_Connect.setText('关闭')

    def server_close(self, msg):
        self.status_signal.emit(msg)
        self.pushButton_Connect.setText('连接')
        print('服务器关闭')
        self._clients.clear()
        self.update_listWidget()

    def update_listWidget(self):
        """
        更新listView，如果self._clients为空则全都删除
        """
        self.listWidget.clear()
        self.listWidget.addItems(self._clients)
        self.listWidget.setCurrentRow(0)

    def get_date_time(self):
        return time.strftime(' [%Y-%m-%d %H:%M:%S]\n', time.localtime())

    def sendData(self, msg):
        try:
            if self.pushButton_Connect.text() == '连接':
                return
            addr = self.get_listView_select_text()
            if addr != '':
                self.udp_server.sendData(addr, msg)
                self.label_TX.setText(
                    str(int(self.label_TX.text()) + len(msg))
                )
        except Exception as err:
            self.status_signal.emit(str(err))

    def get_listView_select_text(self):
        if self.listWidget.count() == 0:
            return ''
        return self.listWidget.currentItem().text()

    def save_file_name(self, data):
        try:
            with open(
                self.lineEdit_Recv_File_Path.text(), 'a', encoding='gbk'
            ) as file:
                file.write(data)
        except Exception as err:
            self.status_signal.emit(str(err))