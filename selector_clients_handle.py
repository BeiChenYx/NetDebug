# 使用selectors实现tcp客户端
# import selectors
import socket
import select


from PyQt5 import QtCore


class TcpClientsWorkThread(QtCore.QThread):
    """
    处理Tcp clients的线程
    """
    dataSignal = QtCore.pyqtSignal(bytes)
    statusSignal = QtCore.pyqtSignal(str)

    def __init__(self, ip, port, count):
        super(TcpClientsWorkThread, self).__init__()
        self._ip = ip
        self._port = port
        self._exit = False
        self._mutex = QtCore.QMutex()

        # 客户端个数
        self._count = count

    def exitTcpClientsThread(self):
        self._mutex.lock()
        [cc.close for cc in self._clients]
        self._clients.clear()
        self._mutex.unlock()

    def sendData(self, data):
        self._mutex.lock()
        for client in self._clients:
            client.send(data)
        self._mutex.unlock()

    def run(self):
        """
        msg格式:
        cmd-message
        cmd:
            0: ClientConnect         客户端已连接
            1: ClientClose           客户端断开
            2: ClientConnectErr      客户端连接错误
            3: info_status           普通状态信息
        """
        self._clients = list()
        self._client_index = dict()

        # 创建客户端，并连接服务器
        for i in range(1, self._count + 1):
            try:
                cc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                cc.connect((self._ip, self._port))
                self._clients.append(cc)
                print('client index: ', i)
                msg = "0-%s %d" % (cc.getsockname(), i)
                self.statusSignal.emit(msg)
                self._client_index[cc] = i
            except Exception as err:
                self.statusSignal.emit(str(err))
        
        for cc in self._clients:
            cc.setblocking(False)

        # 使用事件循环来监听数据到达
        while True:
            if len(self._clients) == 0:
                break
            recvInput, _, _ = select.select(self._clients, [], [])
            for client in recvInput:
                with self._mutex.lock():
                    data = client.recv(1000)
                    if data:
                        self.dataSignal.emit(data)
                        # print(data)
                        # if data.decode('gbk') == 'q':
                        #     print('正常断开连接')
                        #     break
                    else:
                        msg = "1-%s %d ClientClose" % (
                            client.getsockname(),
                            self._client_index[client]
                        )
                        client.close()
                        self.statusSignal.emit(msg)
                        self._clients.remove(client)
                        if len(self._clients) == 0:
                            break
                
        [cc.close for cc in self._clients]
        self.statusSignal.emit('3-TCPClientWorkThread exit')