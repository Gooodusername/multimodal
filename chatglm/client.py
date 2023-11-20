import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8888)
    client_socket.connect(server_address)

    try:
        print('连接到服务器:', server_address)
        while True:
            user_input = input('用户:')
            client_socket.send(user_input.encode('utf-8'))

            response = client_socket.recv(1024)
            print('机器人:', response.decode('utf-8'))

            # if '再见' or '拜拜' in user_input:
            #     break


    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
