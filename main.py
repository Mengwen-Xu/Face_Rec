import sys
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from pyqt import *  #引用界面文件
import recognition
from train_face import *


class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.camera = cv2.VideoCapture(0)  # 0-调用笔记本内置摄像头,1-调用usb摄像头
        self.is_camera_opened = False  # 摄像头有没有打开标记

        # 定时器：30ms捕获一帧
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(30)

    def btnOpenCamera_Clicked(self):
        '''
        打开和关闭摄像头
        '''
        self.is_camera_opened = ~self.is_camera_opened
        if self.is_camera_opened:#摄像头开着呢
            self.camera = cv2.VideoCapture(0)
            self.pushButton.setText("Close Camera")
            self._timer.start()
        else:
            self.camera.release()
            self.pushButton.setText("Open Camera")
            self._timer.stop()


    def btnTrainData_Clicked(self):
        #调用训练数据模型
       self.printf('Training faces. It will take a few seconds. Wait ...')
       train_model(picture_path, 5)
       self.printf('Complete the training ！')


    @QtCore.pyqtSlot()
    def _queryFrame(self):
        # 循环捕获图片
        self.frame = recognition.face_rec(self.camera)
        img_rows, img_cols, channels = self.frame.shape#输出图像形状
        bytesPerLine = channels * img_cols
        cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)#转变成RGB颜色格式
        QImg = QImage(self.frame.data, img_cols,
                      img_rows,bytesPerLine, QImage.Format_RGB888)#装变成qt颜色格式
        #根据形状适应大小，并输出在label上
        self.label.setPixmap(QPixmap.fromImage(QImg).scaled(self.label.size(),
                                Qt.KeepAspectRatio, Qt.SmoothTransformation))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PyQtMainEntry()
    window.show()
    sys.exit(app.exec_())
