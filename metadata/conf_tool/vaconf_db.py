#!/usr/bin/python

import os,sys
import string
import MySQLdb
import vaconf_p_dump

#
# raw file data 
#
all_lines=[]

cam_lines=[]
F10_lines=[]
F20_lines=[]
F30_lines=[]
F40_lines=[]
F50_lines=[]
con_list=[]

####   sql db connections
g_conn=''
g_cur=''

def connectDB():
    global g_conn
    global g_cur
    try:
        g_conn=MySQLdb.connect(host='10.110.9.6',user='labmysql',passwd='123456',port=3306)
        #g_conn=MySQLdb.connect(host='10.110.0.35',user='labmysql',passwd='123456',port=3306)
        g_cur=g_conn.cursor()
        #g_conn.select_db('ConfigDataDB')
        g_conn.select_db('MetaDataDB')
        #g_conn.select_db('meta')
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

def find_str(line_value,con_list):
        str_index=line_value.find(r'=')
        key=line_value[0:str_index]
        value=line_value[str_index+1:]
        con_list.append(key)
        con_list.append(value)
        return con_list

#debug dump lines
def dbgDumpLines(name, lines):
    if name != '':
        print "<<<<<<",name,">>>>>>"
    try:
        max=len(lines)
        for i in range(0, max):
            print lines[i]
	    #line_vlue=lines[i]
	    #con_list=[]
	    #find_str(line_value,con_list)
	    #print con_list
    except:
        print 'Error happend in dbgDumpLines()'
        sys.exit()

def select_CAMID():
	global Cam_ID
	Area=vaconf_p_dump.floor
	Cam_name=vaconf_p_dump.cam_n
	print '>>>>',Area,Cam_name
	sql="select Cam_ID from Cam_loc_tbl where Area='%s'and Cam_name='%s';"%(Area,Cam_name)
#	print sql
	g_cur.execute(sql)
	row = g_cur.fetchone()
	Cam_ID=row[0]
	return Cam_ID


