import os

if __name__ == '__main__':
    fs = list()
    for _,_,files in os.walk(os.getcwd()):
        fs = files
        break
    for f in fs:
        fn = f.split(".")[0]
        fe = f.split(".")[1]
        if fe == "ui":
            cmd = "pyuic5 -o {}.py {}.ui".format(fn,fn)
            os.system(cmd)
