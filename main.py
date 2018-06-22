from PyQt5 import QtCore, QtGui, QtWidgets


from TCPServer import TcpServer
from TCPClients import TcpClients
from UDPServer import UdpServer
from UDPClients import UdpClients


class QTitleLabel(QtWidgets.QLabel):
    """
    新建标题栏标签类
    """

    def __init__(self, *args):
        super(QTitleLabel, self).__init__(*args)
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.setFixedHeight(30)


class QTitleButton(QtWidgets.QPushButton):
    """
    新建标题栏按钮类
    """

    def __init__(self, *args):
        super(QTitleButton, self).__init__(*args)
        # 特殊字体以不借助图片实现最小化最大化和关闭按钮
        self.setFont(QtGui.QFont("Webdings"))  
        self.setFixedWidth(40)

    
class NetDebugMain(QtWidgets.QWidget):
    """
    无边框窗口类
    """

    def __init__(self):
        # 设置为顶级窗口，无边框
        super(NetDebugMain, self).__init__(
            None, QtCore.Qt.FramelessWindowHint)  
        # 设置边界宽度为5
        self._padding = 5  
        self._minWidth = 500
        self._minHeight = 500
        self.setMinimumSize(QtCore.QSize(
            self._minWidth, self._minHeight)
        )
        self.init_ui()
        self.resize(self._minWidth, self._minHeight)
        
        with open("./NetDebug.qss", 'r', encoding='gbk') as fi:
            sheet = fi.read()
            self.setStyleSheet(sheet)

    def init_ui(self):
        self.init_top_bar()
        self.init_side_bar()
        self._main_widget = QtWidgets.QWidget(self)
        self._right_vlayout = QtWidgets.QVBoxLayout()
        self._right_vlayout.addLayout(self._top_bar_hlayout)
        self._right_vlayout.addWidget(self._main_widget)

        self._main_Hlayout = QtWidgets.QHBoxLayout(self)
        self._main_Hlayout.addWidget(self._side_widget)
        self._main_Hlayout.addLayout(self._right_vlayout)
        self.setLayout(self._main_Hlayout)
        

    def init_top_bar(self):
        """
        添加标题图片，标题，标题最小化，最大化，关闭
        按钮，设置标题样式
        """
        self._top_bar_hlayout = QtWidgets.QHBoxLayout()
        self._min_button = QTitleButton(b'\xef\x80\xb0'.decode("utf-8"))
        self._max_button = QTitleButton(b'\xef\x80\xb1'.decode("utf-8"))
        self._close_button = QTitleButton(b'\xef\x81\xb2'.decode("utf-8"))
        self._min_button.setObjectName("MinMaxButton")
        self._max_button.setObjectName("MinMaxButton")
        self._close_button.setObjectName("CloseButton")

        self._top_bar_hlayout.addStretch()
        self._top_bar_hlayout.addWidget(self._min_button)
        self._top_bar_hlayout.addWidget(self._max_button)
        self._top_bar_hlayout.addWidget(self._close_button)
        self._top_bar_hlayout.setSpacing(0)

        self._min_button.setMouseTracking(True)
        self._max_button.setMouseTracking(True)
        self._close_button.setMouseTracking(True)

        self._close_button.clicked.connect(self.close)

    def init_side_bar(self):
        """
        添加侧边栏
        """
        self._tcp_sever_button = QtWidgets.QPushButton('TS')
        self._tcp_clients_button = QtWidgets.QPushButton('TC')
        self._udp_sever_button = QtWidgets.QPushButton('US')
        self._udp_clients_button = QtWidgets.QPushButton('UC')
        self._help_button = QtWidgets.QPushButton('Help')
        self._set_button = QtWidgets.QPushButton('Set')

        self._tcp_sever_button.setFixedSize(QtCore.QSize(40, 40))
        self._tcp_clients_button.setFixedSize(QtCore.QSize(40, 40))
        self._udp_sever_button.setFixedSize(QtCore.QSize(40, 40))
        self._udp_clients_button.setFixedSize(QtCore.QSize(40, 40))
        self._help_button.setFixedSize(QtCore.QSize(40, 40))
        self._set_button.setFixedSize(QtCore.QSize(40, 40))

        self._tcp_sever_button.setMouseTracking(True)
        self._tcp_clients_button.setMouseTracking(True)
        self._udp_sever_button.setMouseTracking(True)
        self._udp_clients_button.setMouseTracking(True)
        self._help_button.setMouseTracking(True)
        self._set_button.setMouseTracking(True)

        self._side_widget = QtWidgets.QWidget()
        self._side_widget.setObjectName('SideWidget')
        self._side_bar_Vlayout = QtWidgets.QVBoxLayout()
        self._side_bar_Vlayout.addWidget(self._tcp_sever_button)
        self._side_bar_Vlayout.addWidget(self._tcp_clients_button)
        self._side_bar_Vlayout.addWidget(self._udp_sever_button)
        self._side_bar_Vlayout.addWidget(self._udp_clients_button)
        self._side_bar_Vlayout.addStretch()
        self._side_bar_Vlayout.addWidget(self._help_button)
        self._side_bar_Vlayout.addWidget(self._set_button)
        self._side_bar_Vlayout.setSpacing(0)
        self._side_widget.setLayout(self._side_bar_Vlayout)



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open("./NetDebug.qss").read())
    widget = QtWidgets.QWidget()
    ui = NetDebugMain()
    ui.show()
    sys.exit(app.exec_())
