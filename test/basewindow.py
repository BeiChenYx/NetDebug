from PyQt5 import QtCore, QtGui, QtWidgets

from mytitlebar import MyTitleBar


class BaseWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(BaseWindow, self).__init__(parent)
        self.setupUi(self)
        self.m_titleBar = MyTitleBar()

        self.setWindowFlags(
            (QtCore.Qt.FramelessWindowHint | 
            QtCore.Qt.WindowMinimizeButtonHint)
        )
        self.initTitleBar()

    def initTitleBar(self):
        self.m_titleBar.move(0, 0)
        self.m_titleBar.signalButtonMinClicked.connect(
            self.onButtonMinClicked
        )
        self.m_titleBar.signalButtonRestoreClicked.connect(
            self.onButtonRestoreClicked
        )
        self.m_titleBar.signalButtonMaxClicked.connect(
            self.onButtonMaxClicked
        )
        self.m_titleBar.signalButtonCloseClicked.connect(
            self.onButtonCloseClicked
        )

    def paintEvent(self, event):
        """
        设置背景色
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
            QtGui.QBrush(QtGui.QColor( 238, 223, 204))
        )

        return QtWidgets.QWidget.paintEvent(event)
    
    def loadStyleSheet(self, sheetName):
        """
        加载样式文件
        """
        with open("./Resources/%s.css" % sheetName,
                  'r', encoding='gbk') as fi:
            styleSheet = self.styleSheet()
            styleSheet += fi.read()
            self.setStyleSheet(styleSheet)

    def onButtonMinClicked(self):
        if QtCore.Qt.Tool == (self.windowFlags() & QtCore.Qt.Tool):
            self.hide()
        else:
            self.showMinimized()

    def onButtonRestoreClicked(self):
        windowPos, windowSize = self.m_titleBar.getRestoreInfo() 
        self.setGeometry(QtCore.QRect(
            windowPos, windowSize
        ))

    def onButtonMaxClicked(self):
        self.m_titleBar.saveRestoreInfo(
            self.pos(), QtCore.QSize(
                self.width(), self.height()
            )
        )
        desktopRect = QtWidgets.QApplication.desktop().availableGeometry()
        factRect = QtCore.QRect(
            desktopRect.x() - 3, desktopRect.y() -3,
            desktopRect.width() + 6, desktopRect.height() + 6
        )
        self.setGeometry(factRect)

    def onButtonCloseClicked(self):
        self.close()