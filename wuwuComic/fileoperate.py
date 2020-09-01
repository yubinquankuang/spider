"""
删除空白文件夹
"""
import os
import sys
path = "H:\python项目\spider-master\comic"

def delete_blank_dir(path):
    file_list = os.listdir(path)
    length = len(file_list)

    if length == 0:
        print(path)
        os.removedirs(path)
        return 1
    return 0


if __name__ == "__main__":
    dir_list = os.listdir(path)
    num = 0
    for dir in dir_list:
        subpath = os.path.join(path,dir)
        num += delete_blank_dir(subpath)
    print(num)