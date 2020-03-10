import threading,re,requests,os.path,logging,src8,sqlite3

conn = sqlite3.connect("data2.db")
START = 6158;END=8000
se=(START,END)
sql_1 = """
SELECT teacher,grade
FROM demand
WHERE id BETWEEN ? AND ?
AND school="吉林市第一中学"
"""
teacher_grade = set()
for x in conn.execute(sql_1,se).fetchall():
    teacher_grade.add(x)
teachers  = {x[0] for x in teacher_grade}
tea2 = [x[0] for x in teacher_grade]
for x in teachers:
    del tea2[tea2.index(x)]
print(tea2)
# tea2: [teacher,]
l3=list()
for x in teacher_grade:
    if x[0] in tea2:
        l3.append(x)
l3 = sorted(l3,key=lambda x:x[0])
# l3: [(teacher,grade),]
print(l3)
bigDict = dict()
for teacher in tea2:
    bigDict[teacher] = {'exist':[]}
# Create bigDict to save ITEM like teacher:{grade:grade,}

# Get teacher and grade's number
# Creat total teacher and grade
total = []
for x in tea2:
    for y in conn.execute("select teacher,grade from demand where teacher=(?) and school='吉林市第一中学' and id between ? and ?",(x,START,END)):
        total.append(y)

for x in total:
    if x[1] not in bigDict[x[0]]['exist']:
        bigDict[x[0]]['exist'].append(x[1])
        bigDict[x[0]][x[1]] = 0
    bigDict[x[0]][x[1]] += 1


#遍历bigDict 查元素 有没有重的
for x in bigDict.keys():
    if len(bigDict[x]['exist']) > 2:
        raise Exception("多了，手动查一遍")

d3 = dict()
for x in bigDict.keys():
    for y in bigDict[x].keys():
        if (y != 'exist') and (type(y) is not list) and (y != '0'):
            d3[x] = y
print(d3)
infl = 0
for x in d3.keys():
    for y in conn.execute("select title from demand where grade='0' and teacher=(?) and school='吉林市第一中学' and id between ? and ?",(x,START,END)):
        print(f"INFLUENCE: {y[0]} -> {d3[x]}")
        infl += 1
print(f"TOTAL INFLUENCE: {infl}")
if input("Continue?\n") == 'y':
    for x in d3.keys():
        conn.execute("UPDATE demand SET grade=? WHERE teacher=?\
            and school='吉林市第一中学' and id between ? and ?",
            (d3[x],x,START,END))
    conn.commit()
conn.close()
