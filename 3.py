import re
import requests
import threading
import os.path
import logging
lock = threading.Lock()
logging.basicConfig(level=logging.INFO)

START = 6500
END = 6666
course_ids = range(START,END+1)
finished_ids = []#int list
文综 = ["政治","地理","历史"]
def proprint(s):
    lock.acquire()
    print(s)
    lock.release()
class Course():
    def __init__(self,course_id:int):
        self.listen_code = "3KNOTl"
        self.base_URL = r"https://school.jledu.com/front/demand/play/"
        self.page_URL = ''
        self.page_data = ''
        self.mp4_URL = ''
        self.title = ''
        self.course_id = course_id

    def 凎(self):
        self.page_URL = self.base_URL + str(self.course_id) + "/" + self.listen_code + "/"
        
        #GET mp4_URL AND TITLE
        r = requests.get(self.page_URL)
        text = r.text
        try:
            self.mp4_URL = re.findall("https.*mp4",text)[0]
        except:
            logging.debug(f"{self.course_id}_Video file does not exist in this page.")
            return
        #GET SCHOOL
        school = re.findall("<p class=\"fsize14\">吉林市第一中学</p>",text)
        if school == []:
            return
        #GET TITLE
        self.title = re.findall("<p class=\"title\">.*</p>",text)[0][17:][:-4]

        #GET SUBJECT
        subject = re.findall("学科：.*<",text)[0][4:][:-1]
        if subject in 文综:
            logging.debug(f"{self.course_id}_{subject}————已经跳过下载")
            return
        #GENERATE HEADERS
        self.headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Referer': self.page_URL
        }

        #DOWNLOAD AND SAVE FILE
        local_path = "F:\\netClass\\"
        local_file_name = f"{subject}_{self.course_id}_{self.title}.mp4"
        if os.path.isfile(local_path + local_file_name):
            logging.debug(f"{self.course_id}_File already exists")
            return
        lock.acquire()
        logging.info(f"{local_file_name}_Downloading")
        lock.release()
        r = requests.get(self.mp4_URL,headers=self.headers)
        lock.acquire()
        logging.info(f"{local_file_name}_Saving")
        with open(local_path + local_file_name, 'wb') as f:
            f.write(r.content)
        lock.release()
def 赣():
    while True:
        findone = False
        for current_id in course_ids:
            if current_id not in finished_ids:
                lock.acquire()
                finished_ids.append(current_id)
                findone = True
                cour = Course(current_id)
                lock.release()
                cour.凎()
                break
        if not findone:
            break
if __name__ == '__main__':
    th_pool = []
    for _ in range(3):
        th_pool.append(threading.Thread(target=赣))
    for i in range(3):
        th_pool[i].start()
    for i in range(3):
        th_pool[i].join()
    print(f"\nI have finished to download {START} to {END}, tired but happy")
