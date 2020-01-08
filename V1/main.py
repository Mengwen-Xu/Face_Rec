import sys
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from pyqt import *  #引用界面文件
import recognition


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
            self.pushButton_2.setText("Close Camera")
            self._timer.start()
        else:
            self.camera.release()
            self.pushButton.setText("Open Camera")
            self._timer.stop()

    def btnCloseCamera_Clicked(self):
       pass

    @QtCore.pyqtSlot()
    def _queryFrame(self):
        '''
        循环捕获图片
        '''
        self.frame = recognition.face_rec(self.camera)
        # ret, self.frame = self.camera.read()
        img_rows, img_cols, channels = self.frame.shape
        bytesPerLine = channels * img_cols

        cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
        QImg = QImage(self.frame.data, img_cols, img_rows,
                      bytesPerLine, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(self.frame).scaled(
            self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PyQtMainEntry()
    window.show()
    sys.exit(app.exec_())
