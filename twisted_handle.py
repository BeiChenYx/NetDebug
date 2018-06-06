# from PyQt5 import QtCore

# from twisted.internet.protocol import Factory, Protocol
# from twisted.internet import reactor, task
# import struct
# from twisted.python import log
# import sys
# import time
# log.startLogging(sys.stdout)

# class TcpServerPipe(QtCore.QObject):
#     """
#     twisted和qt页面通信类
#     """
#     pipeSignal = QtCore.pyqtSignal(str)

#     def emitData(self, data):
#        self.pipeSignal.emit(data) 

# global tcp_server_pipe
# tcp_server_pipe = TcpServerPipe()

# class Work(Protocol):
#     def __init__(self, users):
#         self.users = users
#         # self.last_heartbeat_time = 0
#         self._data_buffer = bytes()

#     def connectionMade(self):
#         log.msg("New connect, the info is:",
#                 self.transport.getPeer())
#         global tcp_server_pipe
#         tcp_server_pipe.emitData(self.transport.getPeer())

#     def connectionLost(self, reason):
#         if self.phone_number in self.users:
#             del self.users[self.phone_number]

#     def dataReceived(self, data):
#         global tcp_server_pipe
#         tcp_server_pipe.emitData(data)

#     # def handle_heartbeat(self, content):
#     #     self.last_heartbeat_time = int(time.time())

#     def send_content(self, send_content, command_id, phone_numbers):
#         length = 12 + len(send_content)
#         version = self.version
#         command_id = command_id
#         header = [length, version, command_id]
#         header_pack = struct.pack('!3I', *header)
#         for phone_number in phone_numbers:
#             if phone_number in self.users.keys():
#                 self.users[phone_number].transport.write(
#                     header_pack + send_content
#                 )
#             else:
#                 log.msg(
#                     "Phone_number:%s 不在线，不能聊天" % phone_number.encode('utf-8')
#                 )


# class WorkFactory(Factory):
#     def __init__(self):
#         print('starting....')
#         self.users = {}

#     def buildProtocol(self, addr):
#         return Work(self.users)


# class TcpServerDebug(QtCore.QThread):
#     receive_data = QtCore.pyqtSignal()
#     def __int__(self):
#         super(TcpServerDebug, self).__init__()

#     def setPort(self, port):
#         self._port = port

#     def run(self):
#         from twisted.internet import reactor
#         reactor.listenTCP(self._port, ChatFactory())
#         reactor.run()
#         del reactor
