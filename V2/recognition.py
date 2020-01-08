import cv2
import numpy as np
import face_data_collect
import dlib
import face_recognition
import detect_face_recognition as dfr
def rect_to_bbox(rect):
    """获得人脸矩形的坐标信息"""
    # print(rect)
    x = rect[3]
    y = rect[0]
    w = rect[1] - x
    h = rect[2] - y
    return (x, y, w, h)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
face_cascade = cv2.CascadeClassifier('.\opencv_module\haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX

idnum = 0

# cam = cv2.VideoCapture(0)
# minW = 0.1*cam.get(3)#图像宽度
# minH = 0.1*cam.get(4)#图像高度

def face_rec(camera):
    # 下面读取摄像头图像，用矩形标识检测到脸部和训练后结果比对，打印出对应标签所对应名字

    with open('pace_names.txt', 'r') as f:
        face_names = f.read()
    names = face_names.split()
    #
    # minW = 0.1 * camera.get(3)  # 图像宽度
    # minH = 0.1 * camera.get(4)  # 图像高度
    # print(minH,minW)

    while(True):
        read, img = camera.read()
        img = np.fliplr(img).copy()

        # face_locations = face_recognition.face_locations(img)  # 定位图片中的人脸
        # src_faces = []
        # src_face_num = 0
        # for (i, rect) in enumerate(face_locations):
        #     src_face_num = src_face_num + 1
        #     (x, y, w, h) = rect_to_bbox(rect)#读取单个人脸的初始坐标与宽度，高度
        #     detect_face = img[y:y + h, x:x + w]#截取出人脸部分
        #     detect_face = cv2.cvtColor(detect_face, cv2.COLOR_BGR2GRAY)#灰度化
        #     src_faces.append(detect_face)
        #     # cv2.imshow("face", detect_face)
        #     # 用框框圈住人脸，注意位置偏移
        #     img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #     # cv2.imshow("image", img)
        # # 人脸对齐操作并保存
        # faces_aligned = dfr.face_alignment(src_faces)
        # face_num = 0
        # for roi_gray in faces_aligned:
        #     face_num = face_num + 1
        #     # cv2.imshow("Align_face", roi_gray)

        # #harr方法检测人脸
        #由于读取的摄像头大小为640x480，所以设置人脸最小为60x60
        faces = face_cascade.detectMultiScale(img, 1.3, 5,minSize=(60,60))
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            roi_gray = gray[y:y + h,x:x + w]#注意别弄错了位置

            try:
                roi_gray = cv2.resize(roi_gray, (200,200), interpolation=cv2.INTER_LINEAR)
                params = recognizer.predict(roi_gray)
                print("name:%s,Confidence:%.2f" % (names[params[0]], params[1]))
                if params[1] < 70:#低于50以下是好的识别参考值，高于80的参考值都会认为是低的置信度评分
                    cv2.putText(img, names[params[0]],(x,y-20),cv2.FONT_HERSHEY_SIMPLEX, 1,255,2)
                    cv2.putText(img, "Confidence:"+str((int)(params[1])), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
            except:
                continue

        if cv2.waitKey(int(1000/12)):
            break
    return img



if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    face_rec(camera)


