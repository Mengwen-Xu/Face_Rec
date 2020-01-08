import cv2
# minW = camera.get(3)  # 图像宽度  480
# minH = camera.get(4)  # 图像高度    640
#开启摄像头，采集图像，并截取脸部存起来作为数据集
def Detect_Face():
    # opencv自带的人脸识别分类器
    face_cascade = cv2.CascadeClassifier('.\opencv_module\haarcascade_frontalface_default.xml')
    # 调用笔记本内置摄像头，所以参数为0，如果有其他的摄像头可以调整参数为1，2
    camera = cv2.VideoCapture(0)
    while (True):
        ret, frame = camera.read()#获取图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 灰度化
        faces = face_cascade.detectMultiScale(gray, 1.3, 5,minSize=(60,60))  # 人脸检测
        for (x, y, w, h) in faces:
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            f = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
            cv2.imshow("face", f)
        cv2.imshow("camera", frame)
        if cv2.waitKey(int(1000 / 12)) & 0xff == ord("q"):
            break
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    Detect_Face()
