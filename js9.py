import threading
import sqlite3
import time
from queue import Queue

import requests
import stdModel

import src8

START = 6158;END = 8000
PROCESS_COUNT = 0
# Mode[1]: only javascript
# Mode[2]: only HTML
# Mode[1,2]: both HTML and javascript
Mode = [2,1]

# Initialize Web Request Params and Solid Data
url = r'https://school.jledu.com/front/demand/demand_list_one'
currentPage = 1
pageSize = 20

# Connect to Database
conn = sqlite3.connect("data2.db")
conn.execute("CREATE TABLE IF NOT EXISTS demand\
    (id INTEGER PRIMARY KEY,\
    subject TEXT,\
    grade TEXT,\
    title TEXT,\
    school TEXT,\
    teacher TEXT)")

# Mode 2 Use HTML       
alr_ext = []
if 2 in Mode:
    not_ext = []
    print("Running@Mode2")
    for x in conn.execute('SELECT id from demand where id >6157'):
        alr_ext.append(x[0])
    for i in range(START,END+1):
        if i not in alr_ext:
            not_ext.append(i)
    not_ext = iter(not_ext)
    q = Queue()
    def get_c():
        global PROCESS_COUNT
        while True:
            try:
                c = src8.genCourseById(next(not_ext))
                if c != None:
                    if c.grade == '':
                        c.grade = '0'
                    PROCESS_COUNT += 1
                    q.put(c)
            except StopIteration:
                q.put(None)
                return
    _max_threads = 4
    _threads = []
    for _ in range(_max_threads):
        _threads.append(threading.Thread(target=get_c))
    for i in range(_max_threads):
        _threads[i].start()
    tihs = _max_threads
    while True:
        if tihs == 0:
            break
        c = q.get()
        if c is None:
            tihs -= 1
            continue
        conn.execute('INSERT INTO demand VALUES(?,?,?,?,?,?)',\
                    c.generate_std_tuple())
        print("INSERT",c)

# Mode 1 Use javascript
if 1 in Mode:
    print("Running@Mode1")
    totalPageSize = None
    while True:
        params = {
            'page.currentPage':currentPage,
            'page.pageSize':pageSize,
            'queryDemand.sort':2,
            'queryDemand.demandType':1
        }
        for _ in range(4):
            dat = requests.get(url, params=params)
            if dat.status_code == 200:
                break
            time.sleep(0.5)
        dat=dat.json()
        if totalPageSize is None:
            totalPageSize = int(dat['page']['totalPageSize'])
        currentPage += 1
        for x in dat['entity']:
            c = stdModel.CourseModel(int(x['id']),x['subjectName'],x['grade'],x['courseName'],x['schoolName'],x['teacher']['name'])
            # search id in db AND grade=='0'?
            found_items = conn.execute("SELECT * FROM demand WHERE id=?",(c.id,)).fetchall()
            if found_items == []:
                print("INSERT",c)
                PROCESS_COUNT += 1
                conn.execute("INSERT INTO demand VALUES(?,?,?,?,?,?)",c.generate_std_tuple())
            elif found_items[0][2] == '0':
                print("UPDATE",c)
                PROCESS_COUNT += 1
                conn.execute("UPDATE demand SET grade=? WHERE id=?",(c.grade,c.id))
            else:
                pass
        if currentPage >= totalPageSize:
            break
conn.commit()
conn.close()
print("FINISHED %d"%PROCESS_COUNT)