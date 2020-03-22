import re
import requests
import threading
import os.path
import time
import logging
from queue import Queue
lock = threading.Lock()
logging.basicConfig(level=logging.INFO)
__author__ = "Gao Mengkai"

START = 7900
END = 8500
MAX_THREADS = 4

# get args
import sys
if len(sys.argv)>1:
    _p=1
    while True:
        if sys.argv[_p] == '-s' or sys.argv[_p].upper == '--START':
            _p += 1
            START = int(sys.argv[_p])
            _p += 1
        elif sys.argv[_p] == '-e' or sys.argv[_p].upper == '--END':
            _p += 1
            END = int(sys.argv[_p])
            _p += 1
        elif sys.argv[_p] == '-t' or sys.argv[_p] == '--threads':
            _p += 1
            MAX_THREADS = int(sys.argv[_p])
            _p += 1
        else:
            _p += 1
        if _p >= len(sys.argv):
            break
q = Queue()
course_ids = iter(range(START,END+1))
finished_ids = [] #int list
文综 = ["政治","地理","历史"]
def proprint(s):
    lock.acquire()
    print(s)
    lock.release()
base_URL = r"https://school.jledu.com/front/demand/play/"
listen_code = ""
def proinfo(s):
    lock.acquire()
    logging.info(s)
    lock.release()
def 凎(course_id:int):
    page_URL = base_URL + str(course_id) + "/"
    
    #GET mp4_URL 
    for _ in range(3):
        try:
            r= requests.get(page_URL)
            break
        except requests.ConnectionError:
            time.sleep(0.5)
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
    
    #GET SUBJECT
    subject = re.findall("学科： (.*)<",text)[0]
    if subject in 文综:
        logging.info(f"[SKIP]    {course_id} is {subject}")
        return

    #GET TITLE
    title = re.findall("<p class=\"title\">(.*)</p>",text)[0]
    if '18级' in title or '高二' in title or '文科' in title:
        logging.info(f"[SKIP]    {course_id} is '18级'")
        return
    
    #GENERATE HEADERS
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Referer': page_URL
    }

    #DOWNLOAD AND SAVE FILE
    local_path = f"F:\\netClass\\{subject}\\"
    local_file_name = f"{subject}_{course_id}_{title}.mp4"
    if os.path.isfile(local_path + local_file_name):#if file already exists
        #To check if file is completed
        r1 = requests.head(mp4_URL,headers=headers)
        len01 = int(r1.headers['Content-Length'])
        #Allow 10MB broken
        if len01 <= os.path.getsize(local_path+local_file_name)+10485760:
            logging.info(f"[EXIST]   {local_file_name}")
            return
        #Cannot return: Download it again
        logging.info(f"[WARNING] {local_file_name}: Exists but is not completed.")
    proinfo(f"[DOWNLOAD]{local_file_name}")
    r = requests.get(mp4_URL,headers=headers)
    q.put([local_path,local_file_name,r.content])
def 赣():
    global MAX_THREADS
    while True:
        try:
            current_id = next(course_ids)
            凎(current_id)
        except StopIteration:
            break
    proinfo("[THREAD]  DOWNLOADER {} EXIT".format(MAX_THREADS))
    MAX_THREADS -= 1
def save_file(local_path,local_file_name,data:bytes):
    proinfo(f"[SAVING]  {local_file_name}")
    with open(local_path + local_file_name, 'wb') as f:
        f.write(data)
    proinfo(f"[SAVED]   {local_file_name}")
def save_file_loop():
    while True:
        dat = q.get()
        if dat == 0:
            proinfo("[THREAD]  SAVER EXIT")
            return
        save_file(dat[0],dat[1],dat[2])
if __name__ == '__main__':
    th_pool = []
    downloader_thread = threading.Thread(target=save_file_loop,name='save_file_loop')
    downloader_thread.start()
    for _ in range(MAX_THREADS):
        th_pool.append(threading.Thread(target=赣))
    for i in range(MAX_THREADS):
        th_pool[i].start()
    for i in range(MAX_THREADS):
        th_pool[i].join()
    q.put(0)
    downloader_thread.join()
    print(f"\nI have finished to download {START} to {END}, tired but happy")
