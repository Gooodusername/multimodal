from pywebio import start_server
from pywebio.output import put_text, put_html, put_buttons, clear, scroll_to
from pywebio.input import input, TEXT
from pywebio.session import set_env, run_js

import requests
import io
import base64
from PIL import Image
import json
import re

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import set_env, info as session_info

def chat():
    set_env(title="多模态对话")
    put_html("<h1>有聊天框的多模态</h1>")
    
    chat_log = []  # List to keep track of the chat history

    def show_chat():
        clear()  # Clear the previous output
        for role, text in chat_log:
            if role == 'User1':
                put_html('<div style="display: flex; justify-content: end; margin: 10px;">'
                     '<div style="padding: 15px; background-color: #f2f2f2; color: #333; '
                     'border-radius: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); display: flex; align-items: center;">'
                     '<img src="https://pic.imgdb.cn/item/654bbca4c458853aef35895f.jpg" alt="User1 Avatar" '
                     'style="width: 30px; height: 30px; border-radius: 50%; margin-right: 10px;">'
                     f'{text}</div></div>')
            else:
                put_html('<div style="margin: 10px; padding: 15px; background-color: #008CBA; color: #fff; '
                     'border-radius: 15px; box-shadow: -2px 2px 10px rgba(0,0,0,0.1); '
                     'width: fit-content;">'
                     f'<b style="color: #fff;">有求必应的多模态:</b> {text}</div>')
        scroll_to()  # Scroll to the bottom of the chat
    
    while True:
        user1_input = input("多模态对话:", type=TEXT)
        if user1_input is None:
            break
        chat_log.append(('User1', user1_input))
        show_chat()
        
        user2_input = input("没有做内容的多模态，得自言自语，要不演示不了。:", type=TEXT,validate=check)
        if user2_input is None:
            break

        chat_log.append(('User2', user2_input))
        show_chat()
def check(t):
    pattern = r'^[a-zA-Z0-9.,!? ]*$'
    if bool(re.match(pattern, t))==False:
        return '太菜了，不会把中文翻译成英文（中文标点也会不行'
    
def getimg(text):
    url="http://192.168.31.2:886"

    payload={
        "prompt":text,
        "negative_prompt": "EasyNegative",
        "steps": 20,
        'width': 512,
        'height': 512,
        # 'sd_model_checkpoint': 'anything-v5-PrtRE.safetensors [7f96a1a9ca]'
        'sd_model_checkpoint': 'qteamixQ_omegaFp16.safetensors [39d6af08b2]'
    ,
    
    }
    response=requests.post(url=f'{url}/sdapi/v1/txt2img',json=payload)

    r=response.json()
    # print(r)
    for i in r['images']:
        image=Image.open(io.BytesIO(base64.b64decode(i)))
    return image

if __name__ == '__main__':
    chat()
