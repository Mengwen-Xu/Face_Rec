import dlib
import face_recognition
import math
import numpy as np
import cv2
#人脸检测+对齐
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
def rect_to_bbox(rect):
    """获得人脸矩形的坐标信息"""
    # print(rect)
    x = rect[3]
    y = rect[0]
    w = rect[1] - x
    h = rect[2] - y
    return (x, y, w, h)


def face_alignment(faces):
    faces_aligned = []# 预测关键点
    for face in faces:
        rec = dlib.rectangle(0, 0, face.shape[0], face.shape[1])
        shape = predictor(np.uint8(face), rec)
        # left eye, right eye, nose, left mouth, right mouth
        order = [36, 45, 30, 48, 54]
        for j in order:
            x = shape.part(j).x
            y = shape.part(j).y
        eye_center = ((shape.part(36).x + shape.part(45).x) * 1. / 2,  # 计算两眼的中心坐标
                      (shape.part(36).y + shape.part(45).y) * 1. / 2)
        dx = (shape.part(45).x - shape.part(36).x)
        dy = (shape.part(45).y - shape.part(36).y)
        angle = math.atan2(dy, dx) * 180. / math.pi     # 计算角度
        RotateMatrix = cv2.getRotationMatrix2D(eye_center, angle, scale=1) # 计算仿射矩阵
        # 进行仿射变换，即旋转
        RotImg = cv2.warpAffine(face, RotateMatrix, (face.shape[0], face.shape[1])
                                ,borderMode=cv2.BORDER_CONSTANT, borderValue=(125, 125, 125))

        faces_aligned.append(RotImg)
    return faces_aligned


def test( ):
    camera = cv2.VideoCapture(0)
    while (True):
        read, img = camera.read()
        # 定位图片中的人脸
        face_locations = face_recognition.face_locations(img)
        # 提取人脸区域的图片并保存
        src_faces = []
        src_face_num = 0
        for (i, rect) in enumerate(face_locations):
            src_face_num = src_face_num + 1
            (x, y, w, h) = rect_to_bbox(rect)
            detect_face = img[y:y + h, x:x + w]
            detect_face = cv2.cvtColor(detect_face, cv2.COLOR_BGR2GRAY)
            src_faces.append(detect_face)
            cv2.imshow("face", detect_face)
            #用框框圈住人脸
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imshow("image", img)
        # 人脸对齐操作并保存
        faces_aligned = face_alignment(src_faces)
        face_num = 0
        for faces in faces_aligned:
            face_num = face_num + 1
            cv2.imshow("Align_face", faces)

        if cv2.waitKey(int(1000/12)) & 0xff == ord("q"):
            break
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    test( )
    print(" SUCCEED !!! ")

