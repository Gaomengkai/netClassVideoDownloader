import requests

'''
6158-6184
吉林一中
'''
listen_code = ""
class_id = range(6158,6185)

url = 'https://1253868908.vod2.myqcloud.com/378170f1vodgzp1253868908/08b2f2755285890798174450095/jWUFtYZVI8sA.mp4'
refer = "https://school.jledu.com/front/demand/play/6176/"
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Referer': 'https://school.jledu.com/front/demand/play/6176/'
}
#r = requests.get(url)
r = requests.get(url, headers=headers)
local_file = "F:\video\1.mp4"
with open("F:\\1.mp4","wb") as f:
    f.write(r.content)
    