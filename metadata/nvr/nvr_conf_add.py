#!/usr/bin/python

import os,sys
import string
import MySQLdb


####   sql db connections
g_conn=''
g_cur=''


def connectDB():
    global g_conn
    global g_cur
    try:
        g_conn=MySQLdb.connect(host='10.110.0.52',user='labmysql',passwd='123456',port=3306)
        g_cur=g_conn.cursor()
        g_conn.select_db('MetaDataDB')
    except MySQLdb.Error, e:
        print 'Connecting to Metadata DB failed!'
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        sys.exit();


def closeDB():
    global g_conn
    global g_cur
    try:
        g_conn.commit()
        g_conn.close()
    except MySQLdb.Error, e:
        print 'Closing Metadata DB failed!'
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        sys.exit();
    except:
        print 'Unknown error happened in closeDB()'
        sys.exit()

def floor_id(floor,cam_name):
	F_site=floor.find('F')
	F_value=floor[0:F_site]
	C_site=cam_name.find('M')
	C_value=cam_name[C_site:]
	return F_value
	

def main():
	try:
		connectDB()
		f=sys.stdin
		while 1:
			line=f.readline()
			sys.stdout.flush()
			if not line:
				break
			line_value=string.strip(line)
			if len(line_value)>0:
				all_str_list=line_value.split(';')
				Nvr_IP=all_str_list[0]
				Brk_IP=all_str_list[1]
				#Channel=int(all_str_list[2])
				Channel=all_str_list[2]
				floor=all_str_list[3]
				cam_name=all_str_list[4]
				print floor,cam_name
				#floor_id(floor,cam_name)
				g_cur.execute("select Area_ID from  Info_Area_tbl where Area_name='%s';"%(floor))
				ar_rows=g_cur.fetchall()
				for ar_row in ar_rows:
					Area_ID=ar_row[0]
				new_F_value=str(Area_ID)+'%'
				sql = "select Cam_ID from  Cam_loc_tbl where Cam_ID like '%s' and Cam_name='%s';"%(new_F_value,cam_name)
				g_cur.execute(sql)
				camid_rows = g_cur.fetchall()
				for camid in camid_rows:
					Cam_ID=int(camid[0])
				print Cam_ID,Nvr_IP,Channel,Brk_IP
				g_cur.execute("insert into Rem_Rec (Cam_ID,Nvr_IP,Channel,Brk_IP) values('%d','%s','%s','%s');"%(Cam_ID,Nvr_IP,Channel,Brk_IP))
			else:
				continue
		closeDB()
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
		sys.exit()
	except:
	 	print "Unexpected error:", sys.exc_info()[0]
	
	
main()	
