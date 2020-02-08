import re
import requests
import threading
import os.path
import logging
lock = threading.Lock()
logging.basicConfig(level=logging.INFO)

START = 6158
END = 6666
MAX_THREADS = 50
course_ids = range(START,END+1)
finished_ids = []
courses_list = []
base_URL = r"https://school.jledu.com/front/demand/play/"

def 凎(course_id):
    page_URL = base_URL + str(course_id) + "/"
    
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
    title = re.findall("<p class=\"title\">.*</p>",text)[0][17:][:-4]
    #GET SCHOOL
    school = re.findall("<p class=\"fsize14\">.*</p>",text)[0][19:][:-4]
    #if school != "吉林市第一中学":
    #   return
    #GET SUBJECT
    subject = re.findall("学科： (.*)<",text)[0]
    #GET TESCHER
    tescher = re.findall("主讲：(.*)<",text)[0]

    #CREATE DICT
    lock.acquire()
    courses_list.append([course_id,subject,school,tescher,title,mp4_URL])
    lock.release()
def 淦(a_list):
    #a method to stick the list
    rtn = str()
    for x in a_list:
        rtn += str(x)
        rtn += ","
    return rtn[:-1]
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
    th_pool = []
    for _ in range(MAX_THREADS):
        th_pool.append(threading.Thread(target=赣))
    for i in range(MAX_THREADS):
        th_pool[i].start()
    for i in range(MAX_THREADS):
        th_pool[i].join()
    print(f"\nI have  爬取了 {START} to {END}, tired but happy")
    courses_list = sorted(courses_list, key=lambda x:x[0])
    with open("3.csv", "w") as f:
        for c in courses_list:
            f.write(淦(c) + "\n")
