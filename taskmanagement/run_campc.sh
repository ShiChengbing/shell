#!/bin/bash

FLOOR=$1
CAMID=$2
PID=$$
HN=`hostname`
work_file="work_campc_${HN}_$PID"

mkdir -p /home/labadmin/va_tasks/$work_file
cd /home/labadmin/va_tasks/$work_file
cp /apps_root/task_dispatch/cam_pc /home/labadmin/va_tasks/$work_file
cp /apps_root/task_dispatch/nvr_rec_all.conf /home/labadmin/va_tasks/$work_file 
cp /apps_root/task_dispatch/pcpipe /home/labadmin/va_tasks/$work_file
cp /apps_root/env_setup/$1/$2/background.bmp /home/labadmin/va_tasks/$work_file
cp /apps_root/env_setup/$1/$2/$2.conf /home/labadmin/va_tasks/$work_file

bakg_num=`cat -n $2.conf |grep background.bmp |awk -F ' ' '{print $1}'`
bakg_pwd=`pwd`
sed -i "${bakg_num}iBackImagePath=$bakg_pwd/background.bmp" $2.conf
bakg_del=`(awk 'BEGIN{print '$bakg_num'+1 }')`
#echo 'bakg_del:'$bakg_del
sed -i "${bakg_del}d" $2.conf
nohup ./cam_pc -v=./$2.conf -a=./nvr_rec_all.conf &
#nohup ./cam_pc -v=./$2.conf -a=./nvr_rec_all.conf  |./pcpipe &
campc_PID=$!
echo $HN $campc_PID $1 $2 >> /home/labadmin/va_tasks/$HN.log

