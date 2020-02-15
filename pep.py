import re,requests,os
from lxml import etree
from html import unescape

base_URL = r"http://bp.pep.com.cn/jc/ptgzkcbzsyjks/"
headers = {
    'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}
def fuck(x):
    if type(x) == type([]):
        if len(x) == 0:
            return ''
        for i in x:
            print("for was called")
            fuck(i)
    if type(x) != type("string"):
        x = etree.tostring(x,encoding='utf-8').decode('utf-8')
        x = unescape(x)
    return x
def fuckfuck(x):
    print(fuck(x))
def pa():
    global base_URL
    r = requests.get(base_URL,headers=headers)
    text = r.content.decode('utf-8')
    tree = etree.HTML(text)
    '''
    x = tree.xpath('//li')[0]
    x = x.xpath('a[@title]')[0]
    fuckfuck(x.get('title'))
    y = tree.xpath("//li/a")

    '''
    for x in tree.xpath('//li'):
        string = unescape(etree.tostring(x).decode('utf-8'))
        title = re.findall('">(.*)</a></h6>',string)[0]
        pdf = re.findall('"(.*.pdf)"',string)[0]
        print(title,pdf)
        pdf = base_URL + pdf[2:]
        fdr = 'F:\\test\\'
        r1 = requests.get(pdf,headers=headers)
        with open(fdr+title+'.pdf', 'wb') as f:
            f.write(r1.content)
        #print(unescape(etree.tostring(x).decode('utf-8')))
        #break
    
if __name__ == '__main__':
    pa()