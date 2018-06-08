# 使用selector来实现TCP服务器
from PyQt5 import QtCore


import selectors
import socket

class TCPServerWorkThread(QtCore.QThread):
    """
    处理TCPServer的服务器线程
    """
    dataSignal = QtCore.pyqtSignal(bytes)
    statusSignal = QtCore.pyqtSignal(str)

    def __init__(self, ip, port):
        super(TCPServerWorkThread, self).__init__()
        self._ip = ip
        self._port = port
        self._exit = False

    def exitTCPServer(self):
        self._exit = True
        cc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cc.connect((self._ip, self._port))
        cc.close()

    def run(self):
        _clients = dict() # conn:addr
        def accept(sock, mask):
            conn, addr = sock.accept()
            conn.setblocking(False)
            sel.register(conn, selectors.EVENT_READ, read)
            # print('client addr: ', addr)
            # print('client conn: ', conn)
            _clients[conn] = addr
            msg = "1-%s" % str(addr)
            self.statusSignal.emit(msg)

        def read(conn, mask):
            data = conn.recv(1000)
            if data:
                self.dataSignal.emit(data)
            else:
                msg = "2-%s" % str(_clients[conn])
                sel.unregister(conn)
                conn.close()
                self.statusSignal.emit(msg)

        sock = socket.socket()
        sock.bind((self._ip, self._port))
        sock.listen(100)
        sock.setblocking(False)
        sel = selectors.DefaultSelector()
        sel.register(sock, selectors.EVENT_READ, accept)

        msg = "3-TCPServerStart"
        self.statusSignal.emit(msg)
        while True:
            if self._exit:
                msg = "4-TCPServerClose"
                self.statusSignal.emit(msg)
                break
            # 事件循环，只有等到有客户端进入/退出/接收数据才会响应
            # 因此在断开时使用一个本地client来触发
            events = sel.select()
            for key, mask in events:
                func = key.data
                obj = key.fileobj
                func(obj, mask)

        sock.close()
        sel.close()