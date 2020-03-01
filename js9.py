import threading,re,sqlite3,time
import requests
import stdModel
import src8
url = r'https://school.jledu.com/front/demand/demand_list_one'
base_URL = r"https://school.jledu.com/front/demand/play/"
currentPage = 1
pageSize = 80
conn = sqlite3.connect("data2.db")
conn.execute("CREATE TABLE IF NOT EXISTS demand\
    (id INTEGER PRIMARY KEY,\
    subject TEXT,\
    grade TEXT,\
    title TEXT,\
    school TEXT,\
    teacher TEXT)")
while True:
    params = {
        'page.currentPage':currentPage,
        'page.pageSize':pageSize,
        'queryDemand.sort':0,
        'queryDemand.demandType':1
    }
    for _ in range(4):
        dat = requests.get(url, params=params)
        if dat.status_code == 200:
            break
        time.sleep(0.5)
    dat=dat.json()
    totalPageSize = int(dat['page']['totalPageSize'])
    currentPage += 1
    for x in dat['entity']:
        try:
            conn.execute("INSERT INTO demand VALUES(?,?,?,?,?,?)",\
                (int(x['id']),x['subjectName'],x['grade'],x['courseName'],x['schoolName'],x['teacher']['name']))
            print(x['id'],x['subjectName'],x['grade'],x['courseName'],x['schoolName'],x['teacher']['name'])
        except sqlite3.IntegrityError:
            pass
            #print("JMP")
    if currentPage == totalPageSize:
        break
alr_ext = []
for x in conn.execute('SELECT id from demand where id >6157'):
    alr_ext.append(x[0])
for i in range(6158,7800):
    if i not in alr_ext:
        c = src8.genCourseById(i)
        if c != None:
            if c.grade == '':
                c.grade = '0'
            conn.execute('INSERT INTO demand VALUES(?,?,?,?,?,?)',\
                (c.id,c.subject,c.grade,c.title,c.school,c.teacher))
            print(c.id,c.subject,c.grade,c.title,c.school,c.teacher)
conn.commit()
conn.close()
print("FINISHED%d"%len(alr_ext))