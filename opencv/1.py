import os
import cv2
import time
def cap_pit():

    cap=cv2.VideoCapture(0)
    if not cap.isOpened():
        print('你看看你本地摄像头是不是坏了')

    group=0
    num=0
    start_time=time.time()

    while True:
        iswork,frame=cap.read()
        if not iswork:
            print('寄了')
            break
            
        cv2.imshow('cap',frame)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break