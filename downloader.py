import re,requests,os
from lxml import etree
from html import unescape

base_URL = r"https://www.yixuela.com/books/wuli/rjb/rjbgzwlbx1/"
headers = {
    'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}
s=2624;e=2690
CNT = 0
for i in range(s,e):
    url = "".join([base_URL,str(i),".html"])
    r=requests.get(url,headers=headers)
    text = r.content.decode('utf-8')
    tree = etree.HTML(text)
    xpath = '/html/body/section/div[2]/div[1]/div[2]'
    for x in tree.xpath(xpath):
        string = unescape(etree.tostring(x).decode('utf-8'))
        jpgs = re.findall('http.*.jpg', string)
        for jpg in jpgs:
            CNT += 1
            with open("F:\\temp\\keben\\{}.jpg".format(CNT),"wb") as f:
                r = requests.get(jpg,headers=headers)
                f.write(r.content)
                print(f'SAVED: {CNT}.jpg')