import os
import sys

import cv2
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

from son_windows.save_setting_window import SaveSettingWindow
from son_windows.view_window import view_window
from tools import change_image, save_ims
from son_windows.run_setting_window import SettingWindow


class MainWindow(QWidget):
    images_show_signal = pyqtSignal(list)  # 展示图片信号

    def __init__(self):
        super().__init__()

        self.ui = self.init_ui()
        self.ui.show()

        # 变化参数
        self.duibidu = False  # 对比度变化标志
        self.gauss = False  # 高斯变化标志
        self.yanjiao = False  # 盐椒标志
        self.bosong = False  # 泊松分布标志

        self.epochs = 1
        self.g_mean = 0.
        self.g_sigma = 10.
        self.g_low = 1.0
        self.g_height = 1.0
        self.y_low = 0.01
        self.y_height = 0.02
        self.bo_mean = 75
        self.scale = 0

        # 图像参数
        self.imgPath = []  # 图像地址列表
        self.imgAll = []  # 图像列表
        self.im_index = 0  # 目前图像索引
        self.changed_images = []  # 变化后的图像

        self.change_sign = 'one'  # 图像变化方式， one表示变化当前, all表示变化所有
        # 菜单栏
        # 1. 开始栏
        self.open_a_image_btn = self.ui.open_a_image
        self.open_images_btn = self.ui.open_images
        self.setting_btn = self.ui.setting

        # 2. 运行栏
        self.run_change_one_btn = self.ui.change_a_image
        self.run_change_all_btn = self.ui.change_images  # 变换所有

        # 显示界面
        self.show_window = self.ui.label

        # 自定义按钮
        self.change_one_btn = self.ui.pushButton_2
        self.change_all_btn = self.ui.pushButton_3  # 变换所有
        self.up_btn = self.ui.pushButton_5
        self.down_btn = self.ui.pushButton_4  # 下一张
        self.save_btn = self.ui.pushButton  # 保存
        self.show_btn = self.ui.pushButton_6

        # 信号与槽

        # 菜单栏
        #   开始栏
        self.open_a_image_btn.triggered.connect(self.open_a_img)  # 选择单张图片
        self.open_images_btn.triggered.connect(self.open_images_dir)  # 选择图片文件夹
        self.setting_btn.triggered.connect(self.setting)  # 设置

        #   运行栏
        self.run_change_one_btn.triggered.connect(self.change_a_img)  # 变换当前图片
        self.run_change_all_btn.triggered.connect(self.change_all_img)

        # 展示
        self.up_btn.clicked.connect(self.up)
        self.down_btn.clicked.connect(self.down)
        self.show_btn.clicked.connect(self.show_changed_images)

        # 自定义信号与槽
        # 展示图像
        self.images_show_signal.connect(self.show_images)

        # 变化图像
        self.change_one_btn.clicked.connect(self.change_a_img)
        self.change_all_btn.clicked.connect(self.change_all_img)

        # 保存
        self.save_btn.clicked.connect(self.save_images)

    def init_ui(self):
        ui = uic.loadUi("./source/ui/main.ui")

        # 关闭变化按钮
        self.open_or_close_run(ui, False)
        ui.pushButton.setEnabled(False)
        ui.pushButton_4.setEnabled(False)
        ui.pushButton_5.setEnabled(False)
        ui.pushButton_6.setEnabled(False)

        return ui

    def open_or_close_run(self, ui, isOpen=False):
        ui.change_a_image.setEnabled(isOpen)
        ui.change_images.setEnabled(isOpen)
        ui.pushButton_2.setEnabled(isOpen)
        ui.pushButton_3.setEnabled(isOpen)

    def open_a_img(self):  # 打开单张图片槽

        # 打开图片
        file_dialog = QFileDialog()
        img_filename = file_dialog.getOpenFileName(self, "打开图片", "./", "*.png\n *.jpg\n *.tif\n *.jpeg\n *bmp")
        imgPath = img_filename[0]  # 加载的图片路径

        if imgPath != '':  # 打开成功
            self.im_index = 0
            self.imgPath = [imgPath]
            img = cv2.imread(imgPath)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.imgAll = [img]
            self.images_show_signal.emit(self.imgAll)

        if (self.duibidu or self.gauss or self.yanjiao) and len(self.imgAll):
            self.open_or_close_run(self.ui, True)
            self.save_btn.setEnabled(False)
            self.show_btn.setEnabled(False)

    def open_images_dir(self):
        file_dialog = QFileDialog()
        dir_name = file_dialog.getExistingDirectory(self, "选择文件夹", "./")
        if dir_name != '':
            files = os.listdir(dir_name)
            self.imgPath = []
            self.imgAll = []
            self.im_index = 0
            for i in range(len(files)):
                if os.path.splitext(files[i])[1] in {'.jpg', '.png', '.tif', '.jpeg', '.bmp', '.PNG', '.JPG'}:
                    self.imgPath.append(files[i])
            for i in range(len(self.imgPath)):
                self.imgPath[i] = dir_name + '/' + self.imgPath[i]

            if len(self.imgPath):

                for name in self.imgPath:
                    img = cv2.imread(name)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    self.imgAll.append(img)

                self.images_show_signal.emit(self.imgAll)

            else:
                pass
                # todo 加一个没有图片的对话框

        if (self.duibidu or self.gauss or self.yanjiao) and len(self.imgAll):
            self.open_or_close_run(self.ui, True)
            self.save_btn.setEnabled(False)
            self.show_btn.setEnabled(False)

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

    def show_changed_images(self):
        show_win = view_window('./source/ui/view.ui', self.changed_images)
        show_win.ui.show()
        show_win.ui.exec()

    def setting(self):
        setting_win = SettingWindow('./source/ui/setting_dialog.ui', False, self.duibidu, self.gauss,
                                    self.yanjiao, self.bosong, self.epochs, self.g_mean, self.g_sigma, self.g_low,
                                    self.g_height,
                                    self.y_low, self.y_height, self.bo_mean,self.scale)
        setting_win.setting_signal.connect(self.setting_para)
        setting_win.ui.exec()

    def setting_para(self, duibidu, gauss, yanjiao, bosong, epochs, g_mean, g_sigma, g_low, g_height,
                     y_low, y_height, bo_mean, scale):
        self.duibidu = duibidu  # 对比度变化标志
        self.gauss = gauss  # 高斯变化标志
        self.yanjiao = yanjiao  # 盐椒标志
        self.bosong = bosong

        self.epochs = epochs
        self.g_mean = g_mean
        self.g_sigma = g_sigma
        self.g_low = g_low
        self.g_height = g_height
        self.y_low = y_low
        self.y_height = y_height
        self.bo_mean = bo_mean
        self.scale = scale

        if (self.duibidu or self.gauss or self.yanjiao or self.bosong) and len(self.imgAll):
            self.open_or_close_run(self.ui, True)
            self.save_btn.setEnabled(False)

        print(self.duibidu, self.gauss, self.yanjiao, self.bosong, self.epochs, self.g_mean, self.g_sigma, self.g_low,
              self.g_height,
              self.y_low, self.y_height, self.bo_mean, self.scale)

    def change_a_img(self):
        self.run_change_all_btn.setEnabled(False)
        self.change_all_btn.setEnabled(False)

        self.change_one_btn.clicked.disconnect(self.change_a_img)
        self.run_change_one_btn.triggered.disconnect(self.change_a_img)

        if self.run_change_one_btn.isChecked():
            self.change_one_btn.click()
        else:
            self.run_change_one_btn.trigger()

        changed_images = change_image(img_list=self.imgAll,
                                      is_all=False,
                                      index=self.im_index,
                                      duibidu=self.duibidu,
                                      gauss=self.gauss,
                                      yanjiao=self.yanjiao,
                                      bosong=self.bosong,
                                      epochs=self.epochs,
                                      g_mean=self.g_mean,
                                      g_sigma=self.g_sigma,
                                      g_low=self.g_low,
                                      g_height=self.g_height,
                                      y_low=self.y_low,
                                      y_height=self.y_height,
                                      bo_mean=self.bo_mean,
                                      scale=self.scale
                                      )
        self.changed_images = changed_images
        self.change_sign = 'one'

        self.change_one_btn.click()
        self.run_change_one_btn.trigger()

        self.change_one_btn.clicked.connect(self.change_a_img)
        self.run_change_one_btn.triggered.connect(self.change_a_img)

        self.run_change_all_btn.setEnabled(True)
        self.change_all_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.show_btn.setEnabled(True)

    def change_all_img(self):

        self.run_change_one_btn.setEnabled(False)
        self.change_one_btn.setEnabled(False)

        self.change_all_btn.clicked.disconnect(self.change_all_img)
        self.run_change_all_btn.triggered.disconnect(self.change_all_img)

        if self.run_change_all_btn.isChecked():
            self.change_all_btn.click()
        else:
            self.run_change_all_btn.trigger()

        changed_images = change_image(img_list=self.imgAll,
                                      is_all=True,
                                      index=self.im_index,
                                      duibidu=self.duibidu,
                                      gauss=self.gauss,
                                      yanjiao=self.yanjiao,
                                      bosong=self.bosong,
                                      epochs=self.epochs,
                                      g_mean=self.g_mean,
                                      g_sigma=self.g_sigma,
                                      g_low=self.g_low,
                                      g_height=self.g_height,
                                      y_low=self.y_low,
                                      y_height=self.y_height,
                                      bo_mean=self.bo_mean,
                                      scale=self.scale
                                      )
        self.changed_images = changed_images
        self.change_sign = 'all'

        self.change_all_btn.click()
        self.run_change_all_btn.trigger()

        self.change_all_btn.clicked.connect(self.change_all_img)
        self.run_change_all_btn.triggered.connect(self.change_all_img)

        self.run_change_one_btn.setEnabled(True)
        self.change_one_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.show_btn.setEnabled(True)

    def up(self):
        self.im_index -= 1
        self.images_show_signal.emit(self.imgAll)

    def down(self):
        self.im_index += 1
        self.images_show_signal.emit(self.imgAll)

    def _start_(self, data, make_dir, sure_save, yuanmingbaocun):
        self.start_number = data
        self.make_dir = make_dir
        self.sure_save = sure_save
        self.yuanmingbaocun = yuanmingbaocun

    def save_images(self):

        self.start_number = 0
        self.make_dir = True
        self.sure_save = False
        self.yuanmingbaocun = False

        save_window = SaveSettingWindow('./source/ui/save_image.ui')
        save_window.save_start_num_sign.connect(self._start_)
        save_window.ui.exec()

        if self.sure_save:
            file_dialog = QFileDialog()
            dir_name = file_dialog.getExistingDirectory(None, "选择文件夹", "./")

            save_ims(self.changed_images,
                     self.imgPath,
                     dir_name,
                     self.im_index,
                     self.start_number,
                     self.change_sign,
                     self.make_dir,
                     self.yuanmingbaocun
                     )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
