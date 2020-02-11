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
课程们 = iter(range(开始,结束+1))
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
    'Referer': "https://school.jledu.com/"
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
    r = requests.get(视频网址,headers=headers,stream=True)
    #锁.acquire()
    玕(f"[DOWNLOAD]{本地文件名称}")
    with open(本地路径 + 本地文件名称+".tmp", 'wb') as f:
        for chunk in r.iter_content(chunk_size=2048):
            if chunk:
                f.write(chunk)
    os.rename(本地路径 + 本地文件名称+".tmp",本地路径 + 本地文件名称)
    玕(f"[SAVED]   {本地文件名称}")
    #锁.release()
def 赣():
    while True:
        try:
            当前编号 = next(课程们)
            凎(当前编号)
        except StopIteration:
            return
if __name__ == '__main__':
    甲 = int(input("输入起始编号："))
    乙 = int(input("输入终止编号："))
    开始 = min([甲,乙])
    结束 = max([甲,乙])
    路径 = str(input(r"输入保存位置（如 D:\网课内容\）（若目录不存在将自动创建）:"))
    if not os.path.exists(路径):
        os.mkdir(路径)
    if 路径[-1] != "\\":
        路径 = 路径 + "\\"
    课程们 = range(开始,结束+1)
    线程池 = []
    for _ in range(3):
        线程池.append(threading.Thread(target=赣))
    for 甲 in range(3):
        线程池[甲].start()
    for 甲 in range(3):
        线程池[甲].join()
    玕(f"\nI have finished to download {开始} to {结束}, tired but happy")
    os.system("PAUSE")
