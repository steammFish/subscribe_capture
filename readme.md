# subscribe_capture

监视屏幕画面，并截取字幕画面。（电影字幕、galgame游戏字幕等等）


1. 首先运行capture.py开始截取字幕画面，将截取的画面保存到当前目录下的目录output_frames。（可能存在相似的图片）
2. 然后运行similar.py去除掉相似的图片
3. 使用combime.py将图片合成长图保存到目录CC中。
4. 运行clear.ps1删除output_frames的缓存。