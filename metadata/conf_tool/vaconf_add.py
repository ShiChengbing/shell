#!/usr/bin/python

import os,sys
import string

import vaconf_db
import vaconf_p_cam
import vaconf_p_f10
import vaconf_p_f20
import vaconf_p_f30
import vaconf_p_f40
import vaconf_p_f50

######################################################################
# the file partition for each segment
######################################################################

def main(ifile):
	# open ifile and read in
	try:
		for i in open(ifile):
			#line_value=i[0:-1]
			line_value=string.strip(i)	
			if len(line_value)>0:
				vaconf_db.all_lines.append(line_value)
			else:
				continue
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
		sys.exit()
	except:
	        print "Unexpected error:", sys.exc_info()[0]

	#vaconf_db.dbgDumpLines("The whole file", vaconf_db.all_lines)
        
	# connect database
	vaconf_db.connectDB()
	
	#read in ifile and prepare the sections
	cam_site=vaconf_db.all_lines.index('[CAM]')
	F10_site=vaconf_db.all_lines.index('[F10]')
	F20_site=vaconf_db.all_lines.index('[F20]')
	F30_site=vaconf_db.all_lines.index('[F30]')
	F40_site=vaconf_db.all_lines.index('[F40]')
	F50_site=vaconf_db.all_lines.index('[F50]')

	vaconf_db.cam_lines=vaconf_db.all_lines[cam_site+1:F10_site]
	#print vaconf_db.cam_lines
	#vaconf_db.dbgDumpLines('[CAM]', vaconf_db.cam_lines)
	if F10_site+1<F20_site:
		vaconf_db.F10_lines=vaconf_db.all_lines[F10_site+1:F20_site]
		#dbgDumpLines('[F10]', vaconf_db.F10_lines)
	if F20_site+1<F30_site:
		vaconf_db.F20_lines=vaconf_db.all_lines[F20_site+1:F30_site]
		#dbgDumpLines('[F20]', vaconf_db.F20_lines)
	if F30_site+1<F40_site:
		vaconf_db.F30_lines=vaconf_db.all_lines[F30_site+1:F40_site]
		#dbgDumpLines('[F30]', vaconf_db.F30_lines)
	if F40_site+1<F50_site:
		vaconf_db.F40_lines=vaconf_db.all_lines[F40_site+1:F50_site]
		#print vaconf_db.F40_lines
		#dbgDumpLines('[F40]', vaconf_db.F40_lines)
	if F50_site+1<len(vaconf_db.all_lines):
		vaconf_db.F50_lines=vaconf_db.all_lines[F50_site+1:]
		#dbgDumpLines('[F50]', vaconf_db.F50_lines)
    
	#parse sections one by one
	vaconf_p_cam.parse_CAM()
	vaconf_p_f10.parse_F10()
	vaconf_p_f20.parse_F20()
	vaconf_p_f30.parse_F30()
	vaconf_p_f40.parse_F40()
	vaconf_p_f50.parse_F50()
	  
	#close database
	vaconf_db.closeDB()

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print 'argument missing'
		print 'vaconf_add.py <input file>!'
		sys.exit()

	inputfile = ''

	inputfile = sys.argv[1]
	#print 'Input file is "', inputfile
	try:
		main(inputfile)
	except BaseException, e:
		print 'Unknown error (',str(e),') happened in entry!'
		sys.exit()
	pass

