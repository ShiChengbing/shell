#!/bin/bash

dispatch_dir='/apps_root/task_dispatch'
res_conf=$1
LOGFILE=$dispatch_dir/$2


nod_names=`awk '{print $1}' $dispatch_dir/$res_conf`
mkdir -p $dispatch_dir
cp /home/labadmin/va_task_platform/kill.sh $dispatch_dir
for host in $nod_names
do
	PID=`grep $host $LOGFILE|awk -F ',' '{print $2}'| tr '\n' ' '`
	echo " $host kill -9 $PID"
	for pid in $PID
	do
		#ssh $host kill -9 $PID
		ssh $host "$dispatch_dir/kill.sh $pid" 2> /dev/null
	done

done
rm -rf $dispatch_dir/task_log/*
#rm -rf $dispatch_dir/all_log
#echo 'none,none,none,none;' > $dispatch_dir/all_log



