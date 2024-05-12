import cv2
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog


class view_window(QDialog):
    show_img_signal = pyqtSignal(list)

    def __init__(self, ui_path, images):
        super().__init__()
        self.ui = self.init_ui(ui_path)
        self.images = images

        self.im_index = 0  # 当前图像索引

        # 按键
        self.up_btn = self.ui.pushButton
        self.down_btn = self.ui.pushButton_2

        # 显示屏
        self.show_window = self.ui.label

        # 展示第一张
        self.show_images(self.images)

        # 链接信号
        # 下一张
        self.down_btn.clicked.connect(self.down)
        # 上一张
        self.up_btn.clicked.connect(self.up)
        # 展示
        self.show_img_signal.connect(self.show_images)

    def init_ui(self, ui_path):
        ui = uic.loadUi(ui_path)
        return ui

    def up(self):
        self.im_index -= 1
        self.show_img_signal.emit(self.images)

    def down(self):
        self.im_index += 1
        self.show_img_signal.emit(self.images)

    def show_images(self, images):
        # 编辑上下张
        if len(images) == 1:
            self.up_btn.setEnabled(False)
            self.down_btn.setEnabled(False)
        else:
            if self.im_index == 0:
                self.up_btn.setEnabled(False)
                self.down_btn.setEnabled(True)
            elif self.im_index == len(images) - 1:
                self.up_btn.setEnabled(True)
                self.down_btn.setEnabled(False)
            else:
                self.up_btn.setEnabled(True)
                self.down_btn.setEnabled(True)

        # 窗口大小
        width = self.show_window.width()
        height = self.show_window.height()

        im1 = images[self.im_index].copy()
        # 图片大小
        mh, nw = im1.shape[:2]

        # 比较图片大小与窗口大小, 进行缩放

        min_wh = min(width, height)
        im1 = cv2.resize(im1, (int(nw * min_wh / max(mh, nw)), int(mh * min_wh / max(mh, nw))))

        img = cv2.Mat(im1)

        rows = img.shape[0]
        cols = img.shape[1]

        # rgb图shape=3，灰度图shape=2
        if len(img.shape) == 3:
            qt_img = QImage(img, cols, rows, cols * img.shape[2], QImage.Format_RGB888)
        else:
            qt_img = QImage(img, cols, rows, cols * img.shape[2], QImage.Format_Indexed8)
        size = QSize(cols, rows)
        qt_img = qt_img.scaled(size)
        self.show_window.setPixmap(QPixmap(qt_img))
        self.show_window.setScaledContents(False)
