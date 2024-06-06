import cv2
import os

# 读取图像
image_files = [f for f in os.listdir('output_frames') if f.endswith('.png')]
if len(image_files) == 0:
    print("没有找到图像文件！")
    exit()

images = [cv2.imread(os.path.join('output_frames', f)) for f in image_files]
if any(img is None for img in images):
    print("读取图像时出错！")
    exit()

# 将图像转换为灰度图
grays = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in images]
if any(gray is None for gray in grays):
    print("转换图像为灰度图时出错！")
    exit()

# 提取图像特征
sift = cv2.SIFT_create()
keypoints_and_descriptors = [sift.detectAndCompute(gray, None) for gray in grays]
if any(kp is None or desc is None for kp, desc in keypoints_and_descriptors):
    print("提取图像特征时出错！")
    exit()

# 使用 FLANN 匹配器
flann = cv2.FlannBasedMatcher()
similarities = []

for i in range(len(keypoints_and_descriptors)):
    for j in range(i + 1, len(keypoints_and_descriptors)):
        keypoints1, descriptors1 = keypoints_and_descriptors[i]
        keypoints2, descriptors2 = keypoints_and_descriptors[j]

        matches = flann.knnMatch(descriptors1, descriptors2, k=2)

        # Lowe's ratio test
        good_matches = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)

        similarity = len(good_matches) / max(len(keypoints1), len(keypoints2))
        similarities.append((i, j, similarity))

# # 删除相似度达到 90% 的图像
# for i, j, similarity in similarities:
#     if similarity > 0.9:
#         os.remove(os.path.join('output_frames', image_files[j]))
#         print(f"删除图像 {image_files[j]}")



for i, j, similarity in similarities:
    if similarity > 0.9:
        file_path = os.path.join('output_frames', image_files[j])
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"删除图像 {image_files[j]}")
        else:
            print(f"文件 {file_path} 不存在")
