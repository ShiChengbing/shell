#!/usr/bin/python

import os,sys
import string
import MySQLdb

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
h_conn=''
h_cur=''

def connectHDB():
    global h_conn
    global h_cur
    try:
        h_conn=MySQLdb.connect(host='10.110.9.6',user='labmysql',passwd='123456',port=3306)
        h_cur=h_conn.cursor()
        h_conn.select_db('HistoryDataDB')
        #h_conn.select_db('meta')
    except MySQLdb.Error, e:
        print 'Connecting to HistoryDataDB DB failed!'
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        sys.exit();

def closeHDB():
    global h_conn
    global h_cur
    try:
        h_conn.commit()
        h_conn.close()
    except MySQLdb.Error, e:
        print 'Closing HistoryDataDB DB failed!'
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        sys.exit();
    except:
        print 'Unknown error happened in closeDB()'
        sys.exit()



