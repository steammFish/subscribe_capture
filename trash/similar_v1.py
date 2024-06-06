import cv2
import os

# 设置图像目录
image_dir = 'output_frames'

# 遍历目录下的所有 PNG 图像
image_files = [f for f in os.listdir(image_dir) if f.endswith('.png')]

# 创建 SIFT 特征提取器
sift = cv2.SIFT_create()

# 遍历图像并比较相似度
for i in range(len(image_files)):
    for j in range(i + 1, len(image_files)):
        image1_path = os.path.join(image_dir, image_files[i])
        image2_path = os.path.join(image_dir, image_files[j])

        # 检查图像是否存在
        if not os.path.exists(image1_path) or not os.path.exists(image2_path):
            continue

        # 读取图像
        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)

        # 将图像转换为灰度图
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # 提取图像特征
        kp1, des1 = sift.detectAndCompute(gray1, None)
        kp2, des2 = sift.detectAndCompute(gray2, None)

        # 使用 Brute-Force 匹配来计算图像相似度
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # 应用 ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])

        # 计算图像相似度
        similarity = len(good) / len(matches)

        print(f"图像 {image_files[i]} 和 {image_files[j]} 的相似度：{similarity:.2f}")

        # 如果相似度大于 85%，则删除图像
        if similarity > 0.85:
            os.remove(image2_path)
            print(f"删除图像 {image_files[j]}")