from enum import Enum

from PyQt5 import QtCore, QtGui, QtWidgets


BUTTON_HEIGHT = 30
BUTTON_WIDTH = 30
TITLE_HEIGHT = 30


class ButtonType(Enum):
    MIN_BUTTON = 0
    MIN_MAX_BUTTON = 1
    ONLY_CLOSE_BUTTON = 2


class MyTitleBar(QtWidgets.QWidget):

    # 按钮触发的信号
    signalButtonMinClicked = QtCore.pyqtSignal()
    signalButtonRestoreClicked = QtCore.pyqtSignal()
    signalButtonMaxClicked = QtCore.pyqtSignal()
    signalButtonCloseClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MyTitleBar, self).__init__(parent)
        self.setupUi(self)

        # 标题栏图标
        self.m_pIcon = QtWidgets.QLabel()
        # 标题栏内容
        self.m_pTitleContent = QtWidgets.QLabel()
        # 最小化按钮
        self.m_pButtonMin = QtWidgets.QPushButton()
        # 最大化还原按钮
        self.m_pButtonRestore = QtWidgets.QPushButton()
        # 最大化还原按钮
        self.m_pButtonMax = QtWidgets.QPushButton()
        # 关闭按钮
        self.m_pButtonClose = QtWidgets.QPushButton()

        # 标题栏背景色
        self.m_colorR = 153
        self.m_colorG = 153
        self.m_colorB = 153

        # 最大化，最小化变量
        self.m_restorePos = QtCore.QPoint()
        self.m_restoreSize = QtCore.QSize()

        # 移动窗口的变量
        self.m_isPressed = False

        # 标题栏跑马灯效果时钟
        self.m_titleRollTimer = QtCore.QTimer()

        # 标题栏内容
        self.m_titleContent = ''

        # 按钮类型
        self.m_buttonType = ButtonType()

        self.initControl()
        self.initConnections()
        self.loadStyleSheet('MyTitle')

    def setBackgroundColor(self, r, g, b):
        """
        设置标题栏背景色
        """
        pass

    def setTitleIcon(self, filePath):
        """
        设置标题栏图标
        """
        pass

    def setTitleContent(self, titleContent):
        """
        设置标题内容
        """
        pass

    def setTitleWidth(self, width):
        """
        设置标题栏长度
        """
        pass

    def setButtonType(self, buttonType):
        """
        设置标题栏上按钮类型
        """
        pass

    def setTitleRoll(self):
        """
        设置标题栏中的标题是否会滚动，具体可以看到效果
        """
        pass

    def saveRestoreInfo(self, point, size):
        """
        保存最大化前窗口的位置和大小
        """
        pass

    def getRestoreInfo(self, point, size):
        """
        获取最大化前窗口的位置和大小
        """
        pass

    def paintEvent(self, event):
        pass

    def mouseDoubleClickEvent(self, event):
        pass

    def mousePressClickEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

    def initControl(self):
        """
        初始化控件
        """
        self.m_pButtonMin.setFixedSize(QtCore.QSize(
            BUTTON_WIDTH, BUTTON_HEIGHT
        ))
        self.m_pButtonRestore.setFixedSize(QtCore.QSize(
            BUTTON_WIDTH, BUTTON_HEIGHT
        ))
        self.m_pButtonMax.setFixedSize(QtCore.QSize(
            BUTTON_WIDTH, BUTTON_HEIGHT
        ))
        self.m_pButtonClose.setFixedSize(QtCore.QSize(
            BUTTON_WIDTH, BUTTON_HEIGHT
        ))

        self.m_pTitleContent.setObjectName("TitleContent")
        self.m_pButtonMin.setObjectName("ButtonMin")
        self.m_pButtonRestore.setObjectName("ButtonRestore")
        self.m_pButtonMax.setObjectName("ButtonMax")
        self.m_pButtonClose.setObjectName("ButtonClose")

        self.mylayout = QtWidgets.QHBoxLayout(self)
        self.mylayout.addWidget(self.m_pIcon)
        self.mylayout.addWidget(self.m_pTitleContent)

        self.mylayout.addWidget(self.m_pButtonMin)
        self.mylayout.addWidget(self.m_pButtonRestore)
        self.mylayout.addWidget(self.m_pButtonMax)
        self.mylayout.addWidget(self.m_pButtonClose)

        self.mylayout.setContentsMargins(5, 0, 0, 0)
        self.mylayout.setSpacing(0) 

        self.m_pTitleContent.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(TITLE_HEIGHT)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def initConnections(self):
        """
        信号槽的绑定
        """
        pass

    def loadStyleSheet(self, sheetName):
        """
        加载样式文件
        """
        pass

    # 按钮触发的槽
    def onButtonMinClicked(self):
        pass
    def onButtonRestoreClicked(self):
        pass
    def onButtonMaxClicked(self):
        pass
    def onButtonCloseClicked(self):
        pass
    def onRollTitle(self):
        pass

