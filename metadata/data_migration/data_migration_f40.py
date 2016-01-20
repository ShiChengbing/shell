#!/usr/bin/python


import os,sys
import string
import active_db
import time
import datetime
import history_db
import config_db
import time_disposal

def F40_dump_sum_time_line(begin_time,end_time,line_ID):
	global F40_values
	F40_values=[]
	sql="SELECT Cam_ID,sum(peoplecount) FROM `F40_result_tbl` WHERE `begin_time` > '%s' AND `end_time` < '%s' AND `line_ID` = '%s';"%(begin_time,end_time,line_ID)
	active_db.a_cur.execute(sql)
	row=active_db.a_cur.fetchone()
	if row[0] == None:
		return F40_values
	else:
		peoplecount_sum=row[0]
		F40_values.append(row[0])
		F40_values.append(begin_time)
		F40_values.append(end_time)
		F40_values.append(line_ID)
		F40_values.append(row[1])
		F40_values.append(time.strftime('%Y%m%d%H%M%S'))
		return F40_values

def get_line_list():
        global line_list
        line_list=[]
        sql="select Line_ID from F40_line_tbl group by Line_ID order by Line_ID;"
        config_db.c_cur.execute(sql)
        numrows=int(config_db.c_cur.rowcount)
        for i in range(numrows):
                row=config_db.c_cur.fetchone()
                line_list.append(row[0])
        return line_list		

def main():
	global lines_list
	try:
		config_db.connectCDB()
		lines_list=get_line_list()
		#print lines_list
		config_db.closeCDB()

		time_disposal.dump_line_time(start_time,finish_time,interval_time,add_time)
		time_list=zip(time_disposal.be_time_list,time_disposal.ed_time_list)
		
		active_db.connectADB()
		history_db.connectHDB()

		for now_time in time_list:
			begin_time=now_time[0]
			end_time=now_time[1]
			for line_ID in lines_list:
				#print line_ID
				F40_dump_sum_time_line(begin_time,end_time,line_ID)
				print F40_values
				if len(F40_values) < 6:
					continue
				else:
					history_db.h_cur.execute("insert into F40_result_tbl values(%s,%s,%s,%s,%s,%s)",F40_values)
				history_db.h_conn.commit()
		history_db.closeHDB()
		
		active_db.closeADB()


        except BaseException, e:
                print 'Unknown error (',str(e),') happened in data_migration_f40 main() ! '
                return None	


if __name__ == "__main__":
        if len(sys.argv) < 5:
                print 'argument missing'
		print 'argument layout: 20131015130000 20131015140000 30 5'
                sys.exit()
	
	start_time=sys.argv[1]
	finish_time = sys.argv[2]
	interval_time = sys.argv[3]
	add_time = sys.argv[4]
        try:
                main()
        except BaseException, e:
                print 'Unknown error (',str(e),') happened in entry!'
                sys.exit()

