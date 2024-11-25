import os
import glob

dirsrc = "../games/labels/train"
dirdst = "../games/labels/test"

dstfiles = glob.glob(os.path.join(dirdst, "*.txt"))
srcfiles = glob.glob(os.path.join(dirsrc, "*.txt"))


def readlines(filepath):
    res = []
    for line in open(filepath).readlines():
        line = line.strip()
        if len(line) == 0:
            continue
        res.append(line)
    return res


for srcfile in srcfiles:
    dstfile = os.path.join(dirdst, os.path.basename(srcfile))
    lines = readlines(srcfile) + readlines(dstfile)    
    with open(dstfile, "w") as f:
        for line in lines:
            f.write(line + "\n")
