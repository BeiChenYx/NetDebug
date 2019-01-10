import os
import time
import configparser

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from UI.ui_UDPServer import Ui_Form
from selector_udp_server_handle import UDPServerWorkThread
from selector_udp_clients_handle import UdpClientsWorkThread


class UdpServer(QtWidgets.QWidget, Ui_Form):

    status_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(UdpServer, self).__init__(parent)
        self.setupUi(self)
        self._config_path = './NetDebug.ini'
        self.timer = QtCore.QTimer(self)
        self.init_connect()
        self._clients = list()
        self.cmd_status_func_dict = {
            0: self.info_status,
            1: self.server_start,
            2: self.server_close,
            3: self.client_start,
            4: self.client_close,
        }

    def init_connect(self):
        self.pushButton_Connect.clicked.connect(self.on_pushButton_Connect)
        self.pushButton_Clear_Recv.clicked.connect(self.on_pushButton_Clear_display)
        self.pushButton_Clear_Count.clicked.connect(self.on_pushButton_clear_count)
        self.checkBox_Recv_To_File.stateChanged.connect(self.on_to_file)
        self.timer.timeout.connect(self.on_timer_out)
        self.checkBox_times_client.stateChanged.connect(self.on_check_Timers)
        self.checkBox_hex_client.stateChanged.connect(self.on_check_hex)
        self.pushButton_create.clicked.connect(self.on_button_client_create)
        self.pushButton_send_client.clicked.connect(self.on_button_send_client)

    def initConfig(self):
        config = configparser.ConfigParser()
        try:
            if os.path.exists(self._config_path):
                config.read(self._config_path) 
                udp_server = config['UDPServer']
                self.lineEdit_IP.setText(udp_server['localip'])
                self.lineEdit_Port.setText(udp_server['localport'])
                self.checkBox_Display_Time.setChecked(
                    udp_server['displayrecvetime'] == 'True'
                )
                self.checkBox_Display_Hex.setChecked(udp_server['hexdisplay'] == 'True')
                self.checkBox_Pause_Display.setChecked(udp_server['pause'] == 'True')
                self.checkBox_Recv_To_File.setChecked(udp_server['readtofile'] == 'True')
                self.lineEdit_Recv_File_Path.setText(udp_server['readtofilepath'])

                self.lineEdit_ip_client.setText(udp_server['ipclient'])
                self.lineEdit_port_client.setText(udp_server['portclient'])
                self.lineEdit_clinet_counts.setText(udp_server['countclient'])
                self.checkBox_hex_client.setChecked(udp_server['hexclient'] == 'True')
                self.checkBox_times_client.setChecked(udp_server['timesclient'] == 'True')
                self.lineEdit_times_client.setText(udp_server['times'])
                self.textEdit_send_client.setText(udp_server['bufclient'])
        except Exception as err:
            self.status_signal.emit(str(err))

    def update_config(self):
        config = {
            'localip': self.lineEdit_IP.text(),
            'localport': self.lineEdit_Port.text(),
            'displayrecvetime': str(self.checkBox_Display_Time.isChecked()),
            'hexdisplay': str(self.checkBox_Display_Hex.isChecked()),
            'pause': str(self.checkBox_Pause_Display.isChecked()),
            'readtofile': str(self.checkBox_Recv_To_File.isChecked()),
            'readtofilepath': self.lineEdit_Recv_File_Path.text(),
            'ipclient': self.lineEdit_ip_client.text(),
            'portclient': self.lineEdit_port_client.text(),
            'countclient': self.lineEdit_clinet_counts.text(),
            'hexclient': str(self.checkBox_hex_client.isChecked()),
            'timesclient': str(self.checkBox_times_client.isChecked()),
            'times': self.lineEdit_times_client.text(),
            'bufclient': self.textEdit_send_client.toPlainText(),
        }
        return config

    def on_pushButton_Connect(self):
        if self.pushButton_Connect.text() == '连接':
            if self.lineEdit_IP.text() == '' or self.lineEdit_Port.text() == '':
                return
            self.udp_server = UDPServerWorkThread(
                self.lineEdit_IP.text(),
                int(self.lineEdit_Port.text())
            )
            self.udp_server.dataSignal.connect(self.on_workData)
            self.udp_server.statusSignal.connect(self.on_workStatus)
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

        date_time = self.get_date_time()
        self.label_RX.setText(str(int(self.label_RX.text()) + len(data)))
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        if self.checkBox_Display_Hex.isChecked():
            data_list = list(map(lambda x: '%02X' % x, data))
            if self.checkBox_Display_Time.isChecked():
                data_display = date_time + ' '.join(data_list) + '\n'
            else:
                data_display = ' '.join(data_list) + ' '
        else:
            if self.checkBox_Display_Time.isChecked():
                data_display = date_time + data.decode('gbk', 'ignore') + '\n'
            else:
                data_display = data.decode('gbk', 'ignore')

        self.textEdit.insertPlainText(data_display)
        if self.checkBox_Recv_To_File.isChecked():
            self.save_file_name(data_display)

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
            if file_name == '':
                self.checkBox_Recv_To_File.setCheckState(QtCore.Qt.Unchecked)
            else:
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

    def on_button_client_create(self):
        """udp客户端创建槽"""
        if self.pushButton_create.text() == '创建':
            ip = self.lineEdit_ip_client.text()
            port = int(self.lineEdit_port_client.text())
            count = int(self.lineEdit_clinet_counts.text())
            self.udp_client = UdpClientsWorkThread(ip, port, count)
            self.udp_client.statusSignal.connect(self.on_workStatus)
            self.udp_client.start()
        else:
            self.udp_client.status_signal.disconnect()
            self.udp_client.exitUdpWorkThread()
            self.udp_client.quit()
            self.udp_client.wait(1000)

    def client_start(self, msg):
        self.status_signal.emit(msg)
        self.pushButton_create.setText('关闭')

    def client_close(self, msg):
        self.status_signal.emit(msg)
        self.pushButton_create.setText('创建')

    def on_button_send_client(self):
        """udp客户端数据发送按钮的槽"""
        if self.pushButton_create.text() == '创建':
            return
        msg = self.handle_data()
        if msg == None:
            return
        self.udp_client.sendData(msg)
        self.label_TX.setText(str(int(self.label_TX.text()) + len(msg)))

    def on_check_hex(self):
        try:
            data = self.textEdit_send_client.toPlainText().strip()
            if not data:
                return
            if self.checkBox_hex_client.isChecked():
                data_temp = ' '.join('%02X' % ord(c) for c in data)
            else:
                data_temp = ''.join(chr(int(h, 16)) for h in data.split(' '))
            self.textEdit_send_client.clear()
            self.textEdit_send_client.insertPlainText(data_temp)
        except Exception as err:
            self.status_signal.emit(str(err))

    def on_check_Timers(self):
        if self.lineEdit_times_client.text() == '':
            self.status_signal.emit('循环间隔不能为空')
            return
        if self.checkBox_times_client.isChecked():
            try:
                self.timer.start(int(self.lineEdit_times_client.text()))
            except Exception as err:
                self.status_signal.emit(str(err))
        else:
            self.timer.stop()

    def handle_data(self):
        """
        生成需要发送的数据
        """
        msg = self.textEdit_send_client.toPlainText()
        if self.checkBox_hex_client.isChecked():
            try:
                data = msg.split(' ')
                return bytes(list(map(lambda x: int(x, 16), data)))
            except Exception:
                self.status_signal.emit('16进制正确格式: 0A 0B 0C 15')
                return None
        else:
            return msg.encode('gbk')

    def on_push_button_clicked(self):
        msg = self.handle_data()
        if msg == None:
            return
        self.data_signal.emit(msg)

    def on_timer_out(self):
        self.on_button_send_client()
