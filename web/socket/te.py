from pywebio_battery import put_audio
# import os
# print(os.getcwd())
with open('./audio.mp3', 'rb') as file:
    
    mp3_bytes = file.read()
put_audio(mp3_bytes)