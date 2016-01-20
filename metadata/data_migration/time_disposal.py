#!/usr/bin/python
"time disposal"

import os,sys
import string
import time
import datetime


def format_time(start_time):
	global fmat_time
	y = start_time[0:4]
	m = start_time[4:6]
	d = start_time[6:8]
	H = start_time[8:10]
	M = start_time[10:12]
	S = start_time[12:]
        s='%s-%s-%s %s:%s:%s'%(y,m,d,H,M,S)
        fmat_time=datetime.datetime.strptime(s,"%Y-%m-%d %H:%M:%S")
        #print 'fmat',fmat_time
        return fmat_time

def count_time(t1,t2):
	#print '>>>t1,t2',t1,t2
	global T
	T=datetime.datetime.strptime(t1,'%Y-%m-%d %H:%M:%S')+datetime.timedelta(minutes=int(t2))
	#print 'T',T
	return T

def unix_time(str_time):
	global unix_times
	unix_times=time.mktime(time.strptime(str(str_time),'%Y-%m-%d %H:%M:%S'))
	return unix_times

def dump_line_time(start_time,finish_time,interval_time,add_time):
        global be_time_list
        global ed_time_list
        be_time_list=[]
        ed_time_list=[]
        begin_time=str(format_time(start_time))
        #print 'begin_time',begin_time
        end_time=str(count_time(begin_time,interval_time))
        #print 'end_time',end_time
        end_stamp=unix_time(end_time)
        fini_time=format_time(finish_time)
        fini_stamp=unix_time(fini_time)
        while end_stamp <= fini_stamp:
                be_time_list.append(begin_time)
                ed_time_list.append(end_time)
                begin_time=str(count_time(begin_time,add_time))
                end_time=str(count_time(str(end_time),add_time))
                end_stamp=unix_time(end_time)
                #print 'end_time>>>>>',end_time

def open_file():
	global file_object
	file_object = open('f10_line_list', 'a')
	
def write_od(value):
        file_object.write(value)
        file_object.write('\n')

def close_file():
        file_object.close( )


