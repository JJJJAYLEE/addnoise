
import os
import shutil

# 原始图片文件夹路径
original_folder = "H:\\data\\SmartphoneImageDenoising\\Smartphone Image Denoising Dataset (SIDD)\\archive\\SIDD_Small_sRGB_Only\\Data"

# 新建文件夹的路径
new_folder = "./AAA"
if not os.path.exists(new_folder):
    os.makedirs(new_folder)

# 初始化计数器
count = 40

# 遍历原始图片文件夹中的子文件夹
for subdir in os.listdir(original_folder):
    subdir_path = os.path.join(original_folder, subdir)
    if os.path.isdir(subdir_path):
        # 获取子文件夹中的所有文件
        files = os.listdir(subdir_path)
        # 如果子文件夹中包含至少两张图片
        if len(files) >= 1:
            # 获取第一张图片的路径
            first_image = os.path.join(subdir_path, files[0])
            # 构造新的文件名
            new_filename = f"{count}.{files[0].split('.')[-1]}"
            # 复制图片到新建文件夹，并重新命名
            shutil.copy(first_image, os.path.join(new_folder, new_filename))
            # 更新计数器
            count += 1
