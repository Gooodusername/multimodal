from pathlib import Path

import torch
from torch.utils.data import DataLoader
from torchvision import transforms

from emonet.models import EmoNet
import glob
import pandas as pd
torch.backends.cudnn.benchmark =  True
import os

from PIL import Image
from torch.utils.data import Dataset

import cv2
import numpy as np

class BaseDataset(Dataset):
    def __init__(self, image_list, transform=None):

        self.imgs = image_list
        self.transform = transform

    def __getitem__(self, index):
        path = self.imgs[index]
        img = Image.open(path) #这里删了一个变量 
        if self.transform is not None:
            img = self.transform(img)

        return img, path

    def __len__(self):
        return len(self.imgs)



def save_expression(pathes, expression, valence, arousal):
    for i in range(len(pathes)):
        path = pathes[i]
        expression_ = expression[i]
        valence_ = valence[i]
        arousal_ = arousal[i]

        s = path.split('/')
        data_type, group, pid, img_id = s[-4], s[-3], s[-2], s[-1]
        img_id = img_id.split('.')[0]
        save_path = os.path.join('./data/extracted_expression', data_type, group, pid, img_id + '.pth')
       
        # expression_ = expression.unsqueeze(1) if expression.dim() == 0 else expression
        # valence_ = valence.unsqueeze(0) if valence.dim() == 0 else valence
        # arousal_ = arousal.unsqueeze(0) if arousal.dim() == 0 else arousal 存成csv
        valence_ = valence_.unsqueeze(0)
        arousal_ = arousal_.unsqueeze(0)
        save_tensor = torch.cat([expression_[0], valence_, arousal_],0)
        torch.save(save_tensor, save_path)

    return


def extract():
    n_expression = 8
    batch_size = 32
    n_workers = 16
    device = 'cuda:0'
    image_size = 256 

    # Create the data loaders
    transform_image = transforms.Compose([transforms.ToTensor(),
                                          transforms.Resize([image_size, image_size],antialias=None)]) #这里是个列表


    print(f'Testing the model on {n_expression} emotional classes')

    print('Loading the data')
    #emo_data = glob.glob('./data/Manually/1/*.jpg')#改成了jpg
    emo_data = glob.glob('C:/Users/A couputer/Documents/code/extract/emonet/emonet/data/Manually/*.jpg')#改成了jpg 
    print(emo_data)
    emo_dataset = BaseDataset(emo_data, transform=transform_image)


    test_dataloader = DataLoader(emo_dataset, batch_size=batch_size, shuffle=False, num_workers=n_workers)

    # Loading the model
    state_dict_path = Path(__file__).parent.joinpath('pretrained', f'emonet_{n_expression}.pth')

    print(f'Loading the model from {state_dict_path}.')
    state_dict = torch.load(str(state_dict_path), map_location='cpu')
    state_dict = {k.replace('module.',''):v for k,v in state_dict.items()}
    net = EmoNet(n_expression=n_expression).to(device)
    net.load_state_dict(state_dict, strict=False)
    net.eval()

    with torch.no_grad():
        # print(test_dataloader)
        for i, data in enumerate(test_dataloader):
            print(data)
            inputs, pathes = data
            inputs = inputs.to(device)
            outputs = net(inputs)

            expression = outputs['expression']
            valence = outputs['valence']
            arousal = outputs['arousal']
            print('expression=',expression)
            print('valence=',valence)
            print('arousal=',arousal)
            save_expression(pathes, expression, valence, arousal)
           
def cap_pit():

    cap=cv2.VideoCapture(0)
    if not cap.isOpened():
        print('你看看你本地摄像头是不是坏了')

    group=0
    num=0
    start_time=time.time()

    while True:
        iswork,frame=cap.read()
        cv2.imshow('cap',frame)
        if not iswork:
            print('寄了')
            break
         
        cappciture=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cappciture)
        
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    return pil_image

if __name__ == '__main__':
    extract()
     