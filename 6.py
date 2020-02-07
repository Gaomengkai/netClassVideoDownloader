import re
import requests
import threading
import os
import os.path
import logging
import sys
lock = threading.Lock()
logging.basicConfig(level=logging.INFO)

START = 6160
END = 6513
path1 = ""
course_ids = range(START,END+1)
finished_ids = []#int list
文综 = ["政治","地理","历史"]
def proprint(s):
    lock.acquire()
    print(s)
    lock.release()
base_URL = r"https://school.jledu.com/front/demand/play/"
listen_code = ""

def 凎(course_id:int):
    page_URL = base_URL + str(course_id) + "/" + listen_code + "/"
    
    #GET mp4_URL AND TITLE
    r = requests.get(page_URL)
    if r.status_code != 200:
        return
    text = r.text
    try:
        mp4_URL = re.findall("https.*mp4",text)[0]
    except:
        logging.debug(f"{course_id}_Video file does not exist in this page.")
        return
    #GET SCHOOL
    school = re.findall("<p class=\"fsize14\">吉林市第一中学</p>",text)
    if school == []:
        return
    #GET TITLE
    title = re.findall("<p class=\"title\">(.*)</p>",text)[0]

    #GET SUBJECT
    subject = re.findall("学科： (.*)<",text)[0]
    if subject in 文综:
        logging.debug(f"{course_id}_{subject}————已经跳过下载")
        return
    #GENERATE HEADERS
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Referer': page_URL
    }

    #DOWNLOAD AND SAVE FILE
    #local_path = "F:\\test\\"
    local_path = "D:\\"
    if path1 != "":
        local_path = path1
    local_file_name = f"{subject}_{course_id}_{title}.mp4"
    if os.path.isfile(local_path + local_file_name):
        r1 = requests.head(mp4_URL,headers=headers)
        len01 = int(r1.headers['Content-Length'])
        if len01 >= os.path.getsize(local_path+local_file_name)+10485760:
            proprint(f"[EXIST]   {local_file_name}")
            return
        proprint(f"[WARNING] {local_file_name}Exists but is not completed.")
        proprint(f"[WARNING] Program will download it again.")
    lock.acquire()
    #print(f"{local_file_name}_Downloading")
    lock.release()
    r = requests.get(mp4_URL,headers=headers,stream=True)
    #lock.acquire()
    proprint(f"[DOWNLOAD]{local_file_name}")
    with open(local_path + local_file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
    proprint(f"[SAVED]   {local_file_name}")
    #lock.release()
def 赣():
    while True:
        findone = False
        for current_id in course_ids:
            if current_id not in finished_ids:
                lock.acquire()
                finished_ids.append(current_id)
                findone = True
                lock.release()
                凎(current_id)
                break
        if not findone:
            break
if __name__ == '__main__':
    i = int(input("输入起始编号："))
    j = int(input("输入终止编号："))
    if i <= j:
        START = i;END = j
    else:
        START = j;END = i
    path1 = str(input(r"输入保存位置（如 D:\网课内容\）（若目录不存在将自动创建）:"))
    if not os.path.exists(path1):
        os.mkdir(path1)
    if path1[-1] != "\\":
        path1 = path1 + "\\"
    course_ids = range(START,END+1)
    th_pool = []
    for _ in range(3):
        th_pool.append(threading.Thread(target=赣))
    for i in range(3):
        th_pool[i].start()
    for i in range(3):
        th_pool[i].join()
    print(f"\nI have finished to download {START} to {END}, tired but happy")
    os.system("PAUSE")
