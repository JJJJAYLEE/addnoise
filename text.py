import numpy as np

# 创建一个二维数组
original_array = np.array([[1, 2],
                            [3, 4]])

# 获取原始数组的高度和宽度
H, W = original_array.shape

# 假设通道数为3
C = 3

# 使用 np.newaxis 在原始数组上添加一个新轴，并重复该轴上的数组
repeated_array = np.repeat(original_array[:, :, np.newaxis], C, axis=2)

# 显示结果
print(repeated_array)
