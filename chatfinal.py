from pywebio import start_server
from pywebio.output import put_text, put_html, put_buttons, clear, scroll_to, put_image, toast,use_scope
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
    try:
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
    except Exception as e:
        return None  # 处理异常情况
    
    

def show_chat(message):
    with use_scope('1'):
        if message.startswith('image:'):   
            toast("图片转换中", color="success")
            keyword = message.split(':', 1)[1]   
            img=get_image(keyword)
                
            put_html('<div style="display: flex; justify-content: flex-end; margin: 10px;">'
                            '<div style="padding: 15px; background-color: #f2f2f2; color: #333; '
                            'border-radius: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); display: flex; align-items: center;">'
                            '<img src="https://pic.imgdb.cn/item/654bbca4c458853aef35895f.jpg" alt="User1 Avatar" '
                            'style="width: 30px; height: 30px; border-radius: 50%; margin-right: 10px;">'
                            f'{message}</div></div>')
                    
            put_html('<div style="margin: 10px; padding: 15px; background-color: #008CBA; color: #fff; '
                            'border-radius: 15px; box-shadow: -2px 2px 10px rgba(0,0,0,0.1); '
                            'width: fit-content;">'
                            f'<b style="color: #fff;">有求必应的多模态:</b>  </div>')
            put_image(img,width='300px')
        else: 
        
            put_html('<div style="display: flex; justify-content: flex-end; margin: 10px;">'
                            '<div style="padding: 15px; background-color: #f2f2f2; color: #333; '
                            'border-radius: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); display: flex; align-items: center;">'
                            '<img src="https://pic.imgdb.cn/item/654bbca4c458853aef35895f.jpg" alt="User1 Avatar" '
                            'style="width: 30px; height: 30px; border-radius: 50%; margin-right: 10px;">'
                            f'{message}</div></div>')
                    
            put_html('<div style="margin: 10px; padding: 15px; background-color: #008CBA; color: #fff; '
                            'border-radius: 15px; box-shadow: -2px 2px 10px rgba(0,0,0,0.1); '
                            'width: fit-content;">'
                            f'<b style="color: #fff;">有求必应的多模态:</b> {"不是我做的"}</div>')
        put_text(" ")
        put_text(" ")
        put_text(" ")
  
    scroll_to(scope='1',position='bottom')

def main():
    clear()
    set_env(title="多模态对话")
    put_html("<h1>有聊天框的多模态</h1>")
    while True:
        user_input = input("多模态对话:", type=TEXT)
        if user_input is None:
            break
        show_chat(user_input)


if __name__ == '__main__':
    main()
