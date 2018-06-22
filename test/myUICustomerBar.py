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
        self._padding = 5
        
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

    def resizeEvent(self, event):
        # 重新调整边界范围以备实现鼠标拖放缩放窗口大小，采用三个列表生成式生成三个列表
        self._right_rect = [QtCore.QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                            for y in range(1, self.height() - self._padding)]
        self._bottom_rect = [QtCore.QPoint(x, y) for x in range(1, self.width() - self._padding)
                             for y in range(self.height() - self._padding, self.height() + 1)]
        self._corner_rect = [QtCore.QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                             for y in range(self.height() - self._padding, self.height() + 1)]
        self._left_drag_rect = [QtCore.QPoint(x, y) for x in range(self._padding) 
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
        elif (event.button() == QtCore.Qt.LeftButton and 
            event.y() < self.myBar.height()):
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        # 判断鼠标位置切换鼠标手势
        # if event.pos() in self

        if QtCore.Qt.LeftButton and self.m_flag:
            # print('m_Position: ', self.m_Position)
            self.move(event.globalPos() - self.m_Position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_flag = False
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QMainWindow()
    ui = MyUICustomerBar()
    ui.setupUi(widget)
    ui.show()
    sys.exit(app.exec_())
