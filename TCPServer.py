import os
import time
import configparser

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from UI.ui_TCPServer import Ui_Form
from Single import SingleSend
from selector_handle import TCPServerWorkThread


class TcpServer(QtWidgets.QWidget, Ui_Form):

    status_signal = QtCore.pyqtSignal(str)
    def __init__(self, parent):
        super(TcpServer, self).__init__(parent)
        self.setupUi(self)
        self.init_ui()
        self._config_path = './NetDebug.ini'
        self.initConnect()
        self.cmd_status_func_dict = {
            0: self.info_status,
            1: self.client_connect,
            2: self.client_close,
            3: self.server_start,
            4: self.server_close,
        }
        self._clients = list()

    def init_ui(self):
        self.single = SingleSend(self)
        self.tabWidget.addTab(self.single, '发送数据')
        self.tabWidget.setCurrentIndex(0)

    def initConfig(self):
        config = configparser.ConfigParser()
        try:
            if os.path.exists(self._config_path):
                config.read(self._config_path) 
                tcp_server = config['TCPServer']
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
                self.lineEdit_Recv_File_Path.setText(
                    tcp_server['readtofilepath']
                )
                self.single.initConfig(tcp_server)
        except Exception as err:
            self.status_signal.emit(str(err))

    def update_config(self):
        config = {
            'localip': self.lineEdit_IP.text(),
            'localport': self.lineEdit_Port.text(),
            'displayrecvetime': str(self.checkBox_Display_Time.isChecked()),
            'hexdisplay': str(self.checkBox_Display_Hex.isChecked()),
            'pause': str(self.checkBox_Pause_Display.isChecked()),
            'readtofilepath': self.lineEdit_Recv_File_Path.text(),
        }
        config.update(self.single.update_config())
        return config

    def initConnect(self):
        self.pushButton_Clear_Recv.clicked.connect(
            self.on_pushButton_Clear_display
        )
        self.pushButton_Clear_Count.clicked.connect(
            self.on_pushButton_clear_count
        )
        self.pushButton_Connect.clicked.connect(self.on_pushButton_Connect)
        self.single.data_signal.connect(self.sendData)
        self.single.status_signal.connect(self.status_signal)
        self.checkBox_Recv_To_File.stateChanged.connect(self.on_to_file)
        self.checkBox_Display_Hex.stateChanged.connect(self.on_check_hex)

    def on_pushButton_Connect(self):
        if self.pushButton_Connect.text() == '连接':
            if self.lineEdit_IP.text() == '' or self.lineEdit_Port.text() == '':
                return
            self.tcp_server = TCPServerWorkThread(
                self.lineEdit_IP.text(), int(self.lineEdit_Port.text())
            )
            self.tcp_server.dataSignal.connect(self.on_workData)
            self.tcp_server.statusSignal.connect(self.on_workStatus)
            self.tcp_server.start()
        else:
            self.tcp_server.exitTCPServer()
            self.tcp_server.quit()
            self.tcp_server.wait(1000)
    
    def on_workData(self, addr, data):
        if self.checkBox_Pause_Display.isChecked():
            return
        
        if self.pushButton_Connect.text() == '连接':
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
        """
        msg格式:
            cmd-message
            cmd:
                0: info_status      普通状态栏消息
                1: client_connect   客户端连接信息
                2: client_close     客户端关闭信息
                3: server_start     服务器开启的信息
                4: server_close     服务器关闭的信息
        """
        try:
            cmd, message = msg.split('-')
            self.handle_workStatus(int(cmd), message)
        except Exception as err:
            self.status_signal.emit(str(err))

    def handle_workStatus(self, cmd, msg):
        self.cmd_status_func_dict[cmd](msg)

    def info_status(self, msg):
        self.status_signal.emit(msg)
    
    def client_connect(self, msg):
        """
        msg:  "127.0.0.1:8000"
        """
        self._clients.append(msg)
        self.update_listWidget()

    def client_close(self, msg):
        self._clients.remove(msg)
        self.update_listWidget()
    
    def server_start(self, msg):
        self.status_signal.emit(msg)
        self.pushButton_Connect.setText('关闭')

    def server_close(self, msg):
        self.status_signal.emit(msg)
        self.pushButton_Connect.setText('连接')
        self._clients.clear()
        self.update_listWidget()

    def on_pushButton_Clear_display(self):
        self.textEdit.clear()

    def update_listWidget(self):
        """
        更新listView，如果self._clients为空则全都删除
        """
        self.listWidget.clear()
        self.listWidget.addItems(self._clients)
        self.listWidget.setCurrentRow(0)
    
    def get_listView_select_text(self):
        if self.listWidget.count() == 0:
            return ''
        return self.listWidget.currentItem().text()
    
    def sendData(self, msg):
        try:
            if self.pushButton_Connect.text() == '连接':
                return
            addr = self.get_listView_select_text()
            if addr != '':
                self.tcp_server.send_data(addr, msg)
                self.label_TX.setText(
                    str(int(self.label_TX.text()) + len(msg))
                )
        except Exception as err:
            self.status_signal.emit(str(err))

    def on_pushButton_clear_count(self):
        self.label_RX.setText('0')
        self.label_TX.setText('0')

    def on_to_file(self, state):
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

    def get_date_time(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]:\n', time.localtime())

    def save_file_name(self, data):
        try:
            with open(
                self.lineEdit_Recv_File_Path.text(), 'a', encoding='gbk'
            ) as file:
                file.write(data)
        except Exception as err:
            self.status_signal.emit(str(err))

    def on_check_hex(self):
        try:
            data = self.textEdit.toPlainText().strip()
            if not data:
                return
            if self.checkBox_Display_Hex.isChecked():
                data_temp = ' '.join('%02X' % ord(c) for c in data)
            else:
                data_temp = ''.join(chr(int(h, 16)) for h in data.split(' '))
            self.textEdit.clear()
            self.textEdit.insertPlainText(data_temp)
        except Exception as err:
            self.status_signal.emit(str(err))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = TcpServer(widget)
    widget.show()
    sys.exit(app.exec_())
