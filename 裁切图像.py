import os
import random

import cv2
import numpy as np



# # 原始图片文件夹路径
# original_folder = "./AAA"
#
# # 新建文件夹的路径
# new_folder = "./BBB"
# if not os.path.exists(new_folder):
#     os.makedirs(new_folder)
#
# # 裁切的目标大小
# target_size = 640, 512
#
#
# # 遍历原始图片文件夹中的所有图片文件
# for filename in os.listdir(original_folder):
#     file_path = os.path.join(original_folder, filename)
#     # 判断是否为文件
#     if os.path.isfile(file_path):
#         # 读取图片
#         img = cv2.imread(file_path)
#         # 获取图片的高度和宽度
#         h, w = img.shape[:2]
#
#         nh, nw = min(h, target_size[1]), min(w, target_size[0])
#         sh = random.randint(0, h - nh + 1)
#         sw = random.randint(0, w - nw + 1)
#
#         new_img = img[sh:nh + sh, sw:nw+sw, :]
#         cv2.imshow("0", new_img)
#         cv2.waitKey(0)



        #
        #
        #
        #
        #
        #
        #
        # # 保存缩放后的图片到新建文件夹中
        # new_filename = os.path.join(new_folder, filename)
        # # cv2.imwrite(new_filename, resized_img)

img = cv2.imread("C:\\Users\\29731\\Desktop\\214.jpg")
h, w = img.shape[:2]
scale = 640.0 / max(img.shape[:2])
resized_img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
cv2.imshow('0,', resized_img)
cv2.waitKey(0)
































