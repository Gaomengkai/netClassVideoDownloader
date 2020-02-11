import sys
import re
import requests
import threading
import os.path
import logging
from PyQt5 import QtCore, QtGui, QtWidgets
#from Pyqt5.QtGui import QStandardItem,QStandardItemModel
import m
lock = threading.Lock()
logging.basicConfig(level=logging.INFO)
__author__ = "Gao Mengkai"
app = QtWidgets.QApplication(sys.argv[1:])
class sucker(m.Ui_MainWindow):
    def __init__(self,form):
        super().__init__()
        self._START = 0
        self._END = 0
        self._PATH = "D:\\netClass"
        self.setupUi(form)
        self.pushButton.clicked.connect(self.ganOnClick)
        self.base_URL = r"https://school.jledu.com/front/demand/play/"
        self.文综 = ["政治","地理","历史"]
    def ganOnClick(self):
        START = self.startNum.value()
        END = self.endNum.value()
        self._PATH = str(self.savePath.toPlainText())
        self.course_id_iter = iter(range(START,END+1))
        self.initialize()
        self.淦()
    def 凎(self,course_id:int,thread_id:int):
        page_URL = self.base_URL + str(course_id) + "/"
        
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
        if subject in self.文综:
            logging.debug(f"{course_id}_{subject}————已经跳过下载")
            return
        #GENERATE HEADERS
        headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Referer': page_URL
        }

        #DOWNLOAD AND SAVE FILE
        #local_path = "F:\\netClass\\"
        local_path = self._PATH
        local_file_name = f"{subject}_{course_id}_{title}.mp4"
        r1 = requests.head(mp4_URL,headers=headers)
        len01 = int(r1.headers['Content-Length'])
        if os.path.isfile(local_path + local_file_name):#if file already exists
            #To check if file is completed
            #Allow 10MB broken
            if len01 <= os.path.getsize(local_path+local_file_name)+10485760:
                logging.info(f"[EXIST]   {local_file_name}")
                return
            #Cannot return: Download it again
            logging.info(f"[WARNING] {local_file_name}Exists but is not completed.")
        lock.acquire()
        logging.info(f"[DOWNLOAD]{local_file_name}")
        lock.release()
        #r = requests.get(mp4_URL,headers=headers)
        r = requests.get(mp4_URL,headers=headers,stream=True)
        lock.acquire()
        logging.info(f"[SAVING]  {local_file_name}")
        #with open(local_path + local_file_name, 'wb') as f:
        #    f.write(r.content)
        size_downloaded = 0
        with open(local_path + local_file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    size_downloaded += 8192
                    self.data_refresh(thread_id,"{:.2}%{}".format(size_downloaded/len01,local_file_name))
                    f.write(chunk)
        lock.release()
        logging.info(f"[SAVED]   {local_file_name}")
    def initialize(self):
        self.info = ["","",""]
    def data_refresh(self,thread_id,string):
        self.info[thread_id] = string
        model = QtGui.QStandardItemModel()
        for _ in range(3):
            model.appendRow(QtGui.QStandardItem(string))
        self.listWidget.setModel(model)
    def 赣(self,thread_id:int):
        while True:
            try:
                course_id = next(self.course_id_iter)
                self.凎(course_id,thread_id)
            except StopIteration:
                return
    def 淦(self):
        threads=[]
        for i in range(3):
            threads.append(threading.Thread(target=self.赣,args=(i,)))
        for i in range(3):
            threads[i].start()

if __name__ == '__main__':
    form = QtWidgets.QMainWindow()
    w = sucker(form)
    form.show()
    sys.exit(app.exec_())
