import os
import os.path

path = "F:\\netClass\\"
for x,y,files in os.walk(path):
    a=files
    break
for b in a:
    if b[0] == " ":
        if os.path.isfile(path+b[1:]):
            print(f"remove{b}")
            os.remove(path+b[1:])
        os.rename(path+b,path+b[1:])