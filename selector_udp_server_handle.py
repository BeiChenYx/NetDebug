from PyQt5 import QtCore


import socket
import select


class UDPServerWorkThread(QtCore.QThread):

    dataSignal = QtCore.pyqtSignal(str, bytes)
    statusSignal = QtCore.pyqtSignal(str)

    def __init__(self, ip, port):
        super(UDPServerWorkThread, self).__init__()
        self._ip = ip
        self._port = port
        self._exit = False

    def exitUdpWorkThread(self):
        self._exit = True

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

            msg = "1-udp server started"
            self.statusSignal.emit(msg)
            while True:
                if self._exit:
                    break

                recvInput, *_ = select.select([sock, ], [sock, ], [])
                if len(recvInput):
                    data, addr = sock.recvfrom(1000)
                    self.dataSignal.emit('{}:{}'.format(*addr), data)
                    self._clients.append('{}:{}'.format(*addr))
                else:
                    QtCore.QThread.msleep(1)

            self._clients.clear()
            sock.close()
            msg = "2-udp server closed"
            self.statusSignal.emit(msg)
        except Exception as err:
            self.statusSignal.emit('0-%s' % str(err))
