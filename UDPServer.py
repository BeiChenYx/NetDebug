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
            self.textEdit.insertPlainText(' '.join(data_list) + ' ' + date_time)
            if self.checkBox_Recv_To_File.isChecked():
                self.save_file_name(' '.join(data_list) + ' ' + date_time)
        else:
            self.textEdit.insertPlainText(data.decode('gbk', 'ignore') + date_time)
            if self.checkBox_Recv_To_File.isChecked():
                self.save_file_name(data.decode('gbk', 'ignore') + date_time)

    def on_workStatus(self, msg):
        cmd, message = msg.split('-')
        self.handle_workStatus(int(cmd), message)

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
        addr = self.get_listView_select_text()
        if addr != '':
            self.udp_server.sendData(addr, msg)
            self.label_TX.setText(
                str(int(self.label_TX.text()) + len(msg))
            )

    def get_listView_select_text(self):
        if self.listWidget.count() == 0:
            return ''
        return self.listWidget.currentItem().text()

    def save_file_name(self, data):
        with open(
            self.lineEdit_Recv_File_Path.text(), 'a', encoding='gbk'
        ) as file:
            file.write(data)