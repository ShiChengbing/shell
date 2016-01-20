#!/usr/bin/python


import os,sys
import string

import vaconf_db
import vaconf_p_cam
import vaconf_p_dump

con_list=[]
F40_con_dic={}
F40_keys=[]
first_keys=[]
first_value=[]
second_value=[]

def F40_conf(g_cam_id,first_value,g_cur):
	F40_values=g_cam_id+first_value
	vaconf_db.g_cur.execute('insert into F40_tbl values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',F40_values)

def get_F40keys(max):
        global con_list
        global F40_con_dic
        global F40_keys
	for i in range(0,max):
		line_value=vaconf_db.F40_lines[i]
		vaconf_db.find_str(line_value,con_list)
		con_key=con_list[0]
		F40_keys.append(con_key)
		con_value=con_list[1]
		F40_con_dic[con_key]=con_value
		con_list=[]
	return F40_keys

def get_keysite(key):
	global key_site
	key_site="%s_site"%(key)
	key_site=F40_keys.index(key)
	return key_site

def get_firstvalue(first_keys):
        global first_value
        for first_key in first_keys:
                first_values=F40_con_dic[first_key]
                first_value.append(first_values)
        return first_value

def get_secondvalue(second_keys):
        global second_value
        for second_key in second_keys:
                second_values=F40_con_dic[second_key]
                second_value.append(second_values)
        return second_value

def get_ROIvalue(keys):
       # global ROI_value
        for key in keys:
                ROI_values=F40_con_dic[key]
                ROI_value.append(ROI_values)
        return ROI_value

nROI_keys=[]

def parse_F40():
	
	try:
                camid_init=vaconf_p_cam.g_camid_init
                print 'camid_init:',camid_init
                if camid_init != 0:
                        vaconf_db.g_cur.execute("select Cam_ID,Cam_name from Cam_loc_tbl where Cam_ID=%d;"%camid_init)
                        cam_rows = vaconf_db.g_cur.fetchall()
                        if not cam_rows:
                                print 'F40 %d is Invalid!!!!'%camid_init
                        else:
				for cam_row in cam_rows:
					CAM_ID=int(cam_row[0])
                                        if CAM_ID == camid_init:
                                                print " F40 %s already exists!!!!!"%CAM_ID
                                                vaconf_db.g_cur.execute("delete from F40_tbl where Cam_ID=%d;"%camid_init)
                                                vaconf_db.g_cur.execute("delete from F40_line_tbl where Cam_ID=%d;"%camid_init)
                                                camid_init=0
                                                pass
                if camid_init == 0:
	                if len(vaconf_db.F40_lines)==0:
	                        return None
	                #vaconf_db.dbgDumpLines('[F40]', vaconf_db.F40_lines);
	                else:
	                        max=len(vaconf_db.F40_lines)
                        	get_F40keys(max)
	                        #print F40_keys
        	                key='nROI'
	                        nROI_site=get_keysite(key)
	                        first_keys=F40_keys[0:nROI_site+1]
	                        get_firstvalue(first_keys)
				if len(first_value) != 9:
					print 'The length of the first_value error!'
					sys.exit()
	                        F40_conf(vaconf_p_cam.g_cam_id,first_value,vaconf_db.g_cur)
	                        value=[]
	                        nROI=F40_con_dic[key]
	                        if nROI>0:
	                                second_keys=F40_keys[nROI_site+1:]
	                                get_secondvalue(second_keys)
	                                for i in range(0,int(nROI)):
	                                        ROI_size="ROI%d"%(i+1)
	                                        ROI_nPts_str="ROI%d_nPts"%(i+1)
	                                        get_keysite(ROI_nPts_str)
	                                        ROI_nPts_site=key_site
	                                        ROI_nPts=F40_con_dic[ROI_nPts_str]
	                                        ROI_site_end=int(ROI_nPts_site)+1+int(ROI_nPts)*2
	                                        ROI_keys=F40_keys[int(ROI_nPts_site)+1:ROI_site_end]
	                                        F40_line=[]
	                                        point_num=0
	                                        max_line=vaconf_p_cam.g_cam_id[0]+999
	                                        vaconf_db.g_cur.execute("select max(Line_ID) from F40_line_tbl where Line_ID between %s and %s;"%(vaconf_p_cam.g_cam_id[0],max_line))
	                                        line_rows=vaconf_db.g_cur.fetchall()
	                                        for line_row in line_rows:
	                                                Max_line=line_row[0]
	                                                if Max_line == None:
	                                                        Line_ID=vaconf_p_cam.g_cam_id[0]+1
	                                                else:
	                                                        Line_ID=Max_line+1
	
	                                        while point_num<int(ROI_nPts)*2:
	                                                F40_line.append('NULL')
	                                                F40_line.append(Line_ID)
	                                                F40_line.append(vaconf_p_cam.g_cam_id[0])
	                                                F40_line.append(ROI_size)
	                                                F40_line.append(ROI_nPts)
	                                                point_xkey=ROI_keys[point_num]
	                                                point_ykey=ROI_keys[point_num+1]
	                                                point_x_value=F40_con_dic[point_xkey]
	                                                point_y_value=F40_con_dic[point_ykey]
	                                                F40_line.append(point_x_value)
	                                                F40_line.append(point_y_value)
	                                                data1=int(Line_ID)
	                                                data2=int(vaconf_p_cam.g_cam_id[0])
	                                                data3=str(ROI_size)
	                                                data4=int(ROI_nPts)
	                                                data5=int(point_x_value)
	                                                data6=int(point_y_value)
	                                                #print "F40_line:%s"%F40_line
	                                                #vaconf_db.g_cur.execute('insert into F40_line_tbl values(%s,%s,%s,%s,%s,%s,%s)',F40_line)
	                                                vaconf_db.g_cur.execute("insert into F40_line_tbl (Line_ID,Cam_ID,ROI,ROI_nPts,roi_point_x,roi_point_y)values('%d','%d','%s','%d','%d','%d');"%(data1,data2,data3,data4,data5,data6))
	                                                F40_line=[]
	                                                point_num+=2


        except BaseException, e:
                print 'Unknown error (',str(e),') happened in parse_F40'
                return None

				

def f40_dump():
	try:
		Cam_ID=vaconf_db.select_CAMID()
		print 'F40 Cam_ID',Cam_ID
        	vaconf_db.g_cur.execute("select * from F40_tbl where Cam_ID='%s';"%(Cam_ID))
        	rows = vaconf_db.g_cur.fetchall()
		if not rows:
			print " no F40 function !!!"
			pass
		else:
	        	for row in rows:
        		        flag='flag=%s'%(row[1])
        		        BackImagePath='BackImagePath=%s'%(row[2])
        	        	DownSampleWidth='DownSampleWidth=%s'%(row[3])
	        	        DownSampleHeight='DownSampleHeight=%s'%(row[4])
        		        IfShadow='IfShadow=%s'%(row[5])
        		        WeightNum_y='WeightNum_y=%s'%(row[6])
        	        	WeightCoefficient='WeightCoefficient=%s'%(row[7])
	        	        NormalizationCoefficient='NormalizationCoefficient=%s'%(row[8])
        		        nROI='nROI=%s'%(row[9])
        		        nROI_size=row[9]
        	        	#print nROI_size
        #*********** creat F40 conf   *****************************************************                     
	        	vaconf_p_dump.write_conf(flag)
        		vaconf_p_dump.write_conf(BackImagePath)
        		vaconf_p_dump.write_conf(DownSampleWidth)
        		vaconf_p_dump.write_conf(DownSampleHeight)
	        	vaconf_p_dump.write_conf(IfShadow)
        		vaconf_p_dump.write_conf(WeightNum_y)
	        	vaconf_p_dump.write_conf(WeightCoefficient)
        		vaconf_p_dump.write_conf(NormalizationCoefficient)
        		vaconf_p_dump.write_conf(nROI)
		
		        if nROI_size>0:
	        	        nROI_sum=1
	                	while nROI_sum<=nROI_size:
		                        ROI_value='ROI%d'%nROI_sum
					Line_ID=Cam_ID+nROI_sum
		                        ROI_values='%s=%d'%(ROI_value,Line_ID)
	        	                #Line_ID=Cam_ID+nROI_sum
	                	        vaconf_db.g_cur.execute("select * from F40_line_tbl where Line_ID='%s' limit 1;"%(Line_ID))
	                        	rows = vaconf_db.g_cur.fetchall()
		                        for row in rows:
		                                ROI_nPts_size=row[4]
	        	                ROI_nPts='%s_nPts=%s'%(ROI_value,ROI_nPts_size)
	                	        vaconf_p_dump.write_conf(ROI_values)
	                        	vaconf_p_dump.write_conf(ROI_nPts)
		                        for i in range(0,ROI_nPts_size):
		                                Rpoint_x='%s_point%d.x'%(ROI_value,i+1)
	        	                        Rpoint_y='%s_point%d.y'%(ROI_value,i+1)
	                	                vaconf_db.g_cur.execute("select * from F40_line_tbl where Line_ID='%s' order by Line_index limit %s,1;"%(Line_ID,i))
	                        	        rows = vaconf_db.g_cur.fetchall()
	                                	for row in rows:
	                                        	Rpoint_xvalue=row[5]
		                                        Rpoint_yvalue=row[6]
		                                ROI_point_x='%s=%s'%(Rpoint_x,Rpoint_xvalue)
	        	                        ROI_point_y='%s=%s'%(Rpoint_y,Rpoint_yvalue)
	                	                vaconf_p_dump.write_conf(ROI_point_x)
	                        	        vaconf_p_dump.write_conf(ROI_point_y)
		                        nROI_sum+=1
		
	except BaseException, e:
		print 'Unknown error (',str(e),') happened in f40_dump!'
	return None
