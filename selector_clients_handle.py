# 使用selectors实现tcp客户端
# import selectors
import socket
import select
import queue


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

        # 客户端个数
        self._count = count
        self._queue = queue.Queue()

    def exitTcpClientsThread(self):
        # [cc.close() for cc in self._clients]
        # self._clients.clear()
        # print('exitTcpClientsThread exit')
        self._exit = True

    def sendData(self, data):
        self._queue.put(data)

    def run(self):
        """
        msg格式:
        cmd-message
        cmd:
            0: ClientConnect         客户端已连接
            1: ClientClose           客户端断开
            2: ClientConnectErr      客户端连接错误
            3: info_status           普通状态信息
            4: clientThreadStart     客户端线程启动
            5: clientThreadClose     客户端线程关闭
        """
        self._clients = list()
        self.statusSignal.emit('4-clientThreadStart')

        # 创建客户端，并连接服务器
        for _ in range(1, self._count + 1):
            try:
                cc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                cc.connect((self._ip, self._port))
                self._clients.append(cc)
                msg = "0-%s" % str(cc.getsockname())
                self.statusSignal.emit(msg)
            except Exception as err:
                msg = "2-Connect error:%s" % str(err)
                self.statusSignal.emit(msg)
        
        for cc in self._clients:
            cc.setblocking(False)

        # 使用事件循环来监听数据到达
        while True:
            if len(self._clients) == 0 or self._exit:
                break
            recvInput, sendOutput, _ = select.select(
                self._clients, self._clients, []
            )
            if len(recvInput) == 0 and self._queue.empty():
                QtCore.QThread.msleep(1)

            if len(sendOutput):
                if not self._queue.empty():
                    data = self._queue.get()
                    for client in sendOutput:
                        client.send(data)
            
            if len(recvInput):
                for client in recvInput:
                    data = client.recv(1000)
                    if data:
                        self.dataSignal.emit(data)
                    else:
                        msg = "1-%s" % str(client.getsockname())
                        client.close()
                        self.statusSignal.emit(msg)
                        self._clients.remove(client)
                        if len(self._clients) == 0:
                            break
                
        count = len(self._clients)
        for i in range(count):
            msg = "1-%s" % str(self._clients[i].getsockname())
            self._clients[i].close()
            self.statusSignal.emit(msg)
        self._clients.clear()
        self.statusSignal.emit('5-clientThreadClose')
