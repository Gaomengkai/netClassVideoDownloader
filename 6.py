import re
import requests
import threading
import os
import os.path
import logging
import sys
锁 = threading.Lock()
logging.basicConfig(level=logging.INFO)
__author__ = "Gao Mengkai"

开始 = 6160
结束 = 6513
路径 = ""
课程们 = range(开始,结束+1)
已经完成 = []#int list
文综 = ["政治","地理","历史"]
def 玕(s):
    锁.acquire()
    print(s)
    锁.release()
基本网址 = r"https://school.jledu.com/front/demand/play/"

def 凎(课程代号:int):
    播放页网址 = 基本网址 + str(课程代号) + "/"
    
    #GET 视频网址 AND TITLE
    r = requests.get(播放页网址)
    if r.status_code != 200:
        return
    text = r.text
    try:
        视频网址 = re.findall("https.*mp4",text)[0]
    except:
        logging.debug(f"{课程代号}_Video file does not exist in this page.")
        return
    #GET SCHOOL
    school = re.findall("<p class=\"fsize14\">吉林市第一中学</p>",text)
    if school == []:
        return
    #GET TITLE
    标题 = re.findall("<p class=\"title\">(.*)</p>",text)[0]

    #GET SUBJECT
    科目 = re.findall("学科： (.*)<",text)[0]
    if 科目 in 文综:
        logging.debug(f"{课程代号}_{科目}————已经跳过下载")
        return
    #GENERATE HEADERS
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Referer': 播放页网址
    }

    #DOWNLOAD AND SAVE FILE
    #本地路径 = "F:\\test\\"
    本地路径 = "D:\\"
    if 路径 != "":
        本地路径 = 路径
    本地文件名称 = f"{科目}_{课程代号}_{标题}.mp4"
    if os.path.isfile(本地路径 + 本地文件名称):
        r1 = requests.head(视频网址,headers=headers)
        给定文件大小 = int(r1.headers['Content-Length'])
        if 给定文件大小 <= os.path.getsize(本地路径+本地文件名称)+10485760:
            玕(f"[EXIST]   {本地文件名称}")
            return
        玕(f"[WARNING] {本地文件名称}Exists but is not completed.")
        玕(f"[WARNING] Program will download it again.")
    锁.acquire()
    #print(f"{本地文件名称}_Downloading")
    锁.release()
    r = requests.get(视频网址,headers=headers,stream=True)
    #锁.acquire()
    玕(f"[DOWNLOAD]{本地文件名称}")
    with open(本地路径 + 本地文件名称, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    玕(f"[SAVED]   {本地文件名称}")
    #锁.release()
def 赣():
    while True:
        领到任务 = False
        for 当前任务 in 课程们:
            if 当前任务 not in 已经完成:
                锁.acquire()
                已经完成.append(当前任务)
                领到任务 = True
                锁.release()
                凎(当前任务)
                break
        if not 领到任务:
            break
if __name__ == '__main__':
    i = int(input("输入起始编号："))
    j = int(input("输入终止编号："))
    if i <= j:
        开始 = i;结束 = j
    else:
        开始 = j;结束 = i
    路径 = str(input(r"输入保存位置（如 D:\网课内容\）（若目录不存在将自动创建）:"))
    if not os.path.exists(路径):
        os.mkdir(路径)
    if 路径[-1] != "\\":
        路径 = 路径 + "\\"
    课程们 = range(开始,结束+1)
    线程池 = []
    for _ in range(3):
        线程池.append(threading.Thread(target=赣))
    for i in range(3):
        线程池[i].start()
    for i in range(3):
        线程池[i].join()
    玕(f"\nI have finished to download {开始} to {结束}, tired but happy")
    os.system("PAUSE")