import pyautogui
import time
import os

#######################################
# 另一种截图方式：
# 指定某个区域，鼠标在区域内则截取区域图
#######################################

# 指定屏幕中的某个区域
region = (960, 1150, 1600, 300)  # 左上角坐标和宽高

# 指定文件夹路径
fp = r'output_frames'

# 创建文件夹
if not os.path.exists(fp):
    os.makedirs(fp)

last_in_region = False  # 记录上一次鼠标是否在指定区域
last_screenshot_time = 0  # 记录上一次截图的时间

while True:
    # 获取鼠标当前位置坐标
    x, y = pyautogui.position()
    
    # 判断鼠标是否在指定区域
    if region[0] <= x <= region[0] + region[2] and region[1] <= y <= region[1] + region[3]:
        if not last_in_region:  # 如果上一次鼠标不在指定区域
            # 截取指定区域的画面
            img = pyautogui.screenshot(region=region)
            
            # 保存截图到文件夹
            fn = str(time.time()) + '.png'
            file_path = os.path.join(fp, fn)
            img.save(file_path)
            
            print("成功截到图片" + fn)
            
            last_screenshot_time = time.time()  # 记录当前截图的时间
            last_in_region = True  # 记录当前鼠标在指定区域
            
        elif time.time() - last_screenshot_time >= 1:  # 如果上一次截图的时间超过1s
            # 截取指定区域的画面
            img = pyautogui.screenshot(region=region)
            
            # 保存截图到文件夹
            fn = str(time.time()) + '.png'
            file_path = os.path.join(fp, fn)
            img.save(file_path)
            
            print("成功截到图片" + fn)
            
            last_screenshot_time = time.time()  # 记录当前截图的时间
            
    else:
        last_in_region = False  # 如果鼠标不在指定区域，重置标志
    
    # 等待一段时间继续监视鼠标
    time.sleep(0.1)