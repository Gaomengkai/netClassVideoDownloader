fd = 'F:\\netClass\\'
科目 = ['语文','数学','英语','物理','化学','生物']
import os
import shutil

for _,_,files in os.walk(fd):
    a=files
    break
for b in a:
    c=b.split('_')[0]
    shutil.move(''.join([fd,b]),''.join([fd,c,'\\',b]))