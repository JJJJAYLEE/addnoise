import sys

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QApplication


class SaveSettingWindow(QDialog):
    save_start_num_sign = pyqtSignal(int, bool, bool, bool)

    def __init__(self, ui_path):
        super().__init__()
        self.ui = self.init_ui(ui_path)

        self.sure_save = False
        self.make_dir = False
        self.yuanmingbaocun = False

        self.start_num_box = self.ui.spinBox
        self.make_dir_box = self.ui.checkBox
        self.sure_btn = self.ui.pushButton
        self.save_way_box = self.ui.checkBox_2

        self.sure_btn.clicked.connect(self.sure)

    def sure(self):
        start_num = self.start_num_box.value()
        if self.make_dir_box.isChecked():
            self.make_dir = True
        if self.save_way_box.isChecked():
            self.yuanmingbaocun = True
        self.sure_save = True
        self.save_start_num_sign.emit(start_num, self.make_dir, self.sure_save, self.yuanmingbaocun)
        self.ui.reject()

    def init_ui(self, ui_path):
        ui = uic.loadUi(ui_path)
        return ui


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SaveSettingWindow('../source/ui/save_image.ui')
    w.ui.show()
    app.exec_()
