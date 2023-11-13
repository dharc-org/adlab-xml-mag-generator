#-*- coding: utf-8 -*-

# mag-subdirs.py
# v0.1

import datetime
import exifread
import hashlib
import json
import pathlib
import subprocess
import sys
import os

# check arguments
if len(sys.argv) < 5:
    print("No parameter has been included")
    print(" 1) script path dharc-xml-mag-generator.py")
    print(" 2) path of json formatted config file i.e. config.json")
    print(" 3) path of images directories subdirs/images")
    print(" 4) an extension i.e. .tif")
    print("i.e. $ python3 mag-subdirs.py /dir/script/adlab-xml-mag-generator.py config.json .tif")
    sys.exit()

# get var from arguments
script = sys.argv[1]
config = sys.argv[2]
path = sys.argv[3]
ext = sys.argv[4]

# list the first sub dirs
dirs = []
dirs = next(os.walk(path))[1]
dirs.sort()

for f in dirs:
    dirpath = pathlib.Path(path) / f
    print("python3 "+str(script)+" "+config+" "+str(dirpath)+" "+ext)

    p = subprocess.Popen(['python3',str(script),config,str(dirpath),ext], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
#p = subprocess.Popen(['ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    output = p.stdout.read()
    #print(output.decode("utf-8"))
    error = p.stderr.read()
    print(error.decode("utf-8"))

    filename=dirpath / os.path.basename(dirpath)
    f = open(str(filename)+".mag.xml", "w+")
    f.write(output.decode("utf-8"))
    f.close()
