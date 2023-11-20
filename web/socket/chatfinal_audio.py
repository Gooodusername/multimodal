from pywebio import start_server
from pywebio.output import put_text, put_html, put_buttons, clear, scroll_to, put_image, toast,use_scope
from pywebio_battery import put_audio
 
from pywebio.input import input, TEXT
from pywebio.session import set_env

import requests
import io
import base64
from PIL import Image
import re

import soundfile as sf
import socket
import pickle
from pydub import AudioSegment
import numpy as np

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
    
def get_aduio_client(text):#在本地存一个audio.wav的文件
    
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
        # for i, waveform in enumerate(audio_data):
        #     # 提取单个波形数据
        #     single_waveform = waveform[0]  # 假设每个波形只有一个声道

        #     # 将 numpy 数组转换为 pydub 可以处理的音频段
        #     audio_segment = AudioSegment(
        #         single_waveform.tobytes(), 
        #         frame_rate=16000,
        #         sample_width=single_waveform.dtype.itemsize, 
        #         channels=1
        #     )
            
        # # 保存为 MP3
        # put_audio(audio_segment)
        # audio_segment.export(f'audio.mp3', format='mp3')
        #! mp3的音质很差
        for i, waveform in enumerate(audio_data):
            # 提取单个波形数据
            single_waveform = waveform[0]  # 假设每个波形只有一个声道
            print(single_waveform)
            sf.write(f'audio.wav', single_waveform, 16000)  # 假设采样率是 16000 Hz

    else:
        print("未接收到数据")
    
    # print(single_waveform)
    # put_audio(single_waveform)

    clientsocket.close()
    

def show_chat(message):
    with use_scope('1'):
        pattern_img='^img.*'
        pattern_aud='^aud.*'
        pattern_ky='^ky.*'
        #!图片的识别
        if re.match(pattern_img,message) is not None:   
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
        #!只用音频的识别
        elif re.match(pattern_aud,message) is not None:
            toast("音频转换中", color="success")
            keyword = message.split(':', 1)[1]
            audio=get_aduio_client(keyword)
                
            put_html('<div style="display: flex; justify-content: flex-end; margin: 10px;">'
                            '<div style="padding: 15px; background-color: #f2f2f2; color: #333; '
                            'border-radius: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); display: flex; align-items: center;">'
                            '<img src="https://pic.imgdb.cn/item/654bbca4c458853aef35895f.jpg" alt="User1 Avatar" '
                            'style="width: 30px; height: 30px; border-radius: 50%; margin-right: 10px;">'
                            f'{message}</div></div>')
                    
            put_html('<div style="margin: 10px; padding: 15px; background-color: #008CBA; color: #fff; '
                            'border-radius: 15px; box-shadow: -2px 2px 10px rgba(0,0,0,0.1); '
                            'width: fit-content;">'
                            f'<b style="color: #fff;">有求必应的多模态:</b></div>')
            with open('./audio.wav', 'rb') as file:
                mp3_bytes = file.read()
            put_audio(mp3_bytes)
   
        #! 音频与图片
        elif re.match(pattern_ky,message) is not None:
            toast("转换中", color="success")
            keyword = message.split(':', 1)[1]
            aud=get_aduio_client(keyword)
               
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
                            f'<b style="color: #fff;">有求必应的多模态:</b> </div>')
            
            put_image(img,width='300px')
            with open('./audio.wav', 'rb') as file:
                mp3_bytes = file.read()
                put_audio(mp3_bytes)
        
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
                            f'<b style="color: #fff;">有求必应的多模态:</b> {"你好呀"}</div>')
        put_text(" ")
        put_text(" ")
        
  
    scroll_to(scope='1',position='bottom')

def main():
    clear()
    set_env(title="多模态对话")
    put_html("<h1>多模态模型聊天，快来和我聊天吧</h1>")
    while True:
        user_input = input("多模态对话:", type=TEXT)
        if user_input is None:
            break
        show_chat(user_input)


if __name__ == '__main__':
    main()
