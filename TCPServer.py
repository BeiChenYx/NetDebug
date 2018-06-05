import os
import configparser

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from UI.ui_TCPServer import Ui_Form
from Single import SingleSend
from SendList import SendList


class TcpServer(QtWidgets.QWidget, Ui_Form):

    status_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(TcpServer, self).__init__(parent)
        self.setupUi(self)
        self.initUi()
        self._config_path = './NetDebug.ini'
    
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


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = TcpServer(widget)
    widget.show()
    sys.exit(app.exec_())
