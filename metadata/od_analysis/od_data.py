#!/usr/bin/python


import os,sys
import string
import vaconf_db
import time
#from datetime import * 
import datetime





#incount_list=[]
#outcount_list=[]

def func_tbl(va_func):
	global func_tbl
	func_tbl='%s_result_tbl'%va_func
	#print 'func_tbl',func_tbl
	return func_tbl

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

def write_od(value):
        file_object = open('od_conf.txt', 'a')
        file_object.write(value)
        file_object.write('\n')
        file_object.close( )
def F10_dump_sum_time_line(func_tbl,begin_time,end_time,line_ID):
	vaconf_db.g_cur.execute("SELECT sum(incount),sum(outcount) FROM `%s` WHERE `begin_time` > '%s' AND `end_time` < '%s' AND `line_ID` = '%s';"%(func_tbl,begin_time,end_time,line_ID))	
	numrows=int(vaconf_db.g_cur.rowcount)
	for i in range(numrows):
		row=vaconf_db.g_cur.fetchone()
		incount_sum=row[0]
		outcount_sum=row[1]
	incount_list.append(incount_sum)
	outcount_list.append(outcount_sum)	
	print incount_sum
	print outcount_sum

def main(file_name):
	global incount_list
	global outcount_list
	global end_init
	try:
		vaconf_db.connectDB()
		func_tbl(va_func)
		incount_list = []
		outcount_list = []
		for i in open(file_name):
			line=string.strip(i)
			print line
			line_ID=line
			begin_time=str(format_time(start_time))
			#print 'begin_time',begin_time
			end_time=count_time(begin_time,interval_time)
			#print 'end_time',end_time
			end_stamp=unix_time(end_time)
			fini_time=format_time(finish_time)
			fini_stamp=unix_time(fini_time)
			while end_stamp <= fini_stamp:
				#print end_stamp,fini_stamp
				#print end_time,fini_time
				incount_sum=0
				outcount_sum=0
				F10_dump_sum_time_line(func_tbl,begin_time,end_time,line_ID)
				begin_time=str(count_time(begin_time,add_time))
				end_time=str(count_time(str(end_time),add_time))
				end_stamp=unix_time(end_time)
				print 'end_time>>>>>',end_time
			print incount_list
			print outcount_list
			for in_sum in incount_list:
				write_od(str(in_sum))
			for out_sum in outcount_list:
				write_od(str(out_sum))
			
			incount_list = []
			outcount_list = []
			
		vaconf_db.closeDB()


        except BaseException, e:
                print 'Unknown error (',str(e),') happened in od_analysis ! '
                return None	




if __name__ == "__main__":
        if len(sys.argv) < 7:
                print 'argument missing'
                print 'vaconf_add.py <input file>!'
                sys.exit()

        inputfile = ''

	va_func=sys.argv[1]
	start_time=sys.argv[2]
	finish_time = sys.argv[3]
	interval_time = sys.argv[4]
	add_time = sys.argv[5]
        inputfile = sys.argv[6]
        #print 'Input file is "', inputfile
        try:
                main(inputfile)
        except BaseException, e:
                print 'Unknown error (',str(e),') happened in entry!'
                sys.exit()
        pass

