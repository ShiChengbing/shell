#!/usr/bin/python


import os,sys
import string
import vaconf_db
import time
import datetime

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

def open_file():
	global file_object
	file_object = open('f40_od_conf.txt', 'a')
	
def write_od(value):
        file_object.write(value)
        file_object.write('\n')

def close_file():
        file_object.close( )

def F40_dump_sum_time_line(begin_time,end_time,line_ID):
	vaconf_db.g_cur.execute("SELECT sum(peoplecount) FROM `F40_result_tbl` WHERE `begin_time` > '%s' AND `end_time` < '%s' AND `line_ID` = '%s';"%(begin_time,end_time,line_ID))
	row=vaconf_db.g_cur.fetchone()
	peoplecount_sum=row[0]
	peoplecount_list.append(peoplecount_sum)
	#print peoplecount_sum

def F40_dump_line_time(start_time,finish_time,interval_time,add_time):	
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

def main(file_name):
	global lines_list
	global peoplecount_list
	try:
		vaconf_db.connectDB()
		lines_list=[]
		for i in open(file_name):
			line=string.strip(i)
			lines_list.append(line)
			line_ID=line
		#print lines_list

		F40_dump_line_time(start_time,finish_time,interval_time,add_time)
		
		open_file()
		for line_ID in lines_list:
			print line_ID

			peoplecount_list = []
			for site in range(0,len(be_time_list)):
				begin_time=be_time_list[site]
				end_time=ed_time_list[site]
				F40_dump_sum_time_line(begin_time,end_time,line_ID)
			#print peoplecount_list

			for peoplecount in peoplecount_list:
				#print peoplecount
				write_od(str(peoplecount))
			peoplecount_list = []

		close_file()
		vaconf_db.closeDB()


        except BaseException, e:
                print 'Unknown error (',str(e),') happened in od_analysis ! '
                return None	


if __name__ == "__main__":
        if len(sys.argv) < 6:
                print 'argument missing'
                print 'vaconf_add.py <input file>!'
		print 'argument layout: 20131008143000 20131008153000 30 5 f40_line_list'
                sys.exit()

        inputfile = ''
	
	#va_func=sys.argv[1]
	start_time=sys.argv[1]
	finish_time = sys.argv[2]
	interval_time = sys.argv[3]
	add_time = sys.argv[4]
        inputfile = sys.argv[5]
        #print 'Input file is "', inputfile
        try:
                main(inputfile)
        except BaseException, e:
                print 'Unknown error (',str(e),') happened in entry!'
                sys.exit()

