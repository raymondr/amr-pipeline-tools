from os import listdir
from os.path import isfile, join
mypath = 'seq'
onlyfiles = [ f.split('.')[0] for f in listdir(mypath) if isfile(join(mypath,f)) ]

import subprocess
cluster_prog = "/s/bovine/e/nobackup/common/tools/cd-hit-v4.6.1-2012-08-27/cd-hit -i %s -o %s"
for id in onlyfiles:
    arg1 = "-i ../seq/%s.fa" % id
    arg2 = "-o ../cdhit/%s.out" % id
    subprocess.call([cluster_prog, arg1, arg2])
