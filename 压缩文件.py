import os
import cv2

# 原始图片文件夹路径
original_folder = "./AAA"

# 新建文件夹的路径
new_folder = "./BBB"
if not os.path.exists(new_folder):
    os.makedirs(new_folder)

# 缩放的目标大小
target_size = 640.0

# 遍历原始图片文件夹中的所有图片文件
for filename in os.listdir(original_folder):
    file_path = os.path.join(original_folder, filename)
    # 判断是否为文件
    if os.path.isfile(file_path):
        # 读取图片
        img = cv2.imread(file_path)
        # 获取图片的高度和宽度
        h, w = img.shape[:2]
        # 计算缩放比例
        if max(h, w) > target_size:
            scale = target_size / max(h, w)
        else:
            scale = 1
        # 缩放图片
        resized_img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
        # 保存缩放后的图片到新建文件夹中
        new_filename = os.path.join(new_folder, filename)
        cv2.imwrite(new_filename, resized_img)

print("缩放并保存完成")



