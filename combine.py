import os
from PIL import Image
import time

########################################
# 将目录下的所有图片合成一张长图
########################################

# 定义图片所在目录和输出图片路径
input_dir = 'output_frames'
output_dir = 'C:/Users/libra/Desktop/cap/CC'

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 获取目录中的所有图片文件
image_files = [f for f in os.listdir(input_dir) if f.endswith('.png')]

# 按文件名排序
image_files.sort()

# 打开所有图片并计算总高度和最大宽度
images = [Image.open(os.path.join(input_dir, file)) for file in image_files]
widths, heights = zip(*(img.size for img in images))

total_height = sum(heights)
max_width = max(widths)

# 创建一个新的空白图像，尺寸为最大宽度和总高度
combined_image = Image.new('RGB', (max_width, total_height))

# 将每个图像粘贴到新图像中
y_offset = 0
for img in images:
    combined_image.paste(img, (0, y_offset))
    y_offset += img.height

# 创建一个规范的文件名
timestamp = time.strftime("%Y%m%d_%H%M%S")
output_filename = f'subtitles_{timestamp}.png'
output_image_path = os.path.join(output_dir, output_filename)

# 保存最终的拼接图像
combined_image.save(output_image_path)
print(f'Combined image saved as {output_image_path}')

