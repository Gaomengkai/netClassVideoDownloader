import threading,re,requests,os.path,logging,src8,sqlite3

conn = sqlite3.connect("data2.db")

sql_1 = """
SELECT *
FROM demand
WHERE id BETWEEN 6158 AND 7500
AND school="吉林市第一中学"
AND subject="数学"
AND title LIKE "%文科%"
"""

sql_2 = 'UPDATE demand SET grade="高中二年级" WHERE title LIKE "%18级%" AND id BETWEEN 6158 AND 7500'
sql_3 = 'UPDATE demand SET grade="高中三年级" WHERE title LIKE "%二轮%" AND id BETWEEN 6158 AND 7500'

