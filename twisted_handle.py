from PyQt5 import QtCore

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver


class TcpServerPipe(QtCore.QObject):
    """
    twisted和qt页面通信类
    """
    pipeSignal = QtCore.pyqtSignal()

    def emitData(self, data):
       self.pipeSignal.emit(data) 

global tcp_server_pipe
tcp_server_pipe = TcpServerPipe()

class Work(LineReceiver):
    def __init__(self):
        self.state = "GETNAME"

    def connectionMade(self):
        echo_buf = "Welcome to the UTEK network debugging tool."
        self.sendLine(echo_buf.encode('utf-8'))

    def connectionLost(self):
        if self.name in self.users:
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == 'GETNAME':
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)
    
    def handle_GETNAME(self, name):
        if name in self.users:
            self.sendLine("Name taken, please choose anothre.".encode("utf-8"))
            return
        self.sendLine(("Welcome, %s" % name).encode('utf-8'))
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = "<%s> %s" % (
            self.name.decode('utf-8', 'ignore'),
            message.decode('utf-8', 'ignore')
        )
        for _, protocol in self.users.items():
            if protocol != self:
                protocol.sendLine(message.encode('utf-8'))


class WorkFactory(Factory):
    def __init__(self):
        print('starting....')
        self.users = {}

    def buildProtocol(self, addr):
        return Work(self.users)


class TcpServerDebug(QtCore.QThread):
    receive_data = QtCore.pyqtSignal()
    def __int__(self):
        super(TcpServerDebug, self).__init__()

    def setPort(self, port):
        self._port = port

    def run(self):
        from twisted.internet import reactor
        reactor.listenTCP(self._port, ChatFactory())
        reactor.run()
        del reactor
