import sys

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QDialog, QApplication


class SettingWindow(QDialog):
    setting_signal = pyqtSignal(bool, bool, bool, bool, int, float, float, float, float, float, float, int, float)

    def __init__(self, ui_path='', show=False, duibidu=False, gauss=False, yanjiao=False, bosong=False, epochs=1,
                 g_mean=0, g_sigma=0.1,
                 g_low=0.5, g_height=0.6, y_low=0.5, y_height=0.6, bo_mean=75, scale=0.):
        super().__init__()
        self.ui_path = ui_path

        self.ui = self.init_ui(duibidu, gauss, yanjiao, bosong, epochs, g_mean, g_sigma, g_low, g_height, y_low,
                               y_height, bo_mean, scale)
        if show:
            self.ui.show()

        # 参数
        self.duibidu = duibidu  # 对比度变化标志
        self.gauss = gauss  # 高斯变化标志
        self.yanjiao = yanjiao  # 盐椒标志
        self.bosong = bosong  # 泊松标志

        self.epochs = epochs
        self.g_mean = g_mean
        self.g_sigma = g_sigma
        self.g_low = g_low
        self.g_height = g_height
        self.y_low = y_low
        self.y_height = y_height
        self.bo_mean = bo_mean
        self.scale = scale

        # 噪声方式
        self.gauss_noise_box = self.ui.checkBox
        self.yanjiao_noise_box = self.ui.checkBox_2
        self.duibidu_box = self.ui.checkBox_3
        self.bosong_box = self.ui.checkBox_4
        # toggled
        # 按钮
        self.sure_btn = self.ui.pushButton
        self.cancel_btn = self.ui.pushButton_2

        # 变换轮数
        self.epochs_box = self.ui.spinBox

        # 噪声参数
        self.gauss_mean = self.ui.doubleSpinBox
        self.gauss_sigma = self.ui.doubleSpinBox_2
        self.gauss_rate_low_threshold = self.ui.doubleSpinBox_3
        self.gauss_rate_height_threshold = self.ui.doubleSpinBox_4

        self.yanjiao_low_threshold = self.ui.doubleSpinBox_5
        self.yanjiao_rate_height_threshold = self.ui.doubleSpinBox_6
        self.scale_box = self.ui.doubleSpinBox_7

        self.bosong_mean = self.ui.spinBox_2

        # 槽连接
        self.gauss_noise_box.stateChanged.connect(self.gauss_change)
        self.yanjiao_noise_box.stateChanged.connect(self.yanjiao_change)
        self.bosong_box.stateChanged.connect(self.bosong_change)
        self.sure_btn.clicked.connect(self.sure_change)
        self.cancel_btn.clicked.connect(self.cancel_change)

    def init_ui(self, duibidu=False, gauss=False, yanjiao=False, bosong=False, epochs=1, g_mean=0, g_sigma=0.1,
                g_low=0.5, g_height=0.6, y_low=0.5, y_height=0.6, bo_mean=75, scale=0.):
        """
        初始化gui界面
        :return:
        """
        ui = uic.loadUi(self.ui_path)

        ui.checkBox.setChecked(gauss)
        ui.checkBox_2.setChecked(yanjiao)
        ui.checkBox_3.setChecked(duibidu)
        ui.checkBox_4.setChecked(bosong)
        self.open_or_close(ui, 'gauss', gauss)
        self.open_or_close(ui, 'yanjiao', yanjiao)
        self.open_or_close(ui, 'bosong', bosong)

        ui.doubleSpinBox.setValue(g_mean)
        ui.doubleSpinBox_2.setValue(g_sigma)
        ui.doubleSpinBox_3.setValue(g_low * 100)
        ui.doubleSpinBox_4.setValue(g_height * 100)
        ui.doubleSpinBox_5.setValue(y_low * 100)
        ui.doubleSpinBox_6.setValue(y_height * 100)
        ui.spinBox_2.setValue(bo_mean)
        ui.spinBox.setValue(epochs)
        ui.doubleSpinBox_7.setValue(scale)

        return ui

    def open_or_close(self, ui=None, name='all', enabled=False):
        """
        :param ui: ui
        :param name: 'gauss', 'yanjiao' 或者 'all'
        :param enabled: 'False表示禁用， True表示开启'
        :return:
        """
        if name == 'gauss':
            ui.label_2.setEnabled(enabled)
            ui.label_3.setEnabled(enabled)
            ui.label_4.setEnabled(enabled)
            ui.label_5.setEnabled(enabled)
            ui.label_8.setEnabled(enabled)
            ui.label_9.setEnabled(enabled)

            ui.doubleSpinBox.setEnabled(enabled)
            ui.doubleSpinBox_2.setEnabled(enabled)
            ui.doubleSpinBox_3.setEnabled(enabled)
            ui.doubleSpinBox_4.setEnabled(enabled)

        if name == 'yanjiao':
            ui.label_6.setEnabled(enabled)
            ui.label_7.setEnabled(enabled)
            ui.label_10.setEnabled(enabled)
            ui.label_11.setEnabled(enabled)

            ui.doubleSpinBox_5.setEnabled(enabled)
            ui.doubleSpinBox_6.setEnabled(enabled)

        if name == 'bosong':
            ui.label_13.setEnabled(enabled)
            ui.spinBox_2.setEnabled(enabled)

        #
        # else:
        #     ui.label_2.setEnabled(enabled)
        #     ui.label_3.setEnabled(enabled)
        #     ui.label_4.setEnabled(enabled)
        #     ui.label_5.setEnabled(enabled)
        #     ui.label_8.setEnabled(enabled)
        #     ui.label_9.setEnabled(enabled)
        #
        #     ui.doubleSpinBox.setEnabled(enabled)
        #     ui.doubleSpinBox_2.setEnabled(enabled)
        #     ui.doubleSpinBox_3.setEnabled(enabled)
        #     ui.doubleSpinBox_4.setEnabled(enabled)
        #
        #     ui.label_6.setEnabled(enabled)
        #     ui.label_7.setEnabled(enabled)
        #     ui.label_10.setEnabled(enabled)
        #     ui.label_11.setEnabled(enabled)
        #
        #     ui.doubleSpinBox_5.setEnabled(enabled)
        #     ui.doubleSpinBox_6.setEnabled(enabled)

    def gauss_change(self):
        if self.gauss_noise_box.isChecked():
            self.open_or_close(self.ui, 'gauss', True)
        else:
            self.open_or_close(self.ui, 'gauss', False)

    def yanjiao_change(self):
        if self.yanjiao_noise_box.isChecked():
            self.open_or_close(self.ui, 'yanjiao', True)
        else:
            self.open_or_close(self.ui, 'yanjiao', False)

    def bosong_change(self):
        if self.bosong_box.isChecked():
            self.open_or_close(self.ui, 'bosong', True)
        else:
            self.open_or_close(self.ui, 'bosong', False)

    def cancel_change(self):
        self.ui.reject()

    def sure_change(self):

        self.duibidu = True if self.duibidu_box.isChecked() else False
        self.epochs = self.epochs_box.value()

        if self.gauss_noise_box.isChecked():
            self.gauss = True

            if self.gauss_rate_height_threshold.value() < self.gauss_rate_low_threshold.value():
                self.gauss_rate_height_threshold.setValue(self.gauss_rate_low_threshold.value())

            self.g_mean = self.gauss_mean.value()
            self.g_sigma = self.gauss_sigma.value()
            self.g_low = (self.gauss_rate_low_threshold.value()) / 100
            self.g_height = (self.gauss_rate_height_threshold.value()) / 100
        else:
            self.gauss = False

        if self.yanjiao_noise_box.isChecked():
            self.yanjiao = True

            if self.yanjiao_rate_height_threshold.value() < self.yanjiao_low_threshold.value():
                self.yanjiao_rate_height_threshold.setValue(self.yanjiao_low_threshold.value())

            self.y_low = (self.yanjiao_low_threshold.value()) / 100
            self.y_height = (self.yanjiao_rate_height_threshold.value()) / 100

        else:
            self.yanjiao = False

        if self.bosong_box.isChecked():
            self.bosong = True
            self.bo_mean = self.bosong_mean.value()
        else:
            self.bosong = False

        self.scale = self.scale_box.value()

        self.setting_signal.emit(self.duibidu, self.gauss, self.yanjiao, self.bosong, self.epochs, self.g_mean,
                                 self.g_sigma, self.g_low,
                                 self.g_height, self.y_low, self.y_height, self.bo_mean, self.scale)
        self.ui.reject()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SettingWindow('../source/ui/setting_dialog.ui', True)
    app.exec_()
