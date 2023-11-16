import cv2
import mediapipe as mp
from emonet.models import EmoNet
import torch
import numpy as np
from pathlib import Path

emo_dic = {0:'Neutral',1:'Happy',2:'Sad',3:'Surprise',4:'Fear',5:'Disgust',6:'Anger', 7:'Contempt'}
rec_weight = [.8, 80., 1. ,50., .8, 1., 1., 100.]

n_expression = 8
device = 'cuda:0'

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

state_dict_path = Path(__file__).parent.joinpath('pretrained', f'emonet_{n_expression}.pth')

print(f'Loading the model from {state_dict_path}.')
state_dict = torch.load(str(state_dict_path), map_location='cpu')
state_dict = {k.replace('module.',''):v for k,v in state_dict.items()}

emo_net = EmoNet(n_expression=n_expression).to(device)
emo_net.load_state_dict(state_dict, strict=False)
emo_net.eval()

cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5) as face_detection:

  while cap.isOpened():
    success, image = cap.read()
    if image==None:
       continue
    if not success:
      print("Ignoring empty camera frame.")
      continue

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    img_w = image.shape[0]
    img_h = image.shape[1]
    if results.detections:
      for detection in results.detections:
        # print(detection)
        mp_drawing.draw_detection(image, detection)
        
        xmin = int(detection.location_data.relative_bounding_box.xmin * img_w)
        ymin = int(detection.location_data.relative_bounding_box.ymin * img_h)
        width = int(detection.location_data.relative_bounding_box.width * img_w)
        height = int(detection.location_data.relative_bounding_box.height * img_w)
        ymin = max(0, ymin)
        xmin = max(0,xmin)
        face = cv2.resize(image[ymin:ymin+width, xmin:xmin+width], (256,256))

        face_tensor = torch.from_numpy(face / 255).permute(2, 0, 1).float()
        # print(face_tensor.shape)
        # print(face_tensor.unsqueeze(0).shape)

        with torch.no_grad():
            inputs = face_tensor.unsqueeze(0).to(device)
            outputs = emo_net(inputs)

        res = torch.nn.Softmax()(outputs['expression'])
        scores = res.cpu().detach().numpy()[0]
        scores = np.asarray([scores[i]*rec_weight[i] for i in range(8)])
        expression = emo_dic[scores.argmax()]
        bar = np.round(scores,4)

        cv2.putText(image, expression, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        for i, score in enumerate(bar):
            h = int(score*100) 
            # cv2.rectangle(image, (xmin, ymin+i*20), (xmin+h, ymin+i*20+15), (0,255,0), -1)
            # cv2.putText(image, emo_dic[i]+": "+str(score), (xmin+h+10, ymin+i*20+12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
            
            cv2.rectangle(image, (xmin, ymin+i*20), (xmin+h, ymin+i*20+15), (0,255,0), -1)
            cv2.putText(image, emo_dic[i]+": "+str(score), (xmin+h+10, ymin+i*20+12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
            
    cv2.imshow('MediaPipe Face Detection', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()