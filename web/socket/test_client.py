import socket
import sys
from pywebio_battery import put_audio

# client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# host=socket.gethostname()

# port=1234

# client.connect((host,port))

# m=client.recv(1024).decode('utf-8')

# client.close()

# print(m)
put_audio('audio.wav')