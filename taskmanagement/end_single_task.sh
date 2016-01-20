#!/bin/bash

dispatch_dir='/apps_root/task_dispatch'
end_conf_dir='/home/labadmin/va_task_platform/end.conf'
all_log_dir="$dispatch_dir/all_log"
end_log_dir='/home/labadmin/va_task_platform/end_log'
active_log_dir="$dispatch_dir/active_log"

rm -rf $end_log_dir
cat $end_conf_dir|while read line
do
	end_cam=`grep "$line" $all_log_dir`
	sed "/$line/d" $active_log_dir > $dispatch_dir/tmp_log
	mv $dispatch_dir/tmp_log $active_log_dir;
	echo $end_cam >>$end_log_dir
done
cp $end_log_dir /apps_root/task_dispatch
if test -s $active_log_dir
then
	break
else
	echo "none,none,none,none;" >$active_log_dir
fi

#active_log_size=`ls -l $active_log_dir|awk '{print $5}'`
#echo $active_log_size >>$dispatch_dir/size
/home/labadmin/va_task_platform/end_va_tasks.sh res.conf end_log
