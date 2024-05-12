import os
import random

import cv2
import numpy as np


def duibidu_change(im):
    im = im.copy()
    im = im.astype(np.float64)
    a = random.uniform(0.5, 2)
    if a > 1.5:
        b = random.uniform(-70, -40)
    elif 1 < a <= 1.5:
        b = random.uniform(-40, -10)
    else:
        b = random.uniform(1, 10)
    im = a * im + b
    im[im < 0] = 0
    im[im > 255] = 255
    im = im.astype(np.uint8)

    # cv2.imshow('0', im)

    return im


# def gauss_change(im, mua, sigma, rate):
#     im = im.copy()
#     num_im = im.shape[0] * im.shape[1]
#     num_false = int(num_im * (1 - rate))
#
#     index_false = np.array(random.sample(range(0, num_im - 1), num_false), dtype=np.int64)
#
#     im_false = np.zeros(num_im, dtype=np.int64)
#     im_false[index_false] = 1
#
#     im_false = im_false.reshape(im[:, :, 0].shape) == 1
#
#     # 产生高斯 noise
#     noise = np.random.normal(mua, sigma, im[:, :, 0].shape)
#
#     noise[im_false] = 0
#
#     im = im.astype(np.float64)
#     # 将噪声和图片叠加
#
#     im_0 = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float64)
#     r = noise / (im_0 + 1E-7)
#     gaussian_out = np.zeros_like(im, dtype=np.float64)
#     gaussian_out[:, :, 0] = im[:, :, 0] * (1 + r)
#     gaussian_out[:, :, 1] = im[:, :, 1] * (1 + r)
#     gaussian_out[:, :, 2] = im[:, :, 2] * (1 + r)
#     # gaussian_out = im + noise
#     # 将超过 1 的置 1，低于 0 的置 0
#     gaussian_out = np.clip(gaussian_out, 0, 255)
#     gaussian_out = gaussian_out.astype(np.uint8)
#
#     # cv2.imshow('1', gaussian_out)
#     return gaussian_out

def gauss_change(im, mua, sigma, rate, scale=0.):
    im = im.copy()
    num_im = im.shape[0] * im.shape[1]
    num_false = int(num_im * (1 - rate))

    index_false = np.array(random.sample(range(0, num_im - 1), num_false), dtype=np.int64)

    im_false = np.zeros(num_im, dtype=np.int64)
    im_false[index_false] = 1

    im_false = im_false.reshape(im[:, :, 0].shape) == 1

    # 使用 np.newaxis 在原始数组上添加一个新轴，并重复该轴上的数组
    im_false = np.repeat(im_false[:, :, np.newaxis], im.shape[2], axis=2)

    # 产生高斯 noise
    noise = np.random.normal(mua, sigma, im.shape)
    noise[im_false] = mua

    # 对噪声进行缩放
    # 计算仿射变换矩阵
    scale = random.random() * scale + 1

    M = np.float32([[scale, 0, 0],
                    [0, scale, 0]])

    noise = cv2.warpAffine(noise, M, (noise.shape[1], noise.shape[0]))

    noise_image = noise + im.astype(np.float64) - mua  # 将原图与噪声叠加
    noise_image = np.clip(noise_image, 0, 255).astype(np.uint8)
    return noise_image


def yanjiao_change(im, rate, scale=0.):
    im = im.copy()
    height, width = im.shape[0], im.shape[1]  # 获取高度宽度像素值
    num = int(height * width * rate)  # 一个准备加入多少噪声小点
    index_false = np.array(random.sample(range(0, height * width - 1), num), dtype=np.int64)
    im_false = np.zeros(height * width, dtype=np.int64)
    im_false[index_false] = 1
    im_false = im_false.reshape(im.shape[:2]) == 1
    noise_im = np.random.randint(2, size=im.shape[:2])

    # 计算仿射变换矩阵
    scale = random.random() * scale + 1

    M = np.float32([[scale, 0, 0],
                    [0, scale, 0]])

    noise_im = cv2.warpAffine(noise_im, M, (noise_im.shape[1], noise_im.shape[0]))


    im = im.astype(np.float64) / 255
    im[im_false, 0] = noise_im[im_false]
    im[im_false, 1] = noise_im[im_false]
    im[im_false, 2] = noise_im[im_false]
    im = np.uint8(im * 255)
    # cv2.imshow('2', im)
    return im


def bosong_change(im, bo_mean, scale):
    im = im.copy()
    noise_type = np.random.poisson(lam=bo_mean, size=im.shape).astype(np.float64)  # lam>=0 值越小，噪声频率就越少，size为图像尺寸

    scale = random.random() * scale + 1

    M = np.float32([[scale, 0, 0],
                    [0, scale, 0]])
    noise_type = cv2.warpAffine(noise_type, M, (noise_type.shape[1], noise_type.shape[0]))

    noise_image = noise_type + im.astype(np.float64) - bo_mean  # 将原图与噪声叠加
    noise_image = np.clip(noise_image, 0, 255).astype(np.uint8)
    return noise_image


def change_image(
        img_list: list,
        is_all=False,
        index=0,
        duibidu=False,
        gauss=False,
        yanjiao=False,
        bosong=False,
        epochs=1,
        g_mean=0,
        g_sigma=0.1,
        g_low=0.5,
        g_height=0.6,
        y_low=0.5,
        y_height=0.6,
        bo_mean=75,
        scale=0.,

):
    ims = img_list if is_all else [img_list[index]]

    out_ims = []

    for im1 in ims:
        for _ in range(epochs):
            im = im1.copy()
            if duibidu:
                im = duibidu_change(im)

            if gauss:
                rate_g = random.uniform(g_low, g_height)
                im = gauss_change(im, g_mean, g_sigma, rate_g, scale)

            if yanjiao:
                rate_y = random.uniform(y_low, y_height)
                im = yanjiao_change(im, rate_y, scale)
            if bosong:
                im = bosong_change(im, bo_mean, scale)

            # cv2.waitKey(1)
            out_ims.append(im)
    return out_ims


def makedir(path="./SaveImg"):
    """
    创建文件夹
    :param path: 路径
    :return:
    """
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def save_ims(imgs: list, path_im: list, save_dir='', index=0, start_num=0, change_sign='one', make_dir=True,
             yuanmingbaocun=False):
    N = len(path_im) if change_sign == 'all' else 1
    num_one = int(len(imgs) / N)  # 一组图片的张书

    # 确定名字
    image_name = []  # 每张图片名字
    imgs_name = []  # 一组图片名字
    if change_sign == 'one':
        #  只有一张图片
        image_name = [os.path.basename(path_im[index]) for _ in imgs]
        imgs_name = [os.path.basename(path_im[index])]
    else:
        # 有N张图片
        for i in range(len(path_im)):
            for j in range(num_one):
                image_name.append(os.path.basename(path_im[i]))
            imgs_name.append(os.path.basename(path_im[i]))

    save_img_parent = []
    if make_dir:
        for name in imgs_name:
            i = 0
            while 1:
                folder = os.path.exists(save_dir + '/' + os.path.splitext(name)[0])
                if folder:
                    i += 1
                    folder1 = os.path.exists(save_dir + '/' + os.path.splitext(name)[0] + '(' + str(i) + ')')
                    if not folder1:
                        break
                else:
                    break
            name = save_dir + '/' + os.path.splitext(name)[0] if i == 0 else save_dir + '/' + os.path.splitext(name)[
                0] + '(' + str(i) + ')'
            os.makedirs(name)
            save_img_parent.append(name)
    else:

        for _ in range(len(imgs_name)):
            save_img_parent.append(save_dir)

    for i, f in enumerate(save_img_parent):
        for j in range(num_one):
            id_im = i * num_one + j
            img = imgs[id_im]
            n = j + start_num

            if yuanmingbaocun:
                p = f + '/' + image_name[id_im]
            else:
                if n == 0:
                    p = f + '/' + os.path.splitext(image_name[id_im])[0] + ' - copy' + \
                        os.path.splitext(image_name[id_im])[
                            1]
                else:
                    p = f + '/' + os.path.splitext(image_name[id_im])[0] + ' - copy (' + str(n) + ')' + \
                        os.path.splitext(image_name[id_im])[1]

            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.imwrite(p, img)
