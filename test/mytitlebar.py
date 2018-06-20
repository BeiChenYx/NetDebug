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
        self.m_startMovePos = QtCore.QPoint()

        # 标题栏跑马灯效果时钟
        self.m_titleRollTimer = QtCore.QTimer()

        # 标题栏内容
        self.m_titleContent = ''

        # 按钮类型
        self.m_buttonType = ButtonType()

        # 标题栏中的标题滚动的位置
        self._nPos = 0

        self.initControl()
        self.initConnections()
        self.loadStyleSheet('MyTitle')

    def setBackgroundColor(self, r, g, b):
        """
        设置标题栏背景色
        """
        self.m_colorR = r
        self.m_colorG = g
        self.m_colorB = b
        self.update()

    def setTitleIcon(self, filePath):
        """
        设置标题栏图标
        """
        titleIcon = QtGui.QPixmap(filePath)
        # 设置图标，并缩放
        self.m_pIcon.setPixmap(titleIcon.scaled(25, 25))

    def setTitleContent(self, titleContent):
        """
        设置标题内容
        """
        self.m_pTitleContent.setText(titleContent)
        self.m_titleContent = titleContent

    def setTitleWidth(self, width):
        """
        设置标题栏长度
        """
        self.setFixedWidth(width)

    def setButtonType(self, buttonType):
        """
        设置标题栏上按钮类型
        """
        self.m_buttonType = buttonType
        if buttonType == ButtonType.MIN_BUTTON:
            self.m_pButtonRestore.setVisible(False)
            self.m_pButtonMax.setVisible(False)
        elif buttonType == ButtonType.MIN_MAX_BUTTON:
            self.m_pButtonRestore.setVisible(False)
        elif buttonType == ButtonType.ONLY_CLOSE_BUTTON:
            self.m_pButtonRestore.setVisible(False)
            self.m_pButtonMax.setVisible(False)
            self.m_pButtonMin.setVisible(False) 
        else:
            pass

    def setTitleRoll(self):
        """
        设置标题栏中的标题是否会滚动，具体可以看到效果
        """
        self.m_titleRollTimer.timeout.connect(
            self.onRollTitle
        )
        self.m_titleRollTimer.start(200)

    def saveRestoreInfo(self, point, size):
        """
        保存最大化前窗口的位置和大小
        """
        self.m_restorePos = point
        self.m_restoreSize = size

    def getRestoreInfo(self):
        """
        获取最大化前窗口的位置和大小
        """
        return (self.m_restorePos, self.m_restoreSize)

    def paintEvent(self, event):
        """
        绘制标题栏背景色
        """
        painter = QtGui.QPainter(self)
        pathBack = QtGui.QPainterPath()
        pathBack.setFillRule(QtCore.Qt.WindingFill)
        pathBack.addRoundedRect(
            QtCore.QRect(0, 0, self.width(), self.height()),
            3, 3
        )
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        painter.fillPath(
            pathBack,
            QtGui.QBrush(QtGui.QColor(
                self.m_colorR, self.m_colorG, self.m_colorB
            ))
        )
        # 当窗口最大化或者还原后，窗口长度变了，标题的长度应该一起改变
        if self.width() != self.parentWidget().width():
            self.setFixedWidth(self.parentWidget().width())

        return QtWidgets.QWidget.paintEvent(event)

    def mouseDoubleClickEvent(self, event):
        """
        双击响应事件，主要实现双击标题栏进行最大化和还原的操作
        """
        if self.m_buttonType == ButtonType.MIN_MAX_BUTTON:
            # 通过最大化按钮的状态判断当前窗口是处于最大化还是
            # 原始大小状态或者通过单独设置变量来表示当前窗口状态
            if self.m_pButtonMax.isVisible():
                self.onButtonMaxClicked()
            else:
                self.onButtonRestoreClicked()

        return QtWidgets.QWidget.mouseDoubleClickEvent(event)

    def mousePressClickEvent(self, event):
        """
        通过mousePressEvent, mouseMoveEvent,mouseReleaseEvent
        三个事件来实现鼠标拖动标题栏移动窗口的效果
        """
        if self.m_buttonType == ButtonType.MIN_MAX_BUTTON:
            # 窗口最大化时禁止拖动窗口
            if self.m_pButtonMax.isVisible():
                self.m_isPressed = True
                self.m_startMovePos = event.globalPos()
        else:
            self.m_isPressed = True
            self.m_startMovePos = event.globalPos()
        return QtWidgets.QWidget.mousePressEvent()

    def mouseMoveEvent(self, event):
        """
        通过mousePressEvent, mouseMoveEvent,mouseReleaseEvent
        三个事件来实现鼠标拖动标题栏移动窗口的效果
        """
        if self.m_isPressed:
            movePoint = event.globalPos() - self.m_startMovePos
            widgetPos = self.parentWidget.pos()
            self.m_startMovePos = event.globalPos()
            self.parentWidget().move(
                widgetPos.x() + movePoint.x(),
                widgetPos.y() + movePoint.y()
            )
        return QtWidgets.QWidget.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        通过mousePressEvent, mouseMoveEvent,mouseReleaseEvent
        三个事件来实现鼠标拖动标题栏移动窗口的效果
        """
        self.m_isPressed = False
        return QtWidgets.QWidget.mouseReleaseEvent(event)

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
        self.m_pButtonMin.clicked.connect(
            self.onButtonMinClicked
        )
        self.m_pButtonRestore.clicked.connect(
            self.onButtonRestoreClicked
        )
        self.m_pButtonMax.clicked.connect(
            self.onButtonMaxClicked
        )
        self.m_pButtonClose.clicked.connect(
            self.onButtonCloseClicked
        )

    def loadStyleSheet(self, sheetName):
        """
        加载样式文件
        """
        with open("./Resources/%s.css" % sheetName,
                  'r', encoding='gbk') as fi:
            styleSheet = self.styleSheet()
            styleSheet += fi.read()
            self.setStyleSheet(styleSheet)

    # 按钮触发的槽
    def onButtonMinClicked(self):
        self.signalButtonMinClicked.emit()

    def onButtonRestoreClicked(self):
        self.m_pButtonRestore.setVisible(False)
        self.m_pButtonMax.setVisible(True)
        self.signalButtonRestoreClicked.emit()

    def onButtonMaxClicked(self):
        self.m_pButtonRestore.setVisible(True)
        self.m_pButtonMax.setVisible(False)
        self.signalButtonMinClicked.emit()

    def onButtonCloseClicked(self):
        self.signalButtonMinClicked.emit()

    def onRollTitle(self):
        """
        让标题栏中的标题显示为滚动的效果
        """
        titleContent = self.m_titleContent
        if self._nPos > len(titleContent):
            self._nPos = 0
        
        self.m_pTitleContent.setText(
            titleContent.mid(self._nPos)
        )
        self._nPos += 1

