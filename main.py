import os
import platform


# 开始压缩图片
def startCompress(root, compressFile, path, extension):
    print("\n压缩开始运行，压缩图片路径为：" + path)
    cmd = "pngquant 256 --quality=65-80 --skip-if-larger --force --ext .png " + path
    os.system(cmd)
    # 重命名后缀
    if extension == 'jpg' or extension == 'jpeg':
        os.remove(path)
        os.rename(os.path.join(root, compressFile + ".png"),
                  os.path.join(root, compressFile))
    print("\n压缩结束运行，压缩图片路径为：" + path)


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

if os.system("pngquant --version") != 0:
    print("\n未检测到pngquant命令行环境，请参照pngquant官网搭建命令行环境：https://pngquant.org/")
else:
    dirPath = input("请选择需要压缩的文件夹路径：")
    # 去除输入路径首位空格
    dirPath = dirPath.rstrip()
    dirPath = dirPath.lstrip()
    print(dirPath)
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
                        startCompress(root, childFile, childFilePath, extension)
                else:
                    # Windows版pngquant只支持png压缩
                    if extension == 'png':
                        startCompress(root, childFile, childFilePath, extension)
