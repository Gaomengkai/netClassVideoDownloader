import re
import requests
import threading
import os.path
import logging

import stdModel
lock = threading.Lock()
logging.basicConfig(level=logging.INFO)

START = 6158
END = 6800
MAX_THREADS = 30
course_ids = iter(range(START,END+1))
courses_list = []
#base_URL = r"https://school.jledu.com/front/demand/play/"
gaosan = list()

def init_3():
    global gaosan
    url = r'https://school.jledu.com/front/demand/demand_list_one?page.currentPage=1&page.pageSize=512&queryDemand.subjectId=&queryDemand.showStatus=0&queryDemand.headStatus=&queryDemand.sort=2&queryDemand.courseName=&queryDemand.loginType=1&queryDemand.demandType=1&queryDemand.subject='
    r = requests.get(url)
    js = r.json()
    entity = js['entity']
    cs = sorted(entity,key=lambda x:x['id'])
    gaosan = list(map(lambda x:int(x['id']),cs))
def genPageURLById(id):
    return r"https://school.jledu.com/front/demand/play/" + str(id)
def getPageTextById(id):
    base_URL = r"https://school.jledu.com/front/demand/play/"
    page_URL = base_URL + str(id) + "/"
    r = requests.get(page_URL)
    if r.status_code != 200:
        return
    return r.text
def getMP4ByCourseId(course_id)->str:
    text = getPageTextById(course_id)
    try:
        mp4_URL = re.findall("https.*mp4",text)[0]
    except:
        logging.debug(f"{course_id}_Video file does not exist in this page.")
        return False
    return mp4_URL
def getMP4ByText(text):
    try:
        mp4_URL = re.findall("https.*mp4",text)[0]
    except:
        logging.debug(f"Video file does not exist in this page.")
        return False
    return mp4_URL
def genCourseById(course_id,hasGrade=False):
    text = getPageTextById(course_id)
    mp4_URL = getMP4ByText(text)
    if not mp4_URL:
        return
    title = re.findall("<p class=\"title\">.*</p>",text)[0][17:][:-4]
    school = re.findall("<p class=\"fsize14\">.*</p>",text)[0][19:][:-4]
    if (school != "吉林市第一中学") and (school != "吉林市第一中学校"):
       return
    subject = re.findall("学科： (.*)<",text)[0]
    try:
        teacher = re.findall('<p class="fsize16">(.*)</p>',text)[0]
        #teacher = re.findall("主讲：(.*)<",text)[0]
    except IndexError:
        teacher = re.findall(r"主讲教师：(.*)</span><span",text)[0]

    if hasGrade:
        grade = "高中三年级" if id in gaosan else "高中二年级"
    else:
        grade = ""
    
    c=stdModel.CourseModel(course_id,subject,grade,title,school,teacher)
    c.add_plus_item(mp4_URL=mp4_URL)
    return c
def genDictByIdAndText(text,id,hasGrade=False):
    mp4_URL = getMP4ByText(text)
    if not mp4_URL:
        return
    title = re.findall("<p class=\"title\">.*</p>",text)[0][17:][:-4]
    school = re.findall("<p class=\"fsize14\">.*</p>",text)[0][19:][:-4]
    if (school != "吉林市第一中学") and (school != "吉林市第一中学校"):
       return
    subject = re.findall("学科： (.*)<",text)[0]
    try:
        teacher = re.findall("主讲：(.*)<",text)[0]
    except IndexError:
        teacher = re.findall("主讲教师：(.*)<",text)[0]

    if hasGrade:
        grade = "高三" if id in gaosan else "高二"
    
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
    dictionary['id'] = id
    dictionary['title'] = title
    dictionary['subject'] = subject
    dictionary['school'] = school
    dictionary['URL'] = genPageURLById(id)
    dictionary['mp4_URL'] = mp4_URL
    if hasGrade:
        dictionary['grade'] = grade
    return dictionary
def 凎(course_id):
    global courses_list
    text = getPageTextById(course_id)
    dictionary = genDictByIdAndText(text,course_id)
    courses_list.append(dictionary)
def 淦(a_dict):
    #a method to stick the list
    rtn = str()
    data_needed = ['id','subject','teacher','title','URL']
    for key in data_needed:
        rtn += str(a_dict[key])
        rtn += ","
    return rtn[:-1]
def 网页淦(a_dict):
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
def genStrByCourse(course,mode) -> str:
    '''
    :param course: stdModel.Course class
    :param mode: 'md' or 'html'
    :return: str()
    '''
    if mode == 'md':
        rtn = str()
        rtn = f'{course.subject}-{course.teacher}-\
            [{course.title}]({genPageURLById(course.id)} "{course.id}_{course.title}")'
        rtn += '\n\n'
        return rtn
    elif mode == 'html':
        rtn = f'{course.subject}-{course.teacher}-\
            <a href="{genPageURLById(course.id)}" target="_blank">{course.title}</a>'
        return rtn
    else:
        raise Exception("Param Error on mode(str)")
def make_a_md_file(courses_list,filename,title='netClass Video List',category='netClass',grade=3):
    '''
    :param courses_list: [stdModel.Course(),]
    :param filename: str
    :param category: Default:'netClass'
    :param grade: Default: 3
    :return: None
    '''
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
            f.write("title: %s\n"%title)
        elif grade == 2:
            f.write("title: netClass Video List for GRADE 2\n")
        else:
            raise Exception("GRADE ERROR or DOES NOT SUPPORT")
        import time
        localtime = time.asctime( time.localtime(time.time()) )
        f.write("date: " + localtime + "\n")
        f.write("category: %s"%category + "\n\n")
        f.write("### 说明：其他年级请到上边的选项条找，找不着的可能在未知\n\n")
        f.write("#### Updated at {}\n\n".format(localtime))
        f.write("#### 最近更新： {}\n\n".format(localtime))
        for c in courses_list:
            if c.subject not in temp_subj:
                f.write(f"# {c.subject}\n\n")
                temp_subj.append(c.subject)
            f.write(genStrByCourse(c,'md'))
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
    #make_a_md_file(courses_list,"D:\\Documents\\Programs\\blog\\content\\" + "courses_list.md")
    #update_blog("D:\\Documents\\Programs\\blog\\","D:\\Documents\\Programs\\gaomengkai.github.io\\")
    print("\nLAST ONE:{}".format(sorted(courses_list,key=lambda x:x['id'])[-1]))
    