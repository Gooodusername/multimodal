import socket
import sys
import time

serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host=socket.gethostname()

port=1234

serversocket.bind((host,port))

serversocket.listen(5)
print('开始侯听')
while True:
    print(time.time())
    clientsocket,addr=serversocket.accept()

    print('没有str的add',addr)
    print('没有str的add',str(addr))

    clientsocket.send('你好'.encode('utf-8'))

    clientsocket.close()

