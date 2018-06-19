from enum import Enum



from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from ui_CustomerTitleBar import Ui_MainWindow


BUTTON_WIDTH = 30
BUTTON_HEIGH = 30
TITLE_HEIGHT = 30


class ButtonType(Enum):
    MIN_BUTTON = 0
    MIN_MAX_BUTTON = 1
    ONLY_CLOSE_BUTTON = 2


class CustomerTitleBar(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(CustomerTitleBar, self).__init__(parent)
        self.setupUi(self)

        # 标题栏背景色
        self.m_colorR = 153
        self.m_colorG = 153
        self.m_colorB = 153

        # 移动串口的变量
        self.m_isPressed = False

        # 按钮类型
        self.m_buttonType = ButtonType.MIN_MAX_BUTTON

        # 窗口边框宽度
        self.m_windowBorderWidth = 0

        # 标题栏是否透明
        self.m_isTransparent = False

        # 标题栏跑马灯效果时钟
        self.m_titleRollTimer = QtCore.QTimer(self)

        self.initControl()
        self.initConnections()
        self.loadStyleSheet('MyTitle')

    def initControl(self):
        self.m_pIcon = QtWidgets.QLabel()
        self.m_pTitleContent = QtWidgets.QLabel()

        self.m_pButtonMin = QtWidgets.QPushButton()
        self.m_pButtonRestore = QtWidgets.QPushButton()
        self.m_pButtonMax = QtWidgets.QPushButton()
        self.m_pButtonClose = QtWidgets.QPushButton()

        self.m_pButtonMin.setFixedSize(QtCore.QSize(
            BUTTON_WIDTH, BUTTON_HEIGH 
        ))
        self.m_pButtonRestore.setFixedSize(QtCore.QSize(
            BUTTON_WIDTH, BUTTON_HEIGH 
        ))
        self.m_pButtonMax.setFixedSize(QtCore.QSize(
            BUTTON_WIDTH, BUTTON_HEIGH 
        ))
        self.m_pButtonClose.setFixedSize(QtCore.QSize(
            BUTTON_WIDTH, BUTTON_HEIGH 
        ))

        self.m_pTitleContent.setObjectName('TitleContent')
        self.m_pButtonMin.setObjectName('ButtonMin')
        self.m_pButtonRestore.setObjectName('ButtonRestore')
        self.m_pButtonMax.setObjectName('ButtonMax')
        self.m_pButtonClose.setObjectName('ButtonClose')

        self.m_pButtonMin.setToolTip('最小化')
        self.m_pButtonRestore.setToolTip('还原')
        self.m_pButtonMax.setToolTip('最大化')
        self.m_pButtonClose.setToolTip('关闭')

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
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)


    def initConnections(self):
        self.m_pButtonMin.clicked.connect(
            self.onButtonMinClickd
        )
        self.m_pButtonRestore.clicked.connect(
            self.onButtonRestoreClickd
        )
        self.m_pButtonMax.clicked.connect(
            self.onButtonMaxClickd
        )
        self.m_pButtonRestore.clicked.connect(
            self.onButtonCloseClickd
        )

    def setBackgroundColor(self, r, g, b, isTransparent):
        self.m_colorR = r
        self.m_colorG = g
        self.m_colorB = b
        self.m_isTransparent = isTransparent 
        self.update()

    def setTitleIcon(self, filePath, iconSize):
        self.m_pIcon.setPixmap(
            QtGui.QPixmap(filePath).scaled(iconSize)
        )

    def setTitleContent(self, titleContent, titleFontSize):
        font = self.m_pTitleContent.font()
        font.setPointSize(titleFontSize)

        self.m_pTitleContent.setText(titleContent)
        self.m_titleContent = titleContent

    def setTitleWidth(self, width):
        self.setFixedWidth(width)

    def setButtonType(self, buttonType):
        self.m_buttonType = buttonType
        if buttonType == ButtonType.MIN_BUTTON:
            self.m_pButtonRestore.setVisible(False)
            self.m_pButtonMax.setVisible(False)
        elif buttonType == ButtonType.MIN_MAX_BUTTON:
            self.m_pButtonRestore.setVisible(False)
        elif buttonType == ButtonType.ONLY_CLOSE_BUTTON:
            self.m_pButtonMin.setVisible(False)
            self.m_pButtonRestore.setVisible(False)
            self.m_pButtonMax.setVisible(False)
        else:
            pass

    def setTitleRoll(self):
        self.m_titleRollTimer.timeout.connect(
            self.onRollTitle
        )

    def setWindowBorderWidth(self, borderWidth):
        self.m_windowBorderWidth = borderWidth

    def saveRestoreInfo(self, point, size):
        self.m_restorePos = point
        self.m_restoreSize = size

    def getRestoreInfo(self, point, size):
        return (self.m_restorePos, self.m_restoreSize)

    def onRollTitle(self):
        pass

    def onButtonMinClickd(self):
        pass

    def onButtonRestoreClickd(self):
        pass

    def onButtonMaxClickd(self):
        pass

    def onButtonCloseClickd(self):
        pass

    def loadStyleSheet(self, sheetName):
        filePath = './Resources/' + sheetName + '.css'
        with open(filePath, 'r', encoding='gbk') as fi:
            styleSheet = self.styleSheet() 
            styleSheet += fi.read()
            self.setStyleSheet(styleSheet)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QMainWindow()
    ui = CustomerTitleBar()
    ui.setupUi(widget)
    ui.show()
    sys.exit(app.exec_())
