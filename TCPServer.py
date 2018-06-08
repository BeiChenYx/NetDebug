import os
import configparser

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from UI.ui_TCPServer import Ui_Form
from Single import SingleSend
from SendList import SendList
from selector_handle import TCPServerWorkThread


class TcpServer(QtWidgets.QWidget, Ui_Form):

    status_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(TcpServer, self).__init__(parent)
        self.setupUi(self)
        self.initUi()
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
    
    def initUi(self):
        self.tabWidget.clear()
        self.single_send = SingleSend(self)
        self.send_list = SendList(self)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidget(self.send_list)
        self.tabWidget.addTab(self.single_send, '单条发送')
        self.tabWidget.addTab(self.scrollArea, '多条发送')

        self.single_send.status_signal.connect(
            self.status_signal
        )

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
                self.checkBox_Recv_To_File.setChecked(
                    tcp_server['readtofile'] == 'True'
                )
                self.lineEdit_Recv_File_Path.setText(
                    tcp_server['readtofilepath']
                )
                self.checkBox_Input_Hex.setChecked(
                    tcp_server['hexinput'] == 'True'
                )
                self.lineEdit_Input_File_Path.setText(
                    tcp_server['inputFromfile']
                )

                self.single_send.initConfig()
        except Exception as err:
            self.status_signal.emit(str(err))

    def update_config(self):
        config = configparser.ConfigParser()
        config['TCPServer'] = {
            'localip': self.lineEdit_IP.text(),
            'localport': self.lineEdit_Port.text(),
            'displayrecvetime': str(self.checkBox_Display_Time.isChecked()),
            'hexdisplay': str(self.checkBox_Display_Hex.isChecked()),
            'pause': str(self.checkBox_Pause_Display.isChecked()),
            'readtofile': str(self.checkBox_Recv_To_File.isChecked()),
            'readtofilepath': self.lineEdit_Recv_File_Path.text(),
            'hexinput': str(self.checkBox_Input_Hex.isChecked()),
            'inputFromfile': self.lineEdit_Input_File_Path.text(),
        }
        with open(self._config_path, 'w', encoding='utf-8') as fi:
            config.write(fi)

    def initConnect(self):
        self.pushButton_Connect.clicked.connect(
            self.on_pushButton_Connect
        )
        self.pushButton_Clear_Recv.clicked.connect(
            self.on_pushButton_Clear_display
        )
    
    def on_pushButton_Connect(self):
        if self.pushButton_Connect.text() == '连接':
            self.tcp_server = TCPServerWorkThread(
                self.lineEdit_IP.text(),
                int(self.lineEdit_Port.text())
            )
            self.tcp_server.dataSignal.connect(
                self.on_workData
            )
            self.tcp_server.statusSignal.connect(
                self.on_workStatus
            )
            self.tcp_server.start()
        else:
            self.tcp_server.exitTCPServer()
            self.tcp_server.quit()
            self.tcp_server.wait(1000)
    
    def on_workData(self, data):
        if self.checkBox_Pause_Display.isChecked():
            return
        if len(self.textEdit.toPlainText()) > 4096:
            self.textEdit.clear()

        if self.checkBox_Display_Hex.isChecked():
            data_list = list(map(lambda x: '%02X' % x, data))
            self.textEdit.moveCursor(QtGui.QTextCursor.End)
            self.textEdit.insertPlainText(
                ' '.join(data_list) + ' '
            )
        else:
            self.textEdit.moveCursor(QtGui.QTextCursor.End)
            self.textEdit.insertPlainText(data.decode('gbk', 'ignore'))

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
        cmd, message = msg.split('-')
        self.handle_workStatus(int(cmd), message)

    def handle_workStatus(self, cmd, msg):
        self.cmd_status_func_dict[cmd](msg)

    def info_status(self, msg):
        self.status_signal.emit(msg)
    
    def client_connect(self, msg):
        """
        msg:  "('127.0.0.1', 8000)"
        """
        client_info = eval(msg)
        info = client_info[0] + ':' + str(client_info[1])
        self._clients.append(info)

    def client_close(self, msg):
        client_info = eval(msg)
        self._clients.remove(
            client_info[0] + ':' + str(client_info[1])
        )
    
    def server_start(self, msg):
        self.status_signal.emit(msg)
        self.pushButton_Connect.setText('关闭')

    def server_close(self, msg):
        self.status_signal.emit(msg)
        self.pushButton_Connect.setText('连接')
        print('服务器关闭')

    def on_pushButton_Clear_display(self):
        self.textEdit.clear()

    def update_listWidget(self):
        """
        更新listView，如果self._clients为空则全都删除
        """
        self.listWidget.clear()
        self.listWidget.addItems(self._clients)
    
    def get_listView_select_text(self):
        return self.listWidget.currentItem().text()
    


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = TcpServer(widget)
    widget.show()
    sys.exit(app.exec_())
