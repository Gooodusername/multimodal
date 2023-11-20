import socket
from transformers import AutoTokenizer, AutoModel
import torch
import threading

tokenizer = AutoTokenizer.from_pretrained("./dataroot/models/THUDM/chatglm2-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("./dataroot/models/THUDM/chatglm2-6b", trust_remote_code=True).half().cuda()
model = model.eval()

initialization = '''你叫小憨是东北大学悉尼智能科技学院HACI实验室的一个交互机器人。
                    你还在学习如何和人交互。你的回答风格是可爱，但是简短且直接。
                    你最喜欢记住别人的信息，并且一起聊八卦。
                    你很喜欢主动提问他人的近况，表示关心。
                    如果你认为对话者聊不下去了，请结束对话，并说很开心和您聊天。
                    HACI实验室是人机情感计算与情感交互实验室。
                '''
_, history = model.chat(tokenizer, initialization, history=[])

def process_message(message, history):
    response, history = model.chat(tokenizer, message, history=history)
    return response

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            print('收到消息:', data.decode('utf-8'))
            response = process_message(data.decode('utf-8'), history)
            client_socket.send(response.encode('utf-8'))

    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8888)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print('等待客户端连接...')
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print('客户端已连接:', client_address)

            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
