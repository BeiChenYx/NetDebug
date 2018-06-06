# 使用selector来实现TCP服务器
import selectors
import socket


def accept(sock, mask):
    conn, addr = sock.accept()
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1000)
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

sock = socket.socket()
sock.bind(('192.168.2.119', 1234))
sock.listen(100)
sock.setblocking(False)
sel = selectors.DefaultSelector()
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    print('waiting....')
    events = sel.select()
    for key, mask in events:
        print(key.data)
        print(key.fileobj)
        func = key.data
        obj = key.fileobj
        func(obj, mask)
