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

def check(t):
    pattern = r'^[a-zA-Z0-9.,!? ]*$'
    if bool(re.match(pattern, t))==False:
        return '太菜了，不会把中文翻译成英文（中文标点也会不行'
def trans():
    
    text=input('text2img', type=TEXT,   placeholder='请输入关键词（只能是英文的',validate=check)
    toast("图片转换中",color="success")
    # put_loading(shape='grow', color='secondary')
    put_image(getimg(text),width='2000px')
    put_button("返回",onclick=trans())

def main():
    trans()

if __name__=="__main__":
    main()