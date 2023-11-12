from pywebio import start_server
from pywebio.output import put_text, put_html, put_buttons, clear, scroll_to, put_image, toast
from pywebio.input import input, TEXT
from pywebio.session import set_env

import requests
import io
import base64
from PIL import Image
import re

# 设置 Stable Diffusion API 的地址
STABLE_DIFFUSION_API = "http://192.168.31.2:886"

def get_image(text):
    # 请求 Stable Diffusion API 获取图像
    payload = {
        "prompt": text,
        "negative_prompt": "EasyNegative",
        "steps": 20,
        'width': 512,
        'height': 512,
        'sd_model_checkpoint': 'qteamixQ_omegaFp16.safetensors [39d6af08b2]'
    }
    
    response = requests.post(url=f'{STABLE_DIFFUSION_API}/sdapi/v1/txt2img', json=payload)
    r = response.json()
    
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i)))
        return image

def chat():
    set_env(title="多模态对话")
    put_html("<h1>有聊天框的多模态</h1>")
    
    chat_log = []  # List to keep track of the chat history

    def show_chat():
        clear()  # Clear the previous output
        for role, message in chat_log:
            if isinstance(message, str):  # if message is text
                chat_log.append(('User2','不好意思没做'))
            elif isinstance(message, Image.Image):  # if message is an image
                # Convert the image to bytes and display it
                img_byte_arr = io.BytesIO()
                message.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                put_image(img_byte_arr)

        scroll_to()  # Scroll to the bottom of the chat

    while True:
        user_input = input("多模态对话:", type=TEXT)
        if user_input is None:
            break
        chat_log.append(('User1', user_input))
        show_chat()

        # Check if the user input is asking for an image
        if user_input.startswith('image:'):  # or any other pattern to request an image
            keyword = user_input.split(',', 1)[1]  # Extract keyword after 'image:'
            toast("图片转换中", color="success")
            image = get_image(keyword)
            chat_log.append(('User2', image))  # Store the image object directly
        else:
            # Here you would call your AI or whatever user2 is supposed to be
            user2_response = "没做"   
            chat_log.append(('User2', user2_response))
        
        show_chat()

if __name__ == '__main__':
    chat()
