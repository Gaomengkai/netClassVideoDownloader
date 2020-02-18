import re
import requests
import threading
import os.path
import logging
lock = threading.Lock()
logging.basicConfig(level=logging.INFO)
__author__ = "Gao Mengkai"

START = 6600
END = 6700
course_ids = iter(range(START,END+1))
#course_ids = iter([6211])
finished_ids = []#int list
文综 = ["政治","地理","历史"]
def proprint(s):
    lock.acquire()
    print(s)
    lock.release()
base_URL = r"https://school.jledu.com/front/demand/play/"
listen_code = ""

def 凎(course_id:int):
    page_URL = base_URL + str(course_id) + "/"
    
    #GET mp4_URL 
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
    
    #GET SUBJECT
    subject = re.findall("学科： (.*)<",text)[0]
    if subject in 文综:
        logging.info(f"[SKIP]    {course_id} is {subject}")
        return

    #GET TITLE
    title = re.findall("<p class=\"title\">(.*)</p>",text)[0]
    if '18级' in title or '高二' in title:
        logging.info(f"[SKIP]    {course_id} is '18级'")
        return
    #GENERATE HEADERS
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Referer': page_URL
    }

    #DOWNLOAD AND SAVE FILE
    local_path = "F:\\netClass\\"
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
    lock.acquire()
    logging.info(f"[DOWNLOAD]{local_file_name}")
    lock.release()
    r = requests.get(mp4_URL,headers=headers)
    lock.acquire()
    logging.info(f"[SAVING]  {local_file_name}")
    with open(local_path + local_file_name, 'wb') as f:
        f.write(r.content)
    lock.release()
    logging.info(f"[SAVED]   {local_file_name}")
def 赣():
    while True:
        try:
            current_id = next(course_ids)
            凎(current_id)
        except StopIteration:
            return
if __name__ == '__main__':
    th_pool = []
    for _ in range(3):
        th_pool.append(threading.Thread(target=赣))
    for i in range(3):
        th_pool[i].start()
    for i in range(3):
        th_pool[i].join()
    print(f"\nI have finished to download {START} to {END}, tired but happy")
