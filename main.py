import os
import threading
from config import global_config


# 压缩线程（同步压缩）
class CompressThread(threading.Thread):
    # 构造方法
    def __init__(self, compressDir) -> None:
        threading.Thread.__init__(self)
        self.compressDir = compressDir

    # 运行方法
    def run(self) -> None:
        print("线程开始运行，压缩路径为：" + self.compressDir)
        # 获得锁
        threadLock.acquire()
        cmd = "pngquant 256 --quality=65-80 --skip-if-larger --force --ext .png " + self.compressDir + "\\*.png"
        os.system(cmd)
        # 释放锁
        threadLock.release()
        print("线程结束运行，压缩路径为：" + self.compressDir)


if __name__ == '__main__':
    configDirStr = global_config.getRaw("config", "compressDir")
    configDir = configDirStr.split(" ")
    print("当前配置需要压缩的文件夹为：")
    print(configDir)
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
        if dir in configDir:
            # 过滤编译文件夹
            if "build\generated" not in os.path.join(root, dir):
                thread = CompressThread(os.path.join(root, dir))
                threads.append(thread)
                thread.start()

# 开始遍历执行压缩线程
for thread in threads:
    thread.join()
