from transformers import AutoTokenizer, AutoModel


tokenizer = AutoTokenizer.from_pretrained("./dataroot/models/THUDM/chatglm2-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("./dataroot/models/THUDM/chatglm2-6b", trust_remote_code=True).half().cuda()
model = model.eval()

initialization = '''你叫小憨是东北大学悉尼智能科技学院HACI实验室的一个交互机器人。
                    你还在学习如何和人交互。你的回答风格是可爱，但是简短且直接。
                    如果你认为对话者聊不下去了，请结束对话，并说很开心和您聊天。
                    HACI实验室是人机情感计算与情感交互实验室。
                '''
_, history = model.chat(tokenizer, initialization, history=[])

while True:
    utts = input('user:')
    response, history = model.chat(tokenizer, utts, history=history)
    # print(history)
    print('bot:',response)
    if '拜拜' in utts or '很开心和您聊天' in response:
        break
    