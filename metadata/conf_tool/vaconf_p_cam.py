#!/usr/bin/python


import os,sys
import string

import vaconf_db
import vaconf_p_dump
import vaconf_p_dump
#********
con_list=[]

g_cam_id=[]

cam_con_dic={}
cam_keys=[]
camvalue=[]
cam_value=[]


def ins_camID(g_CAMarea,cam_id,cam_value,g_cur):
	cam_values=cam_id+cam_value
	d_cam_area=g_CAMarea
	d_Cam_ID=int(cam_id[0])
	d_Cam_name=str(cam_value[0])
	d_cam_FPS=int(cam_value[1])
	d_Matrix1=float(cam_value[2])
	d_Matrix2=float(cam_value[3])
	d_Matrix3=float(cam_value[4])
	d_Matrix4=float(cam_value[5])
	d_Matrix5=float(cam_value[6])
	d_Matrix6=float(cam_value[7])
	d_Matrix7=float(cam_value[8])
	d_Matrix8=float(cam_value[9])
	d_Matrix9=float(cam_value[10])
	d_Matrix10=float(cam_value[11])
	d_Matrix11=float(cam_value[12])
	d_Matrix12=float(cam_value[13])
	d_Matrix13=float(cam_value[14])
	d_Matrix14=float(cam_value[15])
	d_Matrix15=float(cam_value[16])
	d_Matrix16=float(cam_value[17])
	#print g_CAMarea,d_Cam_ID,d_Cam_name,d_cam_FPS,d_Matrix1,d_Matrix2,d_Matrix3,d_Matrix4,d_Matrix5,d_Matrix6,d_Matrix7,d_Matrix8,d_Matrix9,d_Matrix10,d_Matrix11,d_Matrix12,d_Matrix13,d_Matrix14,d_Matrix15,d_Matrix16
	vaconf_db.g_cur.execute("insert into Cam_loc_tbl (Area,Cam_ID,Cam_name,FPS,Matrix1,Matrix2,Matrix3,Matrix4,Matrix5,Matrix6,Matrix7,Matrix8,Matrix9,Matrix10,Matrix11,Matrix12,Matrix13,Matrix14,Matrix15,Matrix16) values('%s','%d','%s','%d','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f');"%(g_CAMarea,d_Cam_ID,d_Cam_name,d_cam_FPS,d_Matrix1,d_Matrix2,d_Matrix3,d_Matrix4,d_Matrix5,d_Matrix6,d_Matrix7,d_Matrix8,d_Matrix9,d_Matrix10,d_Matrix11,d_Matrix12,d_Matrix13,d_Matrix14,d_Matrix15,d_Matrix16))

def upd_maxCAM(new_m_cam,ar_ID,g_cur):
	vaconf_db.g_cur.execute("update Info_Area_tbl set Max_cam='%d'  where Area_ID='%d';"%(new_m_cam,ar_ID))

def get_camvalue(camkeys):
	global camvalue
	for cam_key in camkeys:
		cam_values=cam_con_dic[cam_key]
		camvalue.append(cam_values)
	return camvalue


def parse_CAM():
	global g_cam_id
	global con_list
	global cam_con_dic
	global cam_keys
	global cam_value
	global g_CAMarea
	global g_camid_init
	try:
        	if len(vaconf_db.cam_lines)==0: 
        		return None
		#vaconf_db.dbgDumpLines('[CAM]', vaconf_db.cam_lines);
		else:
			max=len(vaconf_db.cam_lines)
			for i in range(0,max):
				line_value=vaconf_db.cam_lines[i]
				vaconf_db.find_str(line_value,con_list)
				con_key=con_list[0]
				cam_keys.append(con_key)
				con_value=con_list[1]
				cam_con_dic[con_key]=con_value
				con_list=[]

	############ Registration area ##################################################
		camkeys=cam_keys[0]
		CAMarea=cam_con_dic[camkeys]
		g_CAMarea=CAMarea
		area_values=[]
        	area_values.append('NULL')
        	area_values.append(CAMarea)
		Max_cam=0
		area_values.append(Max_cam)
		vaconf_db.g_cur.execute("select Area_name,Max_cam from Info_Area_tbl where Area_name=%s;",CAMarea)
		#area_rows=vaconf_db.g_cur.fetchall()
		area_rows=vaconf_db.g_cur.fetchone()
		if not area_rows:
			data1=str(CAMarea)
			data2=int(Max_cam)
			#vaconf_db.g_cur.execute("insert into Info_Area_tbl values(%s,%s,%s)",area_values)
			vaconf_db.g_cur.execute("insert into Info_Area_tbl (Area_name,Max_cam) values('%s','%d');"%(data1,data2))
		else:
	       		#for area_row in area_rows:
	       		Areaname=area_rows[0]
			#print "Area_name",Areaname
			if Areaname==CAMarea:
				print "%s already exists!!!!!"%CAMarea
			else:
				print "CAMarea error happend in Registration area! "
				sys.exit()    

	############# creat cam_ID #######################################################
		camkeys=cam_keys[1]
		g_camid_init=int(cam_con_dic[camkeys])
		if g_camid_init != 0:
			cam_ID=g_camid_init
			g_cam_id=[cam_ID]
			#print g_cam_id
		else:	
			vaconf_db.g_cur.execute("select Area_ID,Max_cam from Info_Area_tbl where Area_name=%s;",CAMarea)
			ar_rows = vaconf_db.g_cur.fetchall()
			for ar_row in ar_rows:
	    			ar_ID=ar_row[0]
				m_cam=ar_row[1]
				mv_ar_num=ar_ID*1000000
			new_m_cam=int(m_cam+1)
			mv_m_cam=(m_cam+1)*1000
			cam_ID=int(mv_ar_num+mv_m_cam)
			cam_id=[cam_ID]
			g_cam_id=cam_id
			#print "cam_id",cam_id
	############# get cam_value  #####################################################
	        	camkeys=cam_keys[2:]
        		get_camvalue(camkeys)
        		cam_value=camvalue
        		#print"cam_value:", cam_value

        ############# insert value into cam_local_tbl ####################################
		vaconf_db.g_cur.execute("select Cam_ID from Cam_loc_tbl where Cam_ID=%d;"%cam_ID)
		cam_rows = vaconf_db.g_cur.fetchone()
		#print cam_rows
		if not cam_rows:
        	        ins_camID(g_CAMarea,cam_id,cam_value,vaconf_db.g_cur)
        	        upd_maxCAM(new_m_cam,ar_ID,vaconf_db.g_cur)
		else:
			CAM_ID=int(cam_rows[0])
			if CAM_ID == cam_ID:
				print "%s already exists!!!!!"%CAM_ID
				sys.exit()
			else:
				print 'CAMID error happend in insert value into cam_local_tbl!'
				sys.exit()


	except BaseException, e:
		print 'Unknown error (',str(e),') happened in parse_CAM!'
		return None

    
def cam_dump():
	
        #*************  get CAMID      ******************************************************
        #CAMarea_ID=vaconf_p_dump.floor
	#vaconf_p_dump.write_conf(CAMarea_ID)
	Cam_ID=vaconf_db.select_CAMID()
	print 'CAM Cam_ID',Cam_ID

        #************ select cam *************************************************************
        tbl='Cam_loc_tbl'
        #Cam_ID='100100'
        vaconf_db.g_cur.execute("select * from %s where CAM_ID='%s';"%(tbl,Cam_ID))
        rows = vaconf_db.g_cur.fetchall()
        for row in rows:
                CAMID="CAMID=%s"%(row[0])
		Area="Area=%s"%(row[1])
                CAMname="CAMname=%s"%(row[2])
		FPS="FPS=%s"%(row[3])
                HomographyMatrix_11="HomographyMatrix_11=%s"%(row[4])
                HomographyMatrix_12="HomographyMatrix_12=%s"%(row[5])
                HomographyMatrix_13="HomographyMatrix_13=%s"%(row[6])
                HomographyMatrix_14="HomographyMatrix_14=%s"%(row[7])
                HomographyMatrix_21="HomographyMatrix_21=%s"%(row[8])
                HomographyMatrix_22="HomographyMatrix_22=%s"%(row[9])
                HomographyMatrix_23="HomographyMatrix_23=%s"%(row[10])
                HomographyMatrix_24="HomographyMatrix_24=%s"%(row[11])
                HomographyMatrix_31="HomographyMatrix_31=%s"%(row[12])
                HomographyMatrix_32="HomographyMatrix_32=%s"%(row[13])
                HomographyMatrix_33="HomographyMatrix_33=%s"%(row[14])
                HomographyMatrix_34="HomographyMatrix_34=%s"%(row[15])
                HomographyMatrix_41="HomographyMatrix_41=%s"%(row[16])
                HomographyMatrix_42="HomographyMatrix_42=%s"%(row[17])
                HomographyMatrix_43="HomographyMatrix_43=%s"%(row[18])
                HomographyMatrix_44="HomographyMatrix_44=%s"%(row[19])
        #************ creat cam conf *******************************************************
	vaconf_p_dump.write_conf(Area)
        vaconf_p_dump.write_conf(CAMID)
        vaconf_p_dump.write_conf(CAMname)
	vaconf_p_dump.write_conf(FPS)
        vaconf_p_dump.write_conf(HomographyMatrix_11)
        vaconf_p_dump.write_conf(HomographyMatrix_12)
        vaconf_p_dump.write_conf(HomographyMatrix_13)
        vaconf_p_dump.write_conf(HomographyMatrix_14)
        vaconf_p_dump.write_conf(HomographyMatrix_21)
        vaconf_p_dump.write_conf(HomographyMatrix_22)
        vaconf_p_dump.write_conf(HomographyMatrix_23)
        vaconf_p_dump.write_conf(HomographyMatrix_24)
        vaconf_p_dump.write_conf(HomographyMatrix_31)
        vaconf_p_dump.write_conf(HomographyMatrix_32)
        vaconf_p_dump.write_conf(HomographyMatrix_33)
        vaconf_p_dump.write_conf(HomographyMatrix_34)
        vaconf_p_dump.write_conf(HomographyMatrix_41)
        vaconf_p_dump.write_conf(HomographyMatrix_42)
        vaconf_p_dump.write_conf(HomographyMatrix_43)
        vaconf_p_dump.write_conf(HomographyMatrix_44)
        return None
	
	

