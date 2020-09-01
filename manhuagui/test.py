import re
import os
import sys
import time
import requests
import random
from name_list import NAME
from fileoperate import *

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


# 随机选择一个user_agent
user_agent_list = [
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
  'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
]
user_agent = random.choice(user_agent_list)

# 传递给header
headers = { 'User-Agent': user_agent }


def myRequests(url):
    """
    获取对应请求的URL
    设置对应的操作，在请求失败时确保重新发送
    params:
        url：请求地址
    """
    try:
        response = requests.get(url,headers=headers)
    except Exception as e:
        time.sleep(10)
        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            time.sleep(10)
            response = requests.get(url, headers=headers)
            sys.exit(1)
    return response


def get_chapter_url_list(url):
    """
    获取章节链接地址
    params:
        url：漫画目录地址
    return:
        name_list：章节地址列表
    """
    response = myRequests(url)
    html = response.text
    name_list = re.findall(r'/comic/7580/\d{4,11}.html', html)
    for i in range(0,len(name_list)):
        name_list[i] = "https://www.manhuagui.com" + name_list[i]
    time.sleep(1)
    return name_list


def create_comic_dir(dirname):
    """
    创建漫画文件夹
    params:
        dirname:文件夹名称
    return:
        dir_name:文件路径
    """
    path = os.path.dirname(__file__)
    comic_dir = os.path.join(path, "comic")
    dir_name = os.path.join(comic_dir, dirname)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    print(dir_name)
    return dir_name


def get_chapter_comic(chapter_url,pic_num,dir_name):
    """
    下载对应章节图片
    params:
        chapter_url:对应的章节链接
        pic_num:图片编号，本章图片的起始编号
    """
    time.sleep(1)
    response = myRequests(chapter_url)
    html = response.text
    name_list = re.findall(r'https://pic.muamh.com/static/upload/book/.{7,30}.jpg', html)
    while(len(name_list) == 0):
        response = myRequests(chapter_url)
        html = response.text
        name_list = re.findall(r'https://pic.muamh.com/static/upload/book/.{7,30}.jpg', html)
    print(name_list)
    for name in name_list:
        pic_num += 1
        num = "%04d.jpg"%pic_num
        filename = os.path.join(dir_name,num)
        download_comic_jpg(name,filename)
    return pic_num


def download_comic_jpg(comic_url, filename):
    """
    下载对应图片
    params:
        comic_url:漫画图片地址
        filename:存储图片的地址
    return:
    """
    response = myRequests(comic_url)
    print(filename)
    time.sleep(0.5)
    with open(filename,'wb') as f:
        f.write(response.content)


def start_download(chapter_url_list,dir_name,cstart=1,pstart=0):
    """
    下载对应章节列表的漫画
    params：
        chapter_url_list:章节链接
        dir_name:漫画文件夹地址
        cstart：起始章节，base=0
        pstart：当前漫画图片编号
    """
    current_chapter = cstart -1
    pic_start = pstart
    for name in chapter_url_list[cstart:]:
        current_chapter += 1
        print(name,"chapter",current_chapter)
        # pic_start = get_chapter_comic(name, pic_start,dir_name)

def run_exe(comic_dir,dir_url):
    dirName= create_comic_dir(comic_dir)
    chapter_list = get_chapter_url_list(dir_url)
    print(len(chapter_list),chapter_list)
    start_download(chapter_list,dirName,1,0)

def get_comic_list_by_page(page=1):
    """
    获取漫画名称列表
    """
    current_page = page
    name_set = set()
    url = ""
    for i in range(current_page,24):
        url = "https://www.5wmh.com/booklist?page={}&tag=%E5%89%A7%E6%83%85&area=-1&end=-1".format(i)
        print(url)
        response = myRequests(url)
        html = response.text
        name_list = re.findall('href="(https://www.5wmh.com/book/.{4,8}).html" title="(.{2,15})"', html)
        for name in name_list:
            if "<img" in name[1]:
                continue
            name_set.add(name)
    print(len(name_set))


if __name__ == "__main__":
    for name in NAME[0:]:
        dir_name = name[1]
        dir_name = dir_name.replace(":","")
        run_exe(dir_name,name[0])
        time.sleep(1)