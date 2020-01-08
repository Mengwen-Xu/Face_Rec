import numpy as np
import os
import cv2
import pyqt
picture_path = 'data_collection'# 人脸数据路径
recognizer = cv2.face.LBPHFaceRecognizer_create()#cv中自带的识别模型
detector = cv2.CascadeClassifier('.\opencv_module\haarcascade_frontalface_default.xml')#cv中的检测人脸文件
face_names = []




#读取样本文件，并加载到一个列表里，返回值包括2部分，[文件列表，对应标签],标签用来对照姓名用。
def read_image(path,sz=None):
    pr_img=[] #图像列表
    pr_flg=[] #对应标签
    pr_count=0 #初始化检测到的人数
    for dirname,dirnames,filenames in os.walk(path):#遍历当前程序目录
        # print("1",dirname,dirnames,filenames)
        for subdirname in dirnames: #遍历程序文件夹下的各个目录
            # print("2",subdirname, dirnames)
            subject_path=os.path.join(dirname,subdirname)
            #这时候subdirname是循环处理data_collection文件夹下的文件夹，这时如果有新的面孔加进来需要更新标签名字
            face_names.append(subdirname)
            for filename in os.listdir(subject_path): #遍历文件夹下文件
                try:
                    filepath=os.path.join(subject_path,filename)
                    im=cv2.imread(filepath,cv2.IMREAD_GRAYSCALE) #读取文件下PGM文件
                    if im.shape!=(200,200): #判断像素是否200
                        im=cv2.resize(im,(200,200))
                    pr_img.append(np.asarray(im,dtype=np.uint8)) #添加图像
                    pr_flg.append(pr_count)#添加标签
                except:
                    print("io error")
            pr_count+=1 #另一个人的标签

    with open('pace_names.txt', 'w') as f: #把名字写入文件
        f.write(' '.join(face_names)) #每个元素间加一个空格转换为字符串
    return [pr_img, pr_flg]


def train_model(path, epoch=5):
    print('Training faces. It will take a few seconds. Wait ...')
    faces, ids = read_image(path)
    if os.path.exists('trainer.yml'):#是否存在文件
        A = recognizer.read('trainer.yml')  #读取模型参数
    for s in range(1, epoch):
        print('Training ...  %dth' % s)
        recognizer.train(faces, np.array(ids))  #训练模型

    recognizer.write('trainer.yml')         #保存模型参数
    print('Complete the training ！')


if __name__ == "__main__":
    train_model(picture_path, 10)