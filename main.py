import os
import threading


# 压缩线程（同步压缩）
class CompressThread(threading.Thread):
    # 构造方法
    def __init__(self, compressDir) -> None:
        threading.Thread.__init__(self)
        self.compressDir = compressDir

    # 运行方法
    def run(self) -> None:
        print("需要压缩的路径为：" + self.compressDir)
        print("线程开始运行：")
        # 获得锁
        threadLock.acquire()
        cmd = "pngquant 256 --force --ext .png " + self.compressDir + "\\*.png"
        os.system(cmd)
        # 释放锁
        threadLock.release()
        print("压缩线程已结束！")


if __name__ == '__main__':
    a = """
 _____ _             _____                                     _   
|  __ (_)           |  __ \                                   | |  
| |__) |  ___ ______| |__) | __   __ _  __ _ _   _  __ _ _ __ | |_ 
|  ___/ |/ __|______|  ___/ '_ \ / _` |/ _` | | | |/ _` | '_ \| __|
| |   | | (__       | |   | | | | (_| | (_| | |_| | (_| | | | | |_ 
|_|   |_|\___|      |_|   |_| |_|\__, |\__, |\__,_|\__,_|_| |_|\__|
                                  __/ |   | |                      
                                 |___/    |_|     
                                 
请选择需要压缩的文件夹路径：                                    
"""
print(a)
dirPath = input("请输入：")
# 初始化线程锁
threadLock = threading.Lock()
# 压缩线程数组
threads = []
# 开始历遍所有子文件夹
for root, dirs, files in os.walk(dirPath):
    for dir in dirs:
        if dir == "drawable-xhdpi" or dir == "drawable-xxhdpi":
            # 过滤编译文件夹
            if "build\generated" not in os.path.join(root, dir):
                thread = CompressThread(os.path.join(root, dir))
                threads.append(thread)
                thread.start()

# 开始遍历执行压缩线程
for thread in threads:
    thread.join()
