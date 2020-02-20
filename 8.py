import re
import requests
import threading
import os.path
import logging
lock = threading.Lock()
logging.basicConfig(level=logging.INFO)

START = 6158
END = 6800
MAX_THREADS = 30
course_ids = iter(range(START,END+1))
courses_list = []
base_URL = r"https://school.jledu.com/front/demand/play/"
gaosan = list()
def init_3():
    global gaosan
    url = r'https://school.jledu.com/front/demand/demand_list_one?page.currentPage=1&page.pageSize=512&queryDemand.subjectId=&queryDemand.showStatus=0&queryDemand.headStatus=&queryDemand.sort=2&queryDemand.courseName=&queryDemand.loginType=1&queryDemand.demandType=1&queryDemand.subject='
    r = requests.get(url)
    js = r.json()
    entity = js['entity']
    cs = sorted(entity,key=lambda x:x['id'])
    gaosan = list(map(lambda x:int(x['id']),cs))

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
    if (school != "吉林市第一中学") and (school != "吉林市第一中学校"):
       return
    #GET SUBJECT
    subject = re.findall("学科： (.*)<",text)[0]
    #GET TESCHER
    try:
        teacher = re.findall("主讲：(.*)<",text)[0]
    except IndexError:
        teacher = re.findall("主讲教师：(.*)<",text)[0]

    #GET GRADE
    #grade = "高三" if course_id in gaosan else "高二"
    
    #CREATE DICT
    dictionary = dict()
    if teacher in ['鄂春雨','刘波']:
        subject = "数学奥"
    if teacher == '王珊' or (subject == '数学' and '文科' in title):
        subject = "数学文"
    if teacher == '崔泽颖':
        subject = "物理奥"
    if teacher in ['梁红梅','林亚楠']:
        subject = "化学奥"
    dictionary['teacher'] = teacher
    #dictionary['grade'] = grade
    dictionary['id'] = course_id
    dictionary['title'] = title
    dictionary['subject'] = subject
    dictionary['school'] = school
    dictionary['URL'] = page_URL
    dictionary['mp4_URL'] = mp4_URL
    lock.acquire()
    courses_list.append(dictionary)
    lock.release()
def 淦(a_dict):
    #a method to stick the list
    rtn = str()
    data_needed = ['id','subject','teacher','title','URL']
    for key in data_needed:
        rtn += str(a_dict[key])
        rtn += ","
    return rtn[:-1]
def 网页淦(a_dict):
    rtn = str()
    #化学-王守来-<a href="http://baidu.com" target="_blank">课程</a>
    rtn = f"{a_dict['subject']}-{a_dict['teacher']}-<a href=\"{a_dict['URL']}\" target=\"_blank\">{a_dict['title']}</a>"
    return rtn
def md凎(a):
    rtn = str()
    rtn = f"{a['subject']}-{a['teacher']}-[{a['title']}]({a['URL']} \"{a['id']}_{a['title']}\")"
    rtn += "\n\n"
    return rtn

def 赣():
    while True:
        try:
            current_id = next(course_ids)
            凎(current_id)
        except StopIteration:
            return
def make_a_md_file(courses_list,filename,grade=3):
    def _grade_sucker(cl:list,gd:int):
        res = list()
        for c in cl:
            if (c['grade'] == '高三' and gd == 3) or (c['grade'] == '高二' and gd == 2):
                res.append(c)
        if res == []:
            raise Exception("res empty!")
        return res
    temp_subj = list()
    #courses_list = _grade_sucker(courses_list,grade)
    with open(filename,"w",encoding="utf-8") as f:
        if grade == 3:
            f.write("title: netClass Video List\n")
        elif grade == 2:
            f.write("title: netClass Video List for GRADE 2\n")
        else:
            raise Exception("GRADE ERROR or DOES NOT SUPPORT")
        import time
        localtime = time.asctime( time.localtime(time.time()) )
        f.write("date: " + localtime + "\n")
        f.write("category: netClass" + "\n\n")
        #f.write("# netClass List\n\n")
        f.write("# 网课列表（含高二和高三）\n\n")
        f.write("#### 使用脚本从{}获取\n\n".format(base_URL))
        f.write("#### Updated at {}\n\n".format(localtime))
        f.write("#### 最近更新： {}\n\n".format(localtime))
        for c in courses_list:
            if c['subject'] not in temp_subj:
                f.write(f"# {c['subject']}\n\n")
                temp_subj.append(c['subject'])
            f.write(md凎(c))
def update_blog(blog_root:str, web_root:str):
    os.system("7.cmd")

if __name__ == '__main__':
    #init_3()
    th_pool = []
    for _ in range(MAX_THREADS):
        th_pool.append(threading.Thread(target=赣))
    for i in range(MAX_THREADS):
        th_pool[i].start()
    for i in range(MAX_THREADS):
        th_pool[i].join()
    print(f"\nI have  爬取了 {START} to {END}, tired but happy")
    courses_list = sorted(courses_list, key=lambda x:(x['subject'],x['id']))
    #courses_list = sorted(courses_list, key=lambda x:(x['grade'],x['subject'],x['id']))
    with open("3.csv", "w") as f:
        import time
        localtime = time.asctime( time.localtime(time.time()) )
        f.write(localtime+"\n")
        for c in courses_list:
            f.write(淦(c) + "\n")
    with open("D:\\Documents\\Programs\\gaomengkai.github.io\\4.html","w",encoding="utf-8") as f:
        import time
        localtime = time.asctime( time.localtime(time.time()) )
        f.write("<!DOCTYPE HTML>")
        f.write("<html><head><meta charset=\"utf-8\"><title>Powered by GMK</title></head><body>")
        f.write("Updated: "+localtime+"<br>")
        for c in courses_list:
            f.write(网页淦(c) + "<br>")
        f.write("</body></html>")
    #make_a_md_file(courses_list,"D:\\Documents\\Programs\\blog\\content\\" + "courses_list2.md",2)
    make_a_md_file(courses_list,"D:\\Documents\\Programs\\blog\\content\\" + "courses_list.md")
    update_blog("D:\\Documents\\Programs\\blog\\","D:\\Documents\\Programs\\gaomengkai.github.io\\")
    print("\nLAST ONE:{}".format(sorted(courses_list,key=lambda x:x['id'])[-1]))
    