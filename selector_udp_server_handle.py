from PyQt5 import QtCore


import socket
import select
import queue


class UDPServerWorkThread(QtCore.QThread):

    dataSignal = QtCore.pyqtSignal(str, bytes)
    statusSignal = QtCore.pyqtSignal(str)

    def __init__(self, ip, port):
        super(UDPServerWorkThread, self).__init__()
        self._ip = ip
        self._port = port
        self._exit = False
        self._queue = queue.Queue()

    def exitUdpWorkThread(self):
        self._exit = True

    def sendData(self, addr, data):
        self._queue.put((addr,data))

    def run(self):
        """
        msg格式:
        cmd-message
        cmd:
            0: info_status           普通状态信息
            1: serverThreadStart
            2: serverThreadClose
        """
        try:
            self._clients = list()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self._ip, self._port))
            sock.setblocking(False)

            msg = "1-UdpServerStart"
            self.statusSignal.emit(msg)
            while True:
                if self._exit:
                    break

                recvInput, sendOutput, _ = select.select(
                    [sock, ], [sock, ], []
                )
                if len(recvInput) == 0 and self._queue.empty():
                    QtCore.QThread.msleep(1)
                if len(sendOutput) and len(self._clients):
                    if not self._queue.empty():
                        addr, data = self._queue.get()
                        sock.sendto(data, eval(addr))
                        
                if len(recvInput):
                    data, addr = sock.recvfrom(1000)
                    print('addr: ', addr)
                    print('data: ', data)
                    self.dataSignal.emit(str(addr), data)
                    self._clients.append(addr)

            self._clients.clear()
            sock.close()
            msg = "2-UdpServerClose"
            self.statusSignal.emit(msg)
        except Exception as err:
            self.statusSignal.emit('0-%s' % str(err))