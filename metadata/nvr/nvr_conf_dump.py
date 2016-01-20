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

def write_nvr_all_conf(value):
        file_object = open('./nvr_rec_all.conf', 'a')
        file_object.write(value)
        file_object.write('\n')
        file_object.close( )

def write_nvr_work_conf(value1):
        file_object = open('./nvr_rec_work.conf', 'a')
        file_object.write(value1)
        file_object.write('\n')
        file_object.close( )

def main():
	try:
		if os.path.exists(r'./nvr_rec_all.conf'):
			os.remove("nvr_rec_all.conf")
		if os.path.exists(r'./nvr_rec_work.conf'):
			os.remove("nvr_rec_work.conf")
		connectDB()
		floor=sys.argv[1]
		g_cur.execute("select Area_ID from  Info_Area_tbl where Area_name='%s';"%(floor))
		ar_rows=g_cur.fetchall()
		for ar_row in ar_rows:
			Area_ID=ar_row[0]
		new_F_value=str(Area_ID)+'%'
		#sql = "select Cam_ID from  Cam_loc_tbl where Cam_ID like '%s' and Cam_name='%s';"%(new_F_value,cam_name)
		sql = "select Cam_ID,Cam_name from  Cam_loc_tbl where Cam_ID like '%s' ;"%(new_F_value)
		g_cur.execute(sql)
		camid_rows = g_cur.fetchall()
		for camid in camid_rows:
			Cam_ID=int(camid[0])
			Cam_name=camid[1]
		#	print Cam_ID,Cam_name
			g_cur.execute("select * from Rem_Rec where Cam_ID = '%d' ;"%(Cam_ID))
			n_rows = g_cur.fetchall()
			for n_row in n_rows:
				Nvr_IP=n_row[1]
				Channel=n_row[2]
				Brk_IP=n_row[3]
				value="%s|%s|%s|%s"%(floor,Nvr_IP,Channel,Brk_IP)
				value1="%s|%s"%(floor,Channel)
				#print floor,Cam_name,Nvr_IP,Channel,Brk_IP
				write_nvr_all_conf(value)
				write_nvr_work_conf(value1)
		#g_cur.execute("insert into Rem_Rec (Cam_ID,Nvr_IP,Channel,Brk_IP) values('%d','%s','%s','%s');"%(Cam_ID,Nvr_IP,Channel,Brk_IP))
		
		closeDB()
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
		sys.exit()
	except:
	 	print "Unexpected error:", sys.exc_info()[0]
	
	
main()	
