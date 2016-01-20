#!/bin/bash

#begin_time=`date -d last-day +%Y%m%d%H%M%S`
#end_time=`date +%Y%m%d%H%M%S`
begin_time='20131015130000'
end_time='20131015131000'
step_value=1
interval=1
echo $begin_time
echo $end_time
#exit 0


#begin_time=$1
#end_time=$2
#step_value=$3
#interval=$4
pid=$$
#if [ $# -lt 4 ]
#then
#        echo 'Parameter is not enough !!!'
#        echo 'Examples of parameter format: 20131015130000 20131015140000 30 5'
#	exit 0
#fi




nohup /apps_root/develop/kewei/apps_root/metadata/data_migration/data_migration_f10.py $begin_time $end_time $step_value $interval & #>> f10_$pid.log &
nohup /apps_root/develop/kewei/apps_root/metadata/data_migration/data_migration_f20.py $begin_time $end_time $step_value $interval & #>> f20_$pid.log &
nohup /apps_root/develop/kewei/apps_root/metadata/data_migration/data_migration_f30.py $begin_time $end_time $step_value $interval & #>> f30_$pid.log &
nohup /apps_root/develop/kewei/apps_root/metadata/data_migration/data_migration_f40.py $begin_time $end_time $step_value $interval & #>> f40_$pid.log &
