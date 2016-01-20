#!/usr/bin/python


import sys
import vaconf_db
import vaconf_p_cam
import vaconf_p_f10
import vaconf_p_f20
import vaconf_p_f30
import vaconf_p_f40
import vaconf_p_dump

floor=''
cam_name=''
#floor=sys.argv[1]
#cam_name=sys.argv[2]

def main():
		
	try:
		vaconf_db.connectDB()
		
		vaconf_p_dump.open_file()
		#************ creat CAM conf *********
		vaconf_p_dump.write_conf('[CAM]')
		vaconf_p_cam.cam_dump()


		#************ creat F10 conf *********
		vaconf_p_dump.write_conf('[F10]')
		vaconf_p_f10.f10_dump()
		

		#************ creat F20 conf *********
		vaconf_p_dump.write_conf('[F20]')
		vaconf_p_f20.f20_dump()
	
		#************ creat F30 conf *********
		vaconf_p_dump.write_conf('[F30]')
		vaconf_p_f30.f30_dump()

		#************ creat F40 ***************	
		vaconf_p_dump.write_conf('[F40]')
		vaconf_p_f40.f40_dump()

	        #************ creat F50 conf *********
		vaconf_p_dump.write_conf('[F50]')

		vaconf_p_dump.close_file()
		
		vaconf_db.closeDB()
	        
		

		
	except BaseException, e:
		print 'Unknown error (',str(e),') happened in vaconf_p_dump!'


if __name__ == "__main__":
#	floor=sys.argv[1]
#	cam_name=sys.argv[2]
	if len(sys.argv) < 6:
		print 'argument missing'
		main()
#else:
#	floor=''
#	cam_name=''


