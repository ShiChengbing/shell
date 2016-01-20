#!/usr/bin/python


import os,sys
import vaconf_db
import vaconf_p_cam
import vaconf_p_f10
import vaconf_p_f20
import vaconf_p_f30
import vaconf_p_f40
import vaconf_dump

#floor=''
#cam_n=''
floor=vaconf_dump.floor
cam_n=vaconf_dump.cam_name

def open_file():
	global file_object
	conf_dir="/apps_root/env_setup/"+floor+'/'+cam_n+'/'+cam_n+'.conf'
	print conf_dir
	file_object = open(conf_dir, 'a')

def write_conf(value):
	file_object.write(value)
	file_object.write('\n')

def close_file():
	file_object.close( )

def set_conf(fl, cn):
	global floor
	global cam_n
	floor = fl
	cn = cam_n

