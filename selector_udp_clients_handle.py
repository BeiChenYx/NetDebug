import socket
import select
import queue


from PyQt5 import QtCore


class UdpClientsWorkThread(QtCore.QThread):

    statusSignal = QtCore.pyqtSignal(str)
    def __init__(self, ip, port, count):
        super(UdpClientsWorkThread, self).__init__()
        self._ip = ip
        self._port = port
        self._count = count
        self._exit = False
        self._queue = queue.Queue()

    def exitUdpClientsThread(self):
        self._exit = True

    def sendData(self, data):
        self._queue.put(data)

    def run(self):
        """
        msg格式:
        cmd-message
        cmd:
            0: info_status           普通状态信息
            3: clientThreadStart     客户端线程启动
            4: clientThreadClose     客户端线程关闭
        """
        self._clients = list()
        self.statusSignal.emit("3-client thread started")

        for _ in range(1, self._count + 1):
            try:
                cc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                cc.setblocking(False)
                self._clients.append(cc)
            except Exception as err:
                self.statusSignal.emit("0-%s" % str(err))

        while True:
            try:
                if len(self._clients) == 0 or self._exit:
                    break
                _, sendOutput, _ = select.select(self._clients, self._clients, [])
                if len(sendOutput):
                    if not self._queue.empty():
                        data = self._queue.get()
                        for client in sendOutput:
                            client.sendto(data, (self._ip, self._port))
                    else:
                        QtCore.QThread.msleep(1)
            except Exception as err:
                self.statusSignal.emit("0-%s" % str(err))

        count = len(self._clients)
        for i in range(count):
            self._clients[i].close()
            
        self._clients.clear()
        self.statusSignal.emit("4-client thread closed")
