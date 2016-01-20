#!/bin/bash

dispatch_dir='/apps_root/task_dispatch'
taskwork_dir='/home/labadmin/ramfs/va_tasks'
run_campc()
{
	FLOOR=$1
	CAMID=$2
	PID=$$
	
	HN=`hostname`
	work_file="work_campc_${PID}_$CAMID"
	
	mkdir -p $taskwork_dir/$work_file
	cd $taskwork_dir/$work_file
	cp $dispatch_dir/cam_pc $taskwork_dir/$work_file
	cp $dispatch_dir/nvr_rec_all.conf $taskwork_dir/$work_file
	cp $dispatch_dir/pcpipe $taskwork_dir/$work_file
	cp /apps_root/env_setup/$FLOOR/$CAMID/background.bmp $taskwork_dir/$work_file
	cp /apps_root/env_setup/$FLOOR/$CAMID/$CAMID.conf $taskwork_dir/$work_file
	
	bakg_num=`cat -n $2.conf |grep background.bmp |awk -F ' ' '{print $1}'`
	bakg_pwd=`pwd`
	sed -i "${bakg_num}iBackImagePath=$bakg_pwd/background.bmp" $2.conf
	bakg_del=`(awk 'BEGIN{print '$bakg_num'+1 }')`
	#echo 'bakg_del:'$bakg_del
	sed -i "${bakg_del}d" $2.conf
	nohup ./cam_pc -v=./$2.conf -a=./nvr_rec_all.conf &
	campc_PID=$!
	echo $HN,$campc_PID,$1,$2";" >> $taskwork_dir/$HN.log

}

HN=`hostname`
conf_name=$1
echo 'conf_name' $conf_name
mkdir -p $taskwork_dir
cd $taskwork_dir
#cp $dispatch_dir/run_campc.sh ./
rm -rf work_campc_*
rm $HN.log
pipe_pro=`ps axf|grep cam_pc|wc -l`
if [ $pipe_pro -eq 1 ]
then
        echo "cam_pc: no process found !!!"
else
        #sudo killall pcpipe
        sudo killall cam_pc
fi


floor_all=`awk '{print $1}' $dispatch_dir/$conf_name | tr '\n' ' '`
cam_all=`awk '{print $2}' $dispatch_dir/$conf_name | tr '\n' ' '`
floor_list=($floor_all)
cam_list=($cam_all)
line_max=`cat $dispatch_dir/$conf_name|wc -l`
let line_max=$line_max-1
for line_num in `seq 0 $line_max`
do	
        floor_name=${floor_list[$line_num]}
        cam_name=${cam_list[$line_num]}
	echo $floor_name $cam_name
	run_campc $floor_name $cam_name
done
mkdir -p $dispatch_dir/task_log
mv $taskwork_dir/$HN.log $dispatch_dir/task_log/
echo "$HN.log done" >$dispatch_dir/$HN.done

