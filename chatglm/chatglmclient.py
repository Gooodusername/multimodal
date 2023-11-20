import socket
import tkinter as tk
from tkinter import scrolledtext


def start_client(user_input):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('10.52.33.7', 8888)
    client_socket.connect(server_address)

    try:
        print('连接到服务器:', server_address)
        while True:
            
            client_socket.send(user_input.encode('utf-8'))

            response = client_socket.recv(1024)
            print('机器人:', response.decode('utf-8'))

            # if '再见' or '拜拜' in user_input:
            #     break

    finally:
        client_socket.close()


def create_gui():
    # 创建主窗口
    window = tk.Tk()
    window.title("机器人对话客户端")

    # 创建用户输入和机器人回应的框架
    frame_user = tk.Frame(window, bg='lightgrey')
    frame_robot = tk.Frame(window, bg='lightgrey')

    # 创建滚动文本区域用于显示用户输入和机器人回应
    text_user = scrolledtext.ScrolledText(frame_user, wrap=tk.WORD, width=40, height=10)
    text_robot = scrolledtext.ScrolledText(frame_robot, wrap=tk.WORD, width=40, height=10)
    text_user.pack(padx=10, pady=10)
    text_robot.pack(padx=10, pady=10)

    # 处理发送消息的函数
    def send_message():
        user_messages = entry_box.get()
        # TODO: 添加将消息发送到服务器并接收响应的逻辑
        # 目前，只在用户文本区显示消息
        start_client(user_messages)
        text_user.insert(tk.END, f"用户: {user_messages}\n")
        # 清空输入框
        entry_box.delete(0, tk.END)

        # 模拟机器人回应
        robot_response = "这是机器人的回应"  # 实际中应替换为服务器的实际响应
        text_robot.insert(tk.END, f"机器人: {robot_response}\n")

    # 创建一个文本输入框用于用户输入
    entry_box = tk.Entry(window, width=80)
    entry_box.pack(side=tk.BOTTOM, padx=10, pady=10)

    # 创建一个发送按钮
    send_button = tk.Button(window, text="发送", command=send_message)
    send_button.pack(side=tk.BOTTOM)

    # 在窗口中布局框架
    frame_user.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    frame_robot.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # 启动GUI事件循环
    window.mainloop()

# 在您的本地Python环境中运行此函数即可创建并打开GUI窗口


if __name__ == "__main__":
    create_gui()
