"""publish的UI界面处理"""
import configparser

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QCursor

from ui.ui_publish import Ui_publish
from publish import PublishWorkThread

import ui.image_rc


class PublishPushBotton(QtWidgets.QPushButton):
    """主要处理点击信号发送控件的名字"""
    clickedSignal = QtCore.pyqtSignal(str)
    def __init__(self, icon, name, text="", parent=None):
        super(PublishPushBotton, self).__init__(icon, text, parent)
        self._name = name

    def mouseReleaseEvent(self, event):
        """重写clicked信号"""
        self.clickedSignal.emit(self._name)
        event.accept()

class PublishObject(QtWidgets.QWidget):
    """
    这个控件中包含发布要的:
        是否发送的选择按钮
        主题
        发送消息
        发送按钮
    """
    clicked = QtCore.pyqtSignal(str)
    def __init__(self, name, parent):
        """发布消息的组合"""
        super().__init__(parent)
        self._name = name
        self.setObjectName(self._name)

        self.__init_ui__(parent)
        self.__init_connect__()

    def __init_ui__(self, parent):
        self.hlayout = QtWidgets.QHBoxLayout() 
        self.check = QtWidgets.QCheckBox()
        self.topic = QtWidgets.QLineEdit()
        self.msg = QtWidgets.QLineEdit()
        self.button = PublishPushBotton(
            QtGui.QIcon(':/img/启动.png'), 
            self._name + '-button', '', self
        )
        # 设置各个控件的样式
        self.check.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.check.setMinimumSize(25, 25)
        self.check.setMaximumSize(25, 25)
        self.topic.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.topic.setMinimumSize(30, 25)
        self.topic.setMaximumSize(120, 1000)
        self.topic.setPlaceholderText('要发布的主题')

        self.msg.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.msg.setMinimumSize(120, 25)
        self.msg.setMaximumSize(1000, 1000)
        self.msg.setPlaceholderText('发布的消息')

        self.button.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.button.setMinimumSize(35, 35)
        self.button.setMaximumSize(35, 35)
        self.button.setIconSize(QtCore.QSize(25, 25))

        self.hlayout.addWidget(self.check)
        self.hlayout.addWidget(self.topic)
        self.hlayout.addWidget(self.msg)
        self.hlayout.addWidget(self.button)
        self.hlayout.setSpacing(6)
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hlayout)

        self.setMinimumSize(550, 30)
        self.setMaximumSize(1000, 40)

    def __init_connect__(self):
        self.button.clickedSignal.connect(self.clicked)

    def get_topic(self):
        return self.topic.text()
    def get_msg(self):
        return self.msg.text()
    def isChecked(self):
        return self.check.isChecked()
    def setEnabled(self, flag):
        self.check.setEnabled(flag)
        self.topic.setEnabled(flag)
        self.msg.setEnabled(flag)
        self.button.setEnabled(flag)


class PublishWidget(QtWidgets.QWidget, Ui_publish):
    """
    主界面类，主要负责自定义标题了，侧边栏，
    主功能区
    """
    def __init__(self, parent=None):
        super(PublishWidget, self).__init__(parent)
        self.setupUi(self)

        # 先创建工作线程，再去处理初始化
        self._config_path = 'UTMQConfig.ini'
        config = configparser.ConfigParser()
        config.read(self._config_path, 'utf-8')
        utmqset = config['UTMQSet']
        self._push = PublishWorkThread(
            utmqset['username'],
            utmqset['password'],
            utmqset['host'],
            utmqset['port'],
            utmqset['publishid']
        )
        self._push.start()

        self._timer = QtCore.QTimer(self)

        # 先初始化UI，再初始化信号槽
        self.__init_ui__()
        self.__init_connect__()

    def __init_connect__(self):
        """初始化信号槽"""        
        self.radioButton_publish.clicked.connect(self.on_radiobutton_clicked)
        self.pushButton_clear.clicked.connect(
            lambda : self.label_counts.setText('0')
        )
        self._timer.timeout.connect(self.on_timeout)
        self._push.dataSignal.connect(self.on_push_status)
        self.pushButton_7.clicked.connect(self.on_add_push) 
        self.pushButton_8.clicked.connect(self.on_del_push) 
    
    def __init_ui__(self):
        """初始化界面"""
        # 构建 发送按钮 主题 消息的对应关系字典
        self._default_len = 8
        self.button_info = list()
        # 初始化5个发布模块
        for i in range(1, self._default_len):
           publish = PublishObject('publish_%d' % i, self.scrollAreaWidgetContents) 
           self.button_info.append('publish_%d' % i)
           self.formLayout_publish.addWidget(publish)
           publish.clicked.connect(self.on_publish)

    def on_publish(self, name):
        publish_name = name.split('-')[0]
        print(publish_name)
        if publish_name:
            publish = self.findChild(PublishObject, publish_name)
            print(publish)
            topic = publish.get_topic()
            msg = publish.get_msg()
            self._push.on_send(topic, msg) 

    def on_add_push(self):
        """增加一行发布的窗口"""
        button_info_len = len(self.button_info) + 1
        object_name = 'publish_%d' % button_info_len
        publish = PublishObject(object_name, self.scrollAreaWidgetContents) 
        self.formLayout_publish.addWidget(publish)
        self.button_info.append('publish_%d' % button_info_len)
        publish.clicked.connect(self.on_publish)

    def on_del_push(self):
        """删除一行发布的窗口"""
        button_info_len = len(self.button_info)
        if button_info_len > self._default_len: 
            name = self.button_info.pop()
            publish = self.findChild(PublishObject, name)
            publish.disconnect()
            self.formLayout_publish.removeWidget(publish)
            publish.deleteLater()
        button_info_len = len(self.button_info)

    def on_radiobutton_clicked(self):
        """循环发送的按钮"""
        if self.radioButton_publish.isChecked():
            self._push.set_pasue(False) 
            self._timer.start(1000 * int(self.lineEdit_times.text()))
            self.enabled_ui(False)
        else:
            self._push.set_pasue(True) 
            self._timer.stop()
            self.enabled_ui(True)

    def on_timeout(self):
        """超时信号槽"""
        for value in self.button_info:
            publish = self.findChild(PublishObject, value)
            print(publish)
            topic = publish.get_topic()
            msg = publish.get_msg()
            if publish.isChecked():
                self._push.on_send(topic, msg) 

    def enabled_ui(self, flag):
        """界面控件的开启和禁用"""
        self.lineEdit_times.setEnabled(flag)
        # 增加和删除按钮
        self.pushButton_7.setEnabled(flag)
        self.pushButton_8.setEnabled(flag)
        for value in self.button_info:
            publish = self.findChild(PublishObject, value)
            publish.setEnabled(flag)

    def on_push_status(self, length):
        """发送的数据长度槽"""
        self.label_counts.setText(
            str(length + int(self.label_counts.text()))
        )

    def on_update_set(self):
        """
        更新配置，重启服务
        通过信号告诉所有工作页面,
        然后通过配置文件共享数据
        """
        self.radioButton_publish.setChecked(False)
        self.on_radiobutton_clicked()
        self._push.dataSignal.disconnect()
        self._push.exitThread()
        self._push.wait(1)
        del self._push
        # 重启任务
        config = configparser.ConfigParser()
        config.read(self._config_path, 'utf-8')
        utmqset = config['UTMQSet']
        self._push = PublishWorkThread(
            utmqset['username'],
            utmqset['password'],
            utmqset['host'],
            utmqset['port'],
            utmqset['publishid']
        )
        self._push.dataSignal.connect(self.on_push_status)
        self._push.start()

