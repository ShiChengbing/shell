#!/usr/bin/python

import os,sys
import string
import MySQLdb


####   sql db connections
a_conn=''
a_cur=''

def connectADB():
    global a_conn
    global a_cur
    try:
        a_conn=MySQLdb.connect(host='10.110.9.6',user='labmysql',passwd='123456',port=3306)
        a_cur=a_conn.cursor()
        a_conn.select_db('ActiveDataDB')
        #a_conn.select_db('meta')
    except MySQLdb.Error, e:
        print 'Connecting to ActiveDataDB failed!'
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        sys.exit();

def closeADB():
    global a_conn
    global a_cur
    try:
        a_conn.commit()
        a_conn.close()
    except MySQLdb.Error, e:
        print 'Closing ActiveDataDB failed!'
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        sys.exit();
    except:
        print 'Unknown error happened in closeDB()'
        sys.exit()



