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
        self.event_loop = asyncio.get_event_loop()

    def exitTCPServer(self):
        self.event_loop.call_soon_threadsafe(self.event_loop.stop)

    def sendData(self, addr, msg):
        pass

    async def on_work(self, reader, writer):
        """
        处理客户端的协程函数
        """
        addr = writer.get_extra_info('peername')
        self.statusSignal.emit('1-{}:{}'.format(*addr))


    def run(self):
        factory = asyncio.start_server(self.on_work, self._ip, self._port)
        server = self.event_loop.run_until_complete(factory)
        msg = "3-TCPServerStart"
        self.statusSignal.emit(msg)

        try:
            self.event_loop.run_forever()
        except Exception:
            pass
        finally:
            server.close()
            self.event_loop.run_until_complete(server.wait_closed())
            self.event_loop.close()
        
        # TODO: 目前没有什么好方法来退出事件循环，因此下面代码根本无法执行
        msg = "4-TCPServerClose"
        self.statusSignal.emit(msg)
        print(msg)

