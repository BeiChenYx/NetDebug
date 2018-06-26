import socket
import select
import queue


from PyQt5 import QtCore


class UdpClientsWorkThread(QtCore.QThread):

    dataSignal = QtCore.pyqtSignal(bytes)
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
            1: clientThreadStart     客户端线程启动
            2: clientThreadClose     客户端线程关闭
            3: clientCreate          客户端创建完成
            4: clientClose           客户端关闭
        """
        self._clients = list()
        self.statusSignal.emit("1-clientThreadStart")

        for _ in range(1, self._count + 1):
            try:
                cc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                cc.setblocking(False)
                self._clients.append(cc)
            except Exception as err:
                self.statusSignal.emit("0-%s" % str(err))
                print(err)

        while True:
            try:
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
                            client.sendto(data, (self._ip, self._port))
                            msg = "3-%s" % str(client.getsockname())
                            self.statusSignal.emit(msg)
            except Exception as err:
                msg = "0-%s" % str(err)
                self.statusSignal.emit(msg)
                break

            if len(recvInput):
                for client in recvInput:
                    try:
                        data = client.recv(1000)
                        if data:
                            print(data)
                            self.dataSignal.emit(data)
                    except Exception as err:
                        msg = "0-%s" % str(err)
                        msgclient = "4-%s" % str(client.getsockname())
                        client.close()
                        self.statusSignal.emit(msg)
                        self.statusSignal.emit(msgclient)

        count = len(self._clients)
        for i in range(count):
            try:
                msg = "4-%s" % str(self._clients[i].getsockname())
                self.statusSignal.emit(msg)
            except Exception:
                pass
            finally:
                self._clients[i].close()
            
        self._clients.clear()
        self.statusSignal.emit("2-clientThreadClose")
