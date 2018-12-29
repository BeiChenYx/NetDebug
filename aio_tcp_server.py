"""
使用asyncio来实现tcp/ip服务器
"""
from PyQt5 import QtCore

import asyncio


class TCPServerWorkThread(QtCore.QThread):
    """
    处理TCPServer的服务器线程
    """
    dataSignal = QtCore.pyqtSignal(str, bytes)
    statusSignal = QtCore.pyqtSignal(str)

    def __init__(self, ip, port):
        super(TCPServerWorkThread, self).__init__()
        self._ip = str(ip)
        self._port = int(port)
        self._loop = asyncio.get_event_loop()

    def exitTCPServer(self):
        self._server.close()
        self._loop.run_until_complete(self._server.wait_closed())
        print('exitTCPServer exit...')

    def sendData(self, addr, msg):
        pass

    def run(self):
        msg = "3-TCPServerStart"
        self.statusSignal.emit(msg)

        msg = "4-TCPServerClose"
        self.statusSignal.emit(msg)

