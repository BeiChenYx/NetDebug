from PyQt5 import QtCore, QtGui, QtWidgets
from ui_customerBar import Ui_MainWindow

class MyUICustomerBar(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(MyUICustomerBar, self).__init__(None, QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)

        # 最大化和恢复的标记, False表示正常，True表示最大化
        self._max_status = False
        self.m_flag = False
        self.init_ui()
        self.init_connections()
        self.initDrag()
        
    def initDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False


    def init_ui(self):
        self.ButtonClose.setToolTip('关闭窗口')
        self.ButtonMax.setToolTip('最大化')
        self.ButtonMin.setToolTip('最下化')
        self.ButtonClose.setMouseTracking(True)
        self.ButtonMax.setMouseTracking(True)
        self.ButtonMin.setMouseTracking(True)

    def init_connections(self):
        self.ButtonClose.clicked.connect(self.close)
        self.ButtonMin.clicked.connect(self.showMinimized)
        self.ButtonMax.clicked.connect(self._max_restroe_button)

    def _max_restroe_button(self):
        # 切换到恢复窗口大小按钮
        try:
            if self._max_status:
                self.showNormal()
                self._max_status = False
            else:
                self.showMaximized()
                self._max_status = True
        except Exception as err:
            print(err)

    # def resizeEvent(self, QResizeEvent):
    #     try:
    #         self._right_rect = list()
    #         for x in range(self.width(), )
    #     except Exception as err:
    #         print(err)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            print('press m_flag: ', self.m_flag)
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            # self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        print('m_flag: ', self.m_flag)
        if QtCore.Qt.LeftButton and self.m_flag:
            print('m_Position: ', self.m_Position)
            self.move(event.globalPos() - self.m_Position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_flag = False
        # self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QMainWindow()
    ui = MyUICustomerBar()
    ui.setupUi(widget)
    ui.show()
    sys.exit(app.exec_())
