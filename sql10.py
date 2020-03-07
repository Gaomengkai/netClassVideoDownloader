import threading,re,requests,os.path,logging,src8,sqlite3

conn = sqlite3.connect("data2.db")

sql_1 = """
SELECT teacher,grade
FROM demand
WHERE id BETWEEN 6158 AND 8000
AND school="吉林市第一中学"
"""
teacher_grade = set()
for x in conn.execute(sql_1).fetchall():
    teacher_grade.add(x)
teachers  = {x[0] for x in teacher_grade}
tea2 = [x[0] for x in teacher_grade]
for x in teachers:
    del tea2[tea2.index(x)]
print(tea2)
l3=list()
for x in teacher_grade:
    if x[0] in tea2:
        l3.append(x)
l3 = sorted(l3,key=lambda x:x[0])

print()
d1 = dict()
for t in tea2:
    d1[t] = []
    _tmp = ''
    p=-1
    for x in conn.execute("select * from demand where teacher=(?) and school='吉林市第一中学' and id between ? and ?",(t,6158,8000)):
        if x[2] != _tmp:
            p+=1
            if x[2] !='0':
                d1[t].append({x[2]:1})
            _tmp =x[2]
        else:
            if x[2] !='0':
                d1[t][p][x[2]]+=1
d2 = dict()
for x in d1.keys():
    d2[x]=[t for t in d1[x][0].keys()][0]
print(d2)
conn.close()
