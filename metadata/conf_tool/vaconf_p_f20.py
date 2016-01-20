#!/usr/bin/python


import os,sys
import string

import vaconf_db
import vaconf_p_cam
import vaconf_p_dump

con_list=[]
F20_con_dic={}
F20_keys=[]
first_value=[]
second_value=[]

def get_F20keys(max):
        global con_list
        global F20_con_dic
        global F20_keys
        for i in range(0,max):
                line_value=vaconf_db.F20_lines[i]
                vaconf_db.find_str(line_value,con_list)
                con_key=con_list[0]
                F20_keys.append(con_key)
                con_value=con_list[1]
                F20_con_dic[con_key]=con_value
                con_list=[]
        return F20_keys

def get_keysite(key):
        global key_site
        #key_site="%s_site"%(key)
        key_site=F20_keys.index(key)
        return key_site

def get_firstvalue(first_keys):
        global first_value
        for first_key in first_keys:
                first_values=F20_con_dic[first_key]
                first_value.append(first_values)
        return first_value

def get_secondvalue(second_keys):
        global second_value
        for second_key in second_keys:
                second_values=F20_con_dic[second_key]
                second_value.append(second_values)
        return second_value


def F20_conf(g_cam_id,first_value,g_cur):
        F20_values=g_cam_id+first_value
        vaconf_db.g_cur.execute('insert into F20_tbl values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',F20_values)

def parse_F20():
	try:
                camid_init=vaconf_p_cam.g_camid_init
                #print 'camid_init:',camid_init
                if camid_init != 0:
                        vaconf_db.g_cur.execute("select Cam_ID,Cam_name from Cam_loc_tbl where Cam_ID=%d;"%camid_init)
                        cam_rows = vaconf_db.g_cur.fetchall()
                        if not cam_rows:
                                print 'F20 %d is Invalid!!!!'%camid_init
                        else:
                                for cam_row in cam_rows:
                                        CAM_ID=int(cam_row[0])
                                        if CAM_ID == camid_init:
                                                print " F20 %s already exists!!!!!"%CAM_ID
                                                vaconf_db.g_cur.execute("delete from F20_tbl where Cam_ID=%d;"%camid_init)
                                                vaconf_db.g_cur.execute("delete from F20_line_tbl where Cam_ID=%d;"%camid_init)
                                                camid_init=0
                                                pass
		if camid_init == 0:
		
			if len(vaconf_db.F20_lines)==0: 
				return None
			#vaconf_db.dbgDumpLines('[F20]', vaconf_db.F20_lines);
			else:
				#print vaconf_db.F20_lines 
				max=len(vaconf_db.F20_lines)
				get_F20keys(max)
				key='nAlarmROI'
				get_keysite(key)
				first_keys=F20_keys[0:key_site+2]
				get_firstvalue(first_keys)
                	        F20_conf(vaconf_p_cam.g_cam_id,first_value,vaconf_db.g_cur)
                	        value=[]
                	        nAlarmROI=F20_con_dic[key]
				if nAlarmROI>0:
                	                second_keys=F20_keys[key_site+2:]
                	                get_secondvalue(second_keys)
                	                for i in range(0,int(nAlarmROI)):
                	                        ROI_size="ROI%d"%(i+1)
						ROI_alarmType="ROI%d_alarmType"%(i+1)
						ROI_alarmType_value=F20_con_dic[ROI_alarmType]
						ROI_alarmLevel="ROI%d_alarmLevel"%(i+1)
						ROI_alarmLevel_value=F20_con_dic[ROI_alarmLevel]
						ROI_iTripwireDirection="ROI%d_iTripwireDirection"%(i+1)
						ROI_iTripwireDirection_value=F20_con_dic[ROI_iTripwireDirection]
						ROI_iApproachingFrameCount="ROI%d_iApproachingFrameCount"%(i+1)
						ROI_iApproachingFrameCount_value=F20_con_dic[ROI_iApproachingFrameCount]
						ROI_iPassedFrameCount="ROI%d_iPassedFrameCount"%(i+1)
						ROI_iPassedFrameCount_value=F20_con_dic[ROI_iPassedFrameCount]
                                	        ROI_nPts_str="ROI%d_nPts"%(i+1)
						ROI_nPts=F20_con_dic[ROI_nPts_str]
						ROI_dMinTargetSize="ROI%d_dMinTargetSize"%(i+1)
						ROI_dMinTargetSize_value=F20_con_dic[ROI_dMinTargetSize]
						ROI_strDescription="ROI%d_strDescription"%(i+1)
						ROI_strDescription_value=F20_con_dic[ROI_strDescription]
                                	        get_keysite(ROI_nPts_str)
                                        	ROI_nPts_site=key_site
                                        	ROI_site_end=int(ROI_nPts_site)+3+int(ROI_nPts)*2
                                        	ROI_keys=F20_keys[int(ROI_nPts_site)+3:ROI_site_end]
	
        	                                F20_line=[]
                	                        point_num=0
                        	                max_line=vaconf_p_cam.g_cam_id[0]+999
                                	        vaconf_db.g_cur.execute("select max(Line_ID) from F20_line_tbl where Line_ID between %s and %s;"%(vaconf_p_cam.g_cam_id[0],max_line))
                                        	line_rows=vaconf_db.g_cur.fetchall()
	                                        for line_row in line_rows:
        	                                        Max_line=line_row[0]
                	                                if Max_line == None:
                        	                                Line_ID=vaconf_p_cam.g_cam_id[0]+1
                                	                else:
                                        	                Line_ID=Max_line+1
	
        	                                while point_num<int(ROI_nPts)*2:
                	                                F20_line.append('NULL')
                        	                        F20_line.append(Line_ID)
                                	                F20_line.append(vaconf_p_cam.g_cam_id[0])
                                        	        F20_line.append(ROI_size)
							F20_line.append(ROI_alarmType_value)
							F20_line.append(ROI_alarmLevel_value)
							F20_line.append(ROI_iTripwireDirection_value)
							F20_line.append(ROI_iApproachingFrameCount_value)
							F20_line.append(ROI_iPassedFrameCount_value)
                                	                F20_line.append(ROI_nPts)
							F20_line.append(ROI_dMinTargetSize_value)
							F20_line.append(ROI_strDescription_value)
	                                                point_xkey=ROI_keys[point_num]
        	                                        point_ykey=ROI_keys[point_num+1]
                	                                point_x_value=F20_con_dic[point_xkey]
                        	                        point_y_value=F20_con_dic[point_ykey]
                                	                F20_line.append(point_x_value)
                                        	        F20_line.append(point_y_value)
	                                        #        print "F20_line:%s"%F20_line
        	                                        #vaconf_db.g_cur.execute('insert into F20_line_tbl values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',F20_line)
							data1=int(Line_ID)
							data2=int(vaconf_p_cam.g_cam_id[0])
							data3=str(ROI_size)
							data4=int(ROI_alarmType_value)
							data5=int(ROI_alarmLevel_value)
							data6=int(ROI_iTripwireDirection_value)
							data7=int(ROI_iApproachingFrameCount_value)
							data8=int(ROI_iPassedFrameCount_value)
							data9=int(ROI_nPts)
							data10=float(ROI_dMinTargetSize_value)
							data11=str(ROI_strDescription_value)
							data12=int(point_x_value)
							data13=int(point_y_value)
                	                                vaconf_db.g_cur.execute("insert into F20_line_tbl (Line_ID,Cam_ID,ROI,ROI_alarmType,ROI_alarmLevel,ROI_iTripwireDirection,ROI_iApproachingFrameCount,ROI_iPassedFrameCount,ROI_nPts,ROI_dMinTargetSize,ROI_strDescription,roi_point_x,roi_point_y) values('%d','%d','%s','%d','%d','%d','%d','%d','%d','%f','%s','%d','%d');"%(data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11,data12,data13))
                        	                        F20_line=[]
                                	                point_num+=2




	except BaseException, e:
		print 'Unknown error (',str(e),') happened in parse_F20'
	return None

def f20_dump():
	try:
		Cam_ID=vaconf_db.select_CAMID()
		print 'F20 Cam_ID',Cam_ID
		vaconf_db.g_cur.execute("select * from F20_tbl where Cam_ID='%s';"%(Cam_ID))
		rows = vaconf_db.g_cur.fetchall()
		if not rows:
			print " no F20 function !!!"
			pass
		else:
			for row in rows:
				flag='flag=%s'%(row[1])
				dBgThresh='dBgThresh=%s'%(row[2])
				dFactor='dFactor=%s'%(row[3])
				iRefDistance='iRefDistance=%s'%(row[4])
				iDownScale='iDownScale=%s'%(row[5])
				iInitFrame='iInitFrame=%s'%(row[6])
				iLostFrame='iLostFrame=%s'%(row[7])
				dInitLearnRate='dInitLearnRate=%s'%(row[8])
				dInitMean='dInitMean=%s'%(row[9])
				
				dInitStd='dInitStd=%s'%(row[10])
				dInitWeight='dInitWeight=%s'%(row[11])
				dDisWithoutPredict='dDisWithoutPredict=%s'%(row[12])
				dDisWithPredict='dDisWithPredict=%s'%(row[13])
				dMinObjSize='dMinObjSize=%s'%(row[14])
				dMaxObjSize='dMaxObjSize=%s'%(row[15])
				dMinStd='dMinStd=%s'%(row[16])
				dUpdateLearnRate='dUpdateLearnRate=%s'%(row[17])
				iPredictWinLen='iPredictWinLen=%s'%(row[18])
				iStartFrame='iStartFrame=%s'%(row[19])
				
				dSuddenRatio='dSuddenRatio=%s'%(row[20])
				dObjSizeLowRate='dObjSizeLowRate=%s'%(row[21])
				dObjSizeUpRate='dObjSizeUpRate=%s'%(row[22])
				dMaxVelocity='dMaxVelocity=%s'%(row[23])
				bBrectDis='bBrectDis=%s'%(row[24])
				bDesOut='bDesOut=%s'%(row[25])
				bRegionDis='bRegionDis=%s'%(row[26])
				bRegionOut='bRegionOut=%s'%(row[27])
				bSceneOut='bSceneOut=%s'%(row[28])
				bTimeOut='bTimeOut=%s'%(row[29])
				
				bTrajDis='bTrajDis=%s'%(row[30])
				bTypeOut='bTypeOut=%s'%(row[31])
				dNearbyPosition='dNearbyPosition=%s'%(row[32])
				dMediumPosition='dMediumPosition=%s'%(row[33])
				dFarawayPosition='dFarawayPosition=%s'%(row[34])
				dMediumTargetSize='dMediumTargetSize=%s'%(row[35])
				dNearbyTargetSize='dNearbyTargetSize=%s'%(row[36])
				dFarawayTargetSize='dFarawayTargetSize=%s'%(row[37])
				nAlarmROI='nAlarmROI=%s'%(row[38])
				nAlarmROI_size=row[38]
				nNoUse='nNoUse=%s'%(row[39])
	
			vaconf_p_dump.write_conf(flag)
			vaconf_p_dump.write_conf(dBgThresh)
			vaconf_p_dump.write_conf(dFactor)
			vaconf_p_dump.write_conf(iRefDistance)
			vaconf_p_dump.write_conf(iDownScale)
			vaconf_p_dump.write_conf(iInitFrame)
			vaconf_p_dump.write_conf(iLostFrame)
			vaconf_p_dump.write_conf(dInitLearnRate)
			vaconf_p_dump.write_conf(dInitMean)
			vaconf_p_dump.write_conf(dInitStd)
		
			vaconf_p_dump.write_conf(dInitWeight)
			vaconf_p_dump.write_conf(dDisWithoutPredict)
			vaconf_p_dump.write_conf(dDisWithPredict)
			vaconf_p_dump.write_conf(dMinObjSize)
			vaconf_p_dump.write_conf(dMaxObjSize)
			vaconf_p_dump.write_conf(dMinStd)
			vaconf_p_dump.write_conf(dUpdateLearnRate)
			vaconf_p_dump.write_conf(iPredictWinLen)
			vaconf_p_dump.write_conf(iStartFrame)
			vaconf_p_dump.write_conf(dSuddenRatio)
			
			vaconf_p_dump.write_conf(dObjSizeLowRate)
			vaconf_p_dump.write_conf(dObjSizeUpRate)
			vaconf_p_dump.write_conf(dMaxVelocity)
			vaconf_p_dump.write_conf(bBrectDis)
			vaconf_p_dump.write_conf(bDesOut)
			vaconf_p_dump.write_conf(bRegionDis)
			vaconf_p_dump.write_conf(bRegionOut)
			vaconf_p_dump.write_conf(bSceneOut)
			vaconf_p_dump.write_conf(bTimeOut)
			vaconf_p_dump.write_conf(bTrajDis)
			
			vaconf_p_dump.write_conf(bTypeOut)
			vaconf_p_dump.write_conf(dNearbyPosition)
			vaconf_p_dump.write_conf(dMediumPosition)
			vaconf_p_dump.write_conf(dFarawayPosition)
			vaconf_p_dump.write_conf(dMediumTargetSize)
			vaconf_p_dump.write_conf(dNearbyTargetSize)
			vaconf_p_dump.write_conf(dFarawayTargetSize)
			vaconf_p_dump.write_conf(nAlarmROI)
			vaconf_p_dump.write_conf(nNoUse)
			
			if nAlarmROI_size>0:
				nAlarmROI_sum=1
				while nAlarmROI_sum<=nAlarmROI_size:
					ROI_value='ROI%d'%nAlarmROI_sum
					Line_ID=vaconf_db.Cam_ID+nAlarmROI_sum
					ROI_values='%s=%d'%(ROI_value,Line_ID)
					#Line_ID=vaconf_db.Cam_ID+nAlarmROI_sum
					vaconf_db.g_cur.execute("select * from F20_line_tbl where Line_ID='%s' limit 1;"%(Line_ID))
					rows = vaconf_db.g_cur.fetchall()
					for row in rows:
						ROI_nPts_size=row[9]
					#       print "ROI_nPts_size",ROI_nPts_size
					ROI_alarmType='%s_alarmType=%s'%(ROI_value,row[4])
					ROI_alarmLevel='%s_alarmLevel=%s'%(ROI_value,row[5])
					ROI_iTripwireDirection='%s_iTripwireDirection=%s'%(ROI_value,row[6])
					ROI_iApproachingFrameCount='%s_iApproachingFrameCount=%s'%(ROI_value,row[7])
					ROI_iPassedFrameCount='%s_iPassedFrameCount=%s'%(ROI_value,row[8])
					ROI_nPts='%s_nPts=%s'%(ROI_value,ROI_nPts_size)
					ROI_dMinTargetSize='%s_dMinTargetSize=%s'%(ROI_value,row[10])
					ROI_strDescription='%s_strDescription=%s'%(ROI_value,row[11])
					vaconf_p_dump.write_conf(ROI_values)
					vaconf_p_dump.write_conf(ROI_alarmType)
					vaconf_p_dump.write_conf(ROI_alarmLevel)
					vaconf_p_dump.write_conf(ROI_iTripwireDirection)
					vaconf_p_dump.write_conf(ROI_iApproachingFrameCount)
					vaconf_p_dump.write_conf(ROI_iPassedFrameCount)
					vaconf_p_dump.write_conf(ROI_nPts)
					vaconf_p_dump.write_conf(ROI_dMinTargetSize)
					vaconf_p_dump.write_conf(ROI_strDescription)	
					for i in range(0,ROI_nPts_size):
						Rpoint_x='%s_point%d.x'%(ROI_value,i+1)
						Rpoint_y='%s_point%d.y'%(ROI_value,i+1)
						vaconf_db.g_cur.execute("select * from F20_line_tbl where Line_ID='%s' order by Line_index limit %s,1;"%(Line_ID,i))
						rows = vaconf_db.g_cur.fetchall()
						for row in rows:
							Rpoint_xvalue=row[12]
							Rpoint_yvalue=row[13]
						ROI_point_x='%s=%s'%(Rpoint_x,Rpoint_xvalue)
						ROI_point_y='%s=%s'%(Rpoint_y,Rpoint_yvalue)
						vaconf_p_dump.write_conf(ROI_point_x)
						vaconf_p_dump.write_conf(ROI_point_y)
						
						
					nAlarmROI_sum+=1
		
	except BaseException, e:
		print 'Unknown error (',str(e),') happened in f20_dump!'
	return None
