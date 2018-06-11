# 使用selectors实现tcp客户端
import selectors
import socket


from PyQt5 import QtCore


class TcpClientsWorkThread(QtCore.QThread):
    """
    处理Tcp clients的线程
    """

    def __init__(self, ip, port):
        super(TcpClientsWorkThread, self).__init__()
        self._ip = ip
        self._port = port
        self._exit = False
        self._mutex = QtCore.QMutex()

    def run(self):
        def read(sock, mask):
            sock.setblocking(False)
            data = sock.recv(1000)
            if data:
                print(data)
            else:
                print('recv null')
                

        self._clients = list()
        cc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cc.connect((self._ip, self._port))
        cc.setblocking(False)

        sel = selectors.DefaultSelector()
        sel.register(cc, selectors.EVENT_READ, read)

        while True:
            events = sel.select()
            for key, mask in events:
                func = key.data
                func(key.fileobj, mask)