import os
import configparser


from PyQt5 import QtWidgets
from PyQt5 import QtCore
from UI.ui_Publish import Ui_publish



class PublishPushBotton(QtWidgets.QPushButton):
    """主要处理点击信号发送控件的名字"""
    clickedSignal = QtCore.pyqtSignal(str)
    def __init__(self, name, text="", parent=None):
        super(PublishPushBotton, self).__init__(text, parent)
        self._name = name

    def mouseReleaseEvent(self, event):
        """重写clicked信号"""
        self.clickedSignal.emit(self._name)
        event.accept()

class PublishObject(QtWidgets.QWidget):
    """
    这个控件中包含发布要的:
        是否发送的选择按钮
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
        self.msg = QtWidgets.QLineEdit()
        self.button = PublishPushBotton(
            self._name + '-button', '发送', self
        )
        # 设置各个控件的样式
        self.check.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.check.setMinimumSize(25, 25)
        self.check.setMaximumSize(25, 25)

        self.msg.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.msg.setMinimumSize(120, 20)
        self.msg.setMaximumSize(1000, 1000)
        self.msg.setPlaceholderText('发布的消息')

        self.button.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.button.setMinimumSize(80, 25)
        self.button.setMaximumSize(80, 25)

        self.hlayout.addWidget(self.check)
        self.hlayout.addWidget(self.msg)
        self.hlayout.addWidget(self.button)
        self.hlayout.setSpacing(6)
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hlayout)

        self.setMinimumSize(400, 30)
        self.setMaximumSize(1000, 40)

    def __init_connect__(self):
        self.button.clickedSignal.connect(self.clicked)

    def get_msg(self):
        return self.msg.text()
    def set_msg(self, msg):
        self.msg.setText(msg)
    def isChecked(self):
        return self.check.isChecked()
    def setChecked(self, flag):
        self.check.setChecked(flag)
    def setEnabled(self, flag):
        self.check.setEnabled(flag)
        self.msg.setEnabled(flag)
        self.button.setEnabled(flag)

class MulPushButton(QtWidgets.QWidget, Ui_publish):

    status_signal = QtCore.pyqtSignal(str)
    data_signal = QtCore.pyqtSignal(bytes)

    def __init__(self, parent):
        super(MulPushButton, self).__init__(parent)
        self.setupUi(self)

        self._timer = QtCore.QTimer(self)
        self.min_len = 3
        self.button_info = list()

        self.initConnect()

    def initConnect(self):
        self.pushButton_add.clicked.connect(self.on_add_push)
        self.pushButton_del.clicked.connect(self.on_del_push)
        self._timer.timeout.connect(self.on_timeout)
        self.checkBox_publish_mul.stateChanged.connect(self.on_check_Timers)
        self.checkBox_hex_mul.stateChanged.connect(self.on_check_hex)

    def initConfig(self, msg):
        try:
            self.checkBox_hex_mul.setChecked(msg['mulhex'] == 'True')
            self.lineEdit_times_mul.setText(msg['multimes'])
            self._default_len = int(msg['mulcount'])
            # 初始化_default_len - 1个发布模块
            for i in range(self._default_len):
                object_name = 'publish_%d' % i
                publish = PublishObject(
                    object_name, self.scrollAreaWidgetContents
                ) 
                self.formLayout_publish.addWidget(publish)
                self.button_info.append(object_name)
                publish.clicked.connect(self.on_publish)
                publish.set_msg(msg['mulmsg_%d' % i])
                publish.setChecked(msg['mulcheck_%d' % i] == 'True')
        except Exception as err:
            self.status_signal.emit(str(err))

    def update_config(self):
        config = {
                'mulhex': str(self.checkBox_hex_mul.isChecked()),
                'multimes': self.lineEdit_times_mul.text(),
                'mulcount': len(self.button_info),
        }
        for value in self.button_info:
            publish = self.findChild(PublishObject, value)
            num = value.split('_')[1]
            config['mulmsg_%s' % num] = publish.get_msg()
            config['mulcheck_%s' % num] = str(publish.isChecked())
        return config

    def on_publish(self, name):
        publish_name = name.split('-')[0]
        if publish_name:
            publish = self.findChild(PublishObject, publish_name)
            msg = publish.get_msg()
            if self.checkBox_hex_mul.isChecked():
                try:
                    data = msg.split(' ')
                    self.data_signal.emit(
                        bytes(list(map(lambda x: int(x, 16), data)))
                    )
                except Exception:
                    self.status_signal.emit('16进制正确格式: 0A 0B 0C 15')
            else:
                self.data_signal.emit(msg.encode('gbk'))

    def on_add_push(self):
        """增加一行发布的窗口"""
        button_info_len = len(self.button_info)
        object_name = 'publish_%d' % button_info_len
        publish = PublishObject(object_name, self.scrollAreaWidgetContents) 
        self.formLayout_publish.addWidget(publish)
        self.button_info.append('publish_%d' % button_info_len)
        publish.clicked.connect(self.on_publish)

    def on_del_push(self):
        """删除一行发布的窗口"""
        button_info_len = len(self.button_info)
        if button_info_len > self.min_len: 
            name = self.button_info.pop()
            publish = self.findChild(PublishObject, name)
            publish.disconnect()
            self.formLayout_publish.removeWidget(publish)
            publish.deleteLater()

    def on_timeout(self):
        """超时信号槽"""
        for value in self.button_info:
            publish = self.findChild(PublishObject, value)
            msg = publish.get_msg()
            if publish.isChecked():
                if self.checkBox_hex_mul.isChecked():
                    try:
                        data = msg.split(' ')
                        self.data_signal.emit(
                            bytes(list(map(lambda x: int(x, 16), data)))
                        )
                    except Exception:
                        self.status_signal.emit('16进制正确格式: 0A 0B 0C 15')
                else:
                    self.data_signal.emit(msg.encode('gbk'))

    def enabled_ui(self, flag):
        """界面控件的开启和禁用"""
        self.lineEdit_times_mul.setEnabled(flag)
        # 增加和删除按钮
        self.pushButton_add.setEnabled(flag)
        self.pushButton_del.setEnabled(flag)
        for value in self.button_info:
            publish = self.findChild(PublishObject, value)
            publish.setEnabled(flag)

    def on_check_Timers(self):
        """循环发送的按钮"""
        if self.checkBox_publish_mul.isChecked():
            self._timer.start(int(self.lineEdit_times_mul.text()))
            self.enabled_ui(False)
        else:
            self._timer.stop()
            self.enabled_ui(True)

    def on_check_hex(self):
        for value in self.button_info:
            try:
                publish = self.findChild(PublishObject, value)
                data = publish.get_msg()
                if not data:
                    return
                if self.checkBox_hex_mul.isChecked():
                    data_temp = ' '.join('%02X' % ord(c) for c in data)
                else:
                    data_temp = ''.join(chr(int(h, 16)) for h in data.split(' '))
                publish.set_msg(data_temp)
            except Exception as err:
                self.status_signal.emit(str(err))


