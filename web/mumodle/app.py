from flask import Flask, send_file
from pywebio.platform.flask import webio_view
from pywebio.output import put_text, put_html, put_buttons, clear, scroll_to, put_image, toast, use_scope
from pywebio.input import input, TEXT
from pywebio.session import set_env

# 导入其他需要的库
# ...

app = Flask(__name__)

# 您的辅助函数 get_image, get_aduio_client, show_chat 等在此处定义

@app.route("/")
def index():
    return webio_view(main)

def main():
    clear()
    set_env(title="多模态对话")
    put_html("<h1>多模态模型聊天，快来和我聊天吧</h1>")
    while True:
        user_input = input("多模态对话:", type=TEXT)
        if user_input is None:
            break
        show_chat(user_input)

@app.route('/audio.mp3')
def audio_file():
    return send_file('audio.mp3', attachment_filename='audio.mp3')

if __name__ == '__main__':
    app.run(port=5000)
