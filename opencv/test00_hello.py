
import cv2

# print(cv2.getVersionString())

# image = cv2.imread("opencv_logo.jpg")
# print(image.shape)


# cv2.imshow("image", image)
# cv2.waitKey()
import cv2
import time

# 创建视频捕获对象，0是代表本地摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

counter = 0  # 用于跟踪捕获的图像数量
group = 0    # 用于跟踪图像组
start_time = time.time()

while True:
    # 捕获摄像头的一帧
    ret, frame = cap.read()
    cv2.imshow('Camera Feed', frame)
    # 如果正确读取帧，ret为True
    if not ret:
        print("无法读取摄像头帧")
        break

    # 每秒截取一张图
    if time.time() - start_time >= 1:
        
        image_name = f"group_{group}_image_{counter}.jpg"
        # cv2.imwrite(image_name, frame)
        print(f"捕获并保存：{image_name}")
        start_time = time.time()
        counter += 1

        if counter == 4:
            counter = 0
            group += 1

    # 按'q'退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 完成所有操作后，释放捕获器
cap.release()
cv2.destroyAllWindows()

