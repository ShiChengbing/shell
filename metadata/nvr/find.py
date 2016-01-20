#!/usr/bin/python

import os

rootdir = "/apps_root/shichengbing/kewei/apps_root/metadata/nvr"
key = "nvr_rec_all.conf"
fileresult = []
dirresult = []
for root,dirs,files in os.walk(rootdir):
    fileresult.extend([fn for fn in files if fn.find(key) > 0])
    dirresult.extend([dn for dn in dirs if dn.find(key) > 0])
print fileresult
print dirresult

#if os.path.exists(r'/apps_root/shichengbing/kewei/apps_root/metadata/nvr/nvr_rec_all.conf'):
if os.path.exists(r'./nvr_rec_all.conf'):
	print 'yyyy'

