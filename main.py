import os
import platform
import threading


# 压缩线程（同步压缩）
class CompressThread(threading.Thread):
    # 构造方法
    def __init__(self, rootPath, compressFile, compressPath, extensionName) -> None:
        threading.Thread.__init__(self)
        self.root = rootPath
        self.compressFile = compressFile
        self.path = compressPath
        self.extension = extensionName

    # 运行方法
    def run(self) -> None:
        print("\n线程开始运行，压缩图片路径为：" + self.path)
        # 获得锁
        threadLock.acquire()
        cmd = "pngquant 256 --quality=65-80 --skip-if-larger --force --ext .png " + self.path
        os.system(cmd)
        # 重命名后缀
        if self.extension == 'jpg' or self.extension == 'jpeg':
            os.remove(self.path)
            os.rename(os.path.join(self.root, self.compressFile + ".png"),
                      os.path.join(self.root, self.compressFile))
        # 释放锁
        threadLock.release()
        print("\n线程结束运行，压缩图片路径为：" + self.path)


if __name__ == '__main__':
    tag = """
 _____ _             _____                                     _   
|  __ (_)           |  __ \                                   | |  
| |__) |  ___ ______| |__) | __   __ _  __ _ _   _  __ _ _ __ | |_ 
|  ___/ |/ __|______|  ___/ '_ \ / _` |/ _` | | | |/ _` | '_ \| __|
| |   | | (__       | |   | | | | (_| | (_| | |_| | (_| | | | | |_ 
|_|   |_|\___|      |_|   |_| |_|\__, |\__, |\__,_|\__,_|_| |_|\__|
                                  __/ |   | |                      
                                 |___/    |_|     
"""
print(tag)
excludeDir = []
isNeedExclude = input("是否需要配置排除压缩文件夹(Y/N)：")
if isNeedExclude == "Y" or isNeedExclude == "y":
    excludeDirStr = input("请输入需要排除压缩的文件夹(多个以空格分隔)：")
    excludeDir = excludeDirStr.split(" ")
    print("当前配置的排除压缩文件夹为：")
    print(excludeDir)


# 创建压缩线程
def addThread(rootPath, compressFile, compressPath, extensionName):
    compressThread = CompressThread(rootPath, compressFile, compressPath, extensionName)
    compressThread.start()
    threads.append(compressThread)


if os.system("pngquant --version") != 0:
    print("\n未检测到pngquant命令行环境，请参照pngquant官网搭建命令行环境：https://pngquant.org/")
else:
    dirPath = input("请选择需要压缩的文件夹路径：")
    # 去除输入路径首位空格
    dirPath = dirPath.rstrip()
    dirPath = dirPath.lstrip()
    print(dirPath)
    # 初始化线程锁
    threadLock = threading.Lock()
    # 压缩线程数组
    threads = []
    # 开始历遍所有图片
    for root, dirs, files in os.walk(dirPath):
        # 当前路径下所有的图片加入压缩线程
        for childFile in files:
            # 文件名
            childFilePath = os.path.join(root, childFile)
            father_path = os.path.abspath(os.path.dirname(childFilePath) + os.path.sep + ".")
            father_name = os.path.basename(father_path)
            if father_name not in excludeDir:
                # 扩展名
                extension = os.path.splitext(childFilePath)[1][1:]
                if platform.system() != 'Windows':
                    if extension == 'png' or extension == 'jpg' or extension == 'jpeg':
                        addThread(root, childFile, childFilePath, extension)
                else:
                    # Windows版pngquant只支持png压缩
                    if extension == 'png':
                        addThread(root, childFile, childFilePath, extension)
    # 开始遍历执行压缩线程
    for thread in threads:
        thread.join()
