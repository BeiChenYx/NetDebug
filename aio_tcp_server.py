"""
使用asyncio来实现tcp/ip服务器
"""
from PyQt5 import QtCore

import asyncio


class StopTcpServerException(Exception):
    pass

class TcpServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        self.transport = transport
        print('connect: ', self.peername)

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}: {}'.format(message, self.peername))

        print('Send: {!r} : {}'.format(message, self.peername))
        self.transport.write(data)

    def connection_lost(self, exc):
        print('connection_lost: ', self.peername)
        self.transport.close()

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
        coro = self._loop.create_server(
            TcpServerProtocol, self._ip, self._port
        )
        self._server = self._loop.run_until_complete(coro)
        print('Serving on {}'.format(self._server.sockets[0].getsockname()))
        msg = "3-TCPServerStart"
        self.statusSignal.emit(msg)
        try:
            self._loop.run_forever()
        except RuntimeError:
            print('RuntimeError ********')

        print('wait_closed...')
        self._loop.close()
        print('Exit Tcp server!')
        msg = "4-TCPServerClose"
        self.statusSignal.emit(msg)

