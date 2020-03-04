#!usr/bin/env python3

import sqlite3
import time

import src8 as src
import stdModel as mdl

START = 6158
END = 8000 #Only import JLYZ

# import data from database
data_base_filename = "data2.db"
conn = sqlite3.connect(data_base_filename)
sql = 'SELECT * FROM demand WHERE id BETWEEN ? AND ? AND school="吉林市第一中学"'
dat = conn.execute(sql,(START,END))
dat = [x for x in dat]

# gen list
courses_list = [mdl.CourseModel(raw[0],raw[1],raw[2],raw[3],raw[4],raw[5]) for raw in dat]
for x in range(len(courses_list)):
    if '文科' in courses_list[x].title:
        courses_list[x].subject += '文'
    elif '奥班' in courses_list[x].title:
        courses_list[x].subject += '奥'
    elif '理科奥' in courses_list[x].title:
        courses_list[x].subject += '奥'
    if '限时训练' in courses_list[x].title and courses_list[x].subject == '数学':
        courses_list[x].subject = '数学奥'
    elif courses_list[x].teacher == '崔泽颖':
        courses_list[x].subject = '物理奥'
courses_list = sorted(courses_list, key=lambda x:(x.grade,x.subject,x.id))
c2 = list() # 高二
c3 = list() # 高三
c1 = list() # 高一
c0 = list() # 未知
for c in courses_list:
    if c.grade == '高中三年级':
        c3.append(c)
    elif c.grade == '高中二年级':
        c2.append(c)
    elif c.grade == '高中一年级':
        c1.append(c)
    elif c.grade == '0':
        c0.append(c)
# gen markdown FILE
# 高三
src.make_a_md_file(c3,"D:\\Documents\\Programs\\blog\\content\\" + "san.md","高中网课列表3","高三")
# 高二
src.make_a_md_file(c2,"D:\\Documents\\Programs\\blog\\content\\" + "er.md","高中网课列表2","高二")
# 高一
src.make_a_md_file(c1,"D:\\Documents\\Programs\\blog\\content\\" + "yi.md","高中网课列表1","高一")
# 未知
src.make_a_md_file(c0,"D:\\Documents\\Programs\\blog\\content\\" + "wz.md","高中网课列表0","未知")

# update blog
src.update_blog("D:\\Documents\\Programs\\blog\\","D:\\Documents\\Programs\\gaomengkai.github.io\\")

print("F I N I S H E D")