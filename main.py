import configparser


from PyQt5 import QtCore, QtGui, QtWidgets


from TCPServer import TcpServer
from TCPClients import TcpClients
from UDPServer import UdpServer
from UDPClients import UdpClients
from help import Help


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
        self.setFixedHeight(20)

    
class NetDebugMain(QtWidgets.QWidget):
    """
    无边框窗口类
    """

    index_button = QtCore.pyqtSignal(int)

    def __init__(self):
        # 设置为顶级窗口，无边框
        super(NetDebugMain, self).__init__(
            None, QtCore.Qt.FramelessWindowHint)  
        self.setObjectName('main')
        # 设置边界宽度
        self._padding = 5  
        self._minWidth = 700
        self._minHeight = 600
        self.setMinimumSize(QtCore.QSize(
            self._minWidth, self._minHeight)
        )
        self.setMouseTracking(True)
        self._config_path = './NetDebug.ini'
        self.init_ui()
        self.init_connections()
        self.resize(self._minWidth, self._minHeight)
        self.initDrag()
        self.initConfig()
        
        with open("./NetDebug.qss", 'r', encoding='gbk') as fi:
            sheet = fi.read()
            self.setStyleSheet(sheet)
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.on_timer_out)

    def initDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False
        self._left_drag = False
        self._top_drag = False
        self._top_right_corner_drag = False
        self._top_left_corner_drag = False
        self._bottom_left_corner_drag = False

    def init_connections(self):
        self._min_button.clicked.connect(self.showMinimized)
        self._max_button.clicked.connect(self._changeNormalButton)
        self._close_button.clicked.connect(self.close)

        # 添加功能页面信号槽
        self.tcp_server.status_signal.connect(
            self.status_show
        )
        self.tcp_clients.status_signal.connect(
            self.status_show
        )
        self.udp_server.status_signal.connect(
            self.status_show
        )
        self.udp_clients.status_signal.connect(
            self.status_show
        )
        self.index_button.connect(self._main_widget.setCurrentIndex)
        self._tcp_sever_button.clicked.connect(self.on_tcp_server_button)
        self._tcp_clients_button.clicked.connect(self.on_tcp_clients_button)
        self._udp_sever_button.clicked.connect(self.on_udp_server_button)
        self._udp_clients_button.clicked.connect(self.on_udp_clients_button)
        self._help_button.clicked.connect(self.on_help_button)
        self._about_button.clicked.connect(self.on_about_button)

    
    def on_tcp_server_button(self):
        self.index_button.emit(self._index_widget[self.tcp_server])
    def on_tcp_clients_button(self):
        self.index_button.emit(self._index_widget[self.tcp_clients])
    def on_udp_server_button(self):
        self.index_button.emit(self._index_widget[self.udp_server])
    def on_udp_clients_button(self):
        self.index_button.emit(self._index_widget[self.udp_clients])
    def on_help_button(self):
        self.index_button.emit(self._index_widget[self.help])
    def on_about_button(self):
        QtWidgets.QMessageBox.about(self, '版本信息', '网络调试工具 V1.0.0')

    def init_ui(self):
        self.init_top_bar()
        self.init_side_bar()
        self._main_widget = QtWidgets.QStackedWidget(self)
        self._right_vlayout = QtWidgets.QVBoxLayout()
        self._right_vlayout.addLayout(self._top_bar_hlayout)
        self._right_vlayout.addWidget(self._main_widget)
        self._status_label = QtWidgets.QLabel(self)
        self._status_label.setIndent(10)
        self._status_label.setMinimumHeight(16)
        self._right_vlayout.addWidget(self._status_label)
        self._right_vlayout.setSpacing(0)
        self._right_vlayout.setContentsMargins(0, 0, 0, 0)

        self._main_Hlayout = QtWidgets.QHBoxLayout(self)
        self._main_Hlayout.addWidget(self._side_widget)
        self._main_Hlayout.addLayout(self._right_vlayout)
        self._main_Hlayout.setSpacing(0)
        self._main_Hlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._main_Hlayout)
        
        self.tcp_server = TcpServer(self)
        self.tcp_clients = TcpClients(self)
        self.udp_server = UdpServer(self)
        self.udp_clients = UdpClients(self)
        self.help = Help(self)
        self._index_widget = {
            self.tcp_server: 0,
            self.tcp_clients: 1,
            self.udp_server: 2,
            self.udp_clients: 3,
            self.help: 4,
        }

        self._main_widget.addWidget(self.tcp_server)
        self._main_widget.addWidget(self.tcp_clients)
        self._main_widget.addWidget(self.udp_server)
        self._main_widget.addWidget(self.udp_clients)
        self._main_widget.addWidget(self.help)
        

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
        self._top_bar_hlayout.setContentsMargins(0, 0, 0, 0)

        self._min_button.setMouseTracking(True)
        self._max_button.setMouseTracking(True)
        self._close_button.setMouseTracking(True)

    def init_side_bar(self):
        """
        添加侧边栏
        """
        self._title_img = QtWidgets.QLabel('img')
        self._title_img.setObjectName('TitleImg')
        self._tcp_sever_button = QtWidgets.QPushButton('TS')
        self._tcp_clients_button = QtWidgets.QPushButton('TC')
        self._udp_sever_button = QtWidgets.QPushButton('US')
        self._udp_clients_button = QtWidgets.QPushButton('UC')
        self._help_button = QtWidgets.QPushButton('Help')
        self._about_button = QtWidgets.QPushButton('About')

        self._tcp_sever_button.setToolTip('TCP服务器')
        self._tcp_clients_button.setToolTip('TCP客户端')
        self._udp_sever_button.setToolTip('UDP服务器')
        self._udp_clients_button.setToolTip('UDP客户端')
        self._help_button.setToolTip('帮助')
        self._about_button.setToolTip('关于')

        self._title_img.setFixedWidth(32)
        self._tcp_sever_button.setFixedSize(QtCore.QSize(32, 32))
        self._tcp_clients_button.setFixedSize(QtCore.QSize(32, 32))
        self._udp_sever_button.setFixedSize(QtCore.QSize(32, 32))
        self._udp_clients_button.setFixedSize(QtCore.QSize(32, 32))
        self._help_button.setFixedSize(QtCore.QSize(32, 32))
        self._about_button.setFixedSize(QtCore.QSize(32, 32))

        self._title_img.setMouseTracking(True)
        self._tcp_sever_button.setMouseTracking(True)
        self._tcp_clients_button.setMouseTracking(True)
        self._udp_sever_button.setMouseTracking(True)
        self._udp_clients_button.setMouseTracking(True)
        self._help_button.setMouseTracking(True)
        self._about_button.setMouseTracking(True)

        self._img = QtGui.QImage()
        if self._img.load('./images/ico.png'):
            self._title_img.setPixmap(QtGui.QPixmap.fromImage(self._img))
        self._title_img.setScaledContents(True)

        self._side_widget = QtWidgets.QWidget()
        self._side_widget.setObjectName('SideWidget')
        self._side_bar_Vlayout = QtWidgets.QVBoxLayout()
        self._side_bar_Vlayout.addWidget(self._title_img)
        self._side_bar_Vlayout.addWidget(self._tcp_sever_button)
        self._side_bar_Vlayout.addWidget(self._tcp_clients_button)
        self._side_bar_Vlayout.addWidget(self._udp_sever_button)
        self._side_bar_Vlayout.addWidget(self._udp_clients_button)
        self._side_bar_Vlayout.addWidget(self._help_button)
        self._side_bar_Vlayout.addStretch()
        self._side_bar_Vlayout.addWidget(self._about_button)
        self._side_bar_Vlayout.setSpacing(25)
        self._side_bar_Vlayout.setContentsMargins(0, 10, 0, 0)
        self._side_widget.setFixedWidth(60)
        self._side_bar_HlayOut = QtWidgets.QHBoxLayout()
        self._side_bar_HlayOut.addLayout(self._side_bar_Vlayout)
        self._side_widget.setLayout(self._side_bar_HlayOut)

    def _changeNormalButton(self):
        # 切换到恢复窗口大小按钮
        try:
            self.showMaximized()  # 先实现窗口最大化
            self._max_button.setText(
                b'\xef\x80\xb2'.decode("utf-8"))  # 更改按钮文本
            self._max_button.setToolTip("恢复")  # 更改按钮提示
            self._max_button.disconnect()  # 断开原本的信号槽连接
            self._max_button.clicked.connect(
                self._changeMaxButton)  # 重新连接信号和槽
        except:
            pass

    def _changeMaxButton(self):
        # 切换到最大化按钮
        try:
            self.showNormal()
            self._max_button.setText(b'\xef\x80\xb1'.decode("utf-8"))
            self._max_button.setToolTip("最大化")
            self._max_button.disconnect()
            self._max_button.clicked.connect(self._changeNormalButton)
        except:
            pass

    def resizeEvent(self, event):
        """
        自定义窗口调整大小的事件
        """
        # self._right_rect = [QtCore.QPoint(x, y) 
        #     for x in  range(self.x() + self.width() - self._padding, self.x() + self.width())
        #         for y in range(self.y() + self._padding, self.y() + self.height() - self._padding)
        # ]
        self._right_rect = [QtCore.QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
            for y in range(1, self.height() - self._padding)
        ]
        self._bottom_rect = [QtCore.QPoint(x, y) for x in range(1, self.width() - self._padding)
                             for y in range(self.height() - self._padding, self.height() + 1)]
        self._corner_rect = [QtCore.QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                             for y in range(self.height() - self._padding, self.height() + 1)]
        self._left_drag_rect = [QtCore.QPoint(x, y) for x in range(1, self._padding) 
                                for y in range(1, self.height() - self._padding)]
    
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton) and (event.pos() in self._corner_rect):
            # 鼠标左键点击右下角边界区域
            self._corner_drag = True
            event.accept()
        elif (event.button() == QtCore.Qt.LeftButton) and (event.pos() in self._right_rect):
            # 鼠标左键点击右侧边界区域
            self._right_drag = True
            event.accept()
        elif (event.button() == QtCore.Qt.LeftButton) and (event.pos() in self._bottom_rect):
            # 鼠标左键点击下侧边界区域
            self._bottom_drag = True
            event.accept()
        elif (event.button() == QtCore.Qt.LeftButton) and (event.pos() in self._left_drag_rect):
            self._left_drag = True
            event.accept()
        elif (event.button() == QtCore.Qt.LeftButton) and (event.y() < self._min_button.height()):
            # 鼠标左键点击标题栏区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.pos() in self._corner_rect:
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif event.pos() in self._bottom_rect:
            self.setCursor(QtCore.Qt.SizeVerCursor)
        elif event.pos() in self._right_rect:
            self.setCursor(QtCore.Qt.SizeHorCursor)
        elif event.pos() in self._left_drag_rect:
            self.setCursor(QtCore.Qt.SizeHorCursor)
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)

        if QtCore.Qt.LeftButton and self._right_drag:
            # 右侧调整窗口宽度
            self.resize(event.pos().x(), self.height())
            event.accept()
        elif QtCore.Qt.LeftButton and self._left_drag:
            oldx = self.x()
            offsetMouseX = event.pos().x()
            self.resize(self.width() - event.pos().x(), self.height())
            if self.width() > self._minWidth:
                self.move(oldx + offsetMouseX, self.y())
            event.accept()
        elif QtCore.Qt.LeftButton and self._bottom_drag:
            # 下侧调整窗口高度
            self.resize(self.width(), event.pos().y())
            event.accept()
        elif QtCore.Qt.LeftButton and self._corner_drag:
            # 右下角同时调整高度和宽度
            self.resize(event.pos().x(), event.pos().y())
            event.accept()
        elif QtCore.Qt.LeftButton and self._move_drag:
            # 标题栏拖放窗口位置
            self.move(event.globalPos() - self.move_DragPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        # 鼠标释放后，各扳机复位
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False
        self._left_drag = False
        self._top_drag = False
        self._top_left_corner_drag = False
        self._top_right_corner_drag = False
        self._bottom_left_corner_drag = False

    def closeEvent(self, event):
        self.update_config()
        event.accept()

    def initConfig(self):
        self.tcp_server.initConfig()
        self.tcp_clients.initConfig()
        self.udp_server.initConfig()
        self.udp_clients.initConfig()

    def update_config(self):
        config = configparser.ConfigParser()
        config['TCPServer'] = self.tcp_server.update_config()
        config['TCPClients'] = self.tcp_clients.update_config()
        config['UDPServer'] = self.udp_server.update_config()
        config['UDPClients'] = self.udp_clients.update_config()

        with open(self._config_path, 'w', encoding='utf-8') as fi:
            config.write(fi)

    def status_show(self, msg):
        self._status_label.setText(msg)
        self.timer.start(5000)

    def on_timer_out(self):
        self._status_label.clear()
        self.timer.stop()



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open("./NetDebug.qss").read())
    widget = QtWidgets.QWidget()
    ui = NetDebugMain()
    ui.show()
    sys.exit(app.exec_())
