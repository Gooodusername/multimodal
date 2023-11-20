import socket
from audioldm import text_to_audio, build_model

audio=0

def server():
    serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    host=socket.gethostname()

    port=1234

    serversocket.bind((host,port))

    serversocket.listen(5)
     
    audioldm=build_model(model_name="audioldm-m-full")
 

    try:
        while True:
            clientsocket, addr = serversocket.accept()
            ms = clientsocket.recv(1024).decode('utf-8')  # 解码成字符串
            audio = text_to_audio(
                        latent_diffusion="audioldm-m-full",
                        text=ms,
                        seed=42,
                        duration=5,
                        guidance_scale=2.5,
                        n_candidate_gen_per_text=3
                    )
            clientsocket.close()
    except Exception as e:
        print("发生异常：", e)
    finally:
        serversocket.close()
    
    return audio

if __name__=="__main__":
    server()
    
