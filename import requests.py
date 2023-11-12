import requests
import io
import base64
from PIL import Image

url="http://192.168.31.2:886"

payload={
    "prompt":"beautiful lady",
    "negative_prompt": "EasyNegative",
    "steps": 20,
    'width': 512,
    'height': 512,
    # 'sd_model_checkpoint': 'anything-v5-PrtRE.safetensors [7f96a1a9ca]'
    'sd_model_checkpoint': 'qteamixQ_omegaFp16.safetensors [39d6af08b2]'
,
 
}

response=requests.post(url=f'{url}/sdapi/v1/txt2img',json=payload)

r = response.json()

for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
    image.save('1.png')
 