import os
import cv2
print(os.getcwd())
imgs=cv2.imread('opencv_logo.jpg')
cv2.imshow('imgs',imgs)
cv2.waitKey(1)