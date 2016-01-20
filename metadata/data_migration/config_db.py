#!/usr/bin/python

import os,sys
import string
import MySQLdb

####   sql db connections
c_conn=''
c_cur=''

def connectCDB():
    global c_conn
    global c_cur
    try:
        c_conn=MySQLdb.connect(host='10.110.9.6',user='labmysql',passwd='123456',port=3306)
        c_cur=c_conn.cursor()
        c_conn.select_db('ConfigDataDB')
    except MySQLdb.Error, e:
        print 'Connecting to ConfigDataDB DB failed!'
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        sys.exit();

def closeCDB():
    global c_conn
    global c_cur
    try:
        c_conn.commit()
        c_conn.close()
    except MySQLdb.Error, e:
        print 'Closing ConfigDataDB DB failed!'
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        sys.exit();
    except:
        print 'Unknown error happened in closeDB()'
        sys.exit()



