import socket
import pickle
from pywebio_battery import put_audio
import soundfile as sf

single_waveform=0

def client(text):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '10.52.33.7'
    port = 8754

    clientsocket.connect((host, port))
    clientsocket.send(text.encode('utf-8'))
    print("开始接受返回信息")

    received_data = b''
    while True:
        audio = clientsocket.recv(1024)
        if not audio:  # 没有更多数据
            break
        received_data += audio

    print("从服务器收到的信息是：", received_data)

    if received_data:
        # 反序列化
        
        audio_data = pickle.loads(received_data)
        print(audio_data)
        # put_audio(audio_data)
        for i, waveform in enumerate(audio_data):
            # 提取单个波形数据
            single_waveform = waveform[0]  # 假设每个波形只有一个声道
            print(single_waveform)
            sf.write(f'audio.wav', single_waveform, 16000)  # 假设采样率是 16000 Hz
    else:
        print("未接收到数据")
    
    print(single_waveform)
    put_audio(single_waveform)

    clientsocket.close()

if __name__ == '__main__':
    client("A hammer is hitting a wooden surface")
