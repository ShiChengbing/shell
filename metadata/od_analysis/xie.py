#!/usr/bin/python
import time
from datetime import *


start_time='20131008143000'

def format_time(start_time):
        global fmat_time
        y = start_time[0:4]
        m = start_time[4:6]
        d = start_time[6:8]
        H = start_time[8:10]
        M = start_time[10:12]
        S = start_time[12:]
        print y ,m ,d,H,M,S
        s='%s-%s-%s %s:%s:%s'%(y,m,d,H,M,S)
	print s
	fmat_time=datetime.strptime(s,"%Y-%m-%d %H:%M:%S")
        #now = date(int(y),int(m),int(d))
        #tm = time(int(H),int(M),int(S))
        #fmat_time= '%s %s'%(now,tm)
        print 'fmat',fmat_time
        return fmat_time
format_time(start_time)
