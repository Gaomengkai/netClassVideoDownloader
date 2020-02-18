url = r'https://school.jledu.com/front/demand/demand_list_one?page.currentPage=1&page.pageSize=512&queryDemand.subjectId=&queryDemand.showStatus=0&queryDemand.headStatus=&queryDemand.sort=2&queryDemand.courseName=&queryDemand.loginType=1&queryDemand.demandType=1&queryDemand.subject='
import requests
r = requests.get(url)
js = r.json()
entity = js['entity']
'''
for x in entity:
    print(x['id'],x['courseName'],x['grade'])
'''
cs = sorted(entity,key=lambda x:x['id'])
for x in cs:
    print(x['id'],x['courseName'])
print("len:" + str(len(entity)))