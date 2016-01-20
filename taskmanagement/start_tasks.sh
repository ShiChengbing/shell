#!/bin/bash
id &> /tmp/bbb
res_dir="/home/labadmin/va_task_platform/$1"
task_dir="/home/labadmin/va_task_platform/$2"

work_dir="/home/labadmin/va_task_platform"


if [ $# -lt 2 ]
then
	echo 'Parameter is not enough !!!'
        echo 'Examples of parameter format: res.conf task.conf'
fi

dispatch_dir='/apps_root/task_dispatch'

nod_all=`awk '{print $1}' $res_dir | tr '\n' ' '`
cap_all=`awk '{print $2}' $res_dir | tr '\n' ' '`
nod_list=($nod_all)
cap_list=($cap_all)
res_num=${#nod_list[@]}
echo "res_num"$res_num
let seq_num=$res_num-1

mkdir -p $dispatch_dir

task_num=1
for i in `seq 0 $seq_num`
do 
	task_name=${nod_list[$i]}
	echo $task_name
	cap=${cap_list[$i]}
	
	let st_num=$task_num+$cap-1
	#echo " $task_num,$st_num"
	sed -n "$task_num,${st_num}p" $task_dir > $work_dir/$task_name
	#sed -n "$task_num,${st_num}p" $task_dir > /home/labadmin/va_task_platform/$task_name
	cp $work_dir/$task_name $dispatch_dir  2> /dev/null

	let task_num=$task_num+$cap
	each_task=`cat $task_name|wc -l`
	let actual_task=$actual_task+$each_task
done
#cd $work_dir
cp $work_dir/* $dispatch_dir

rm -rf $dispatch_dir/task_log/*
rm -rf $dispatch_dir/*.done

all_task=`cat task.conf|wc -l`
if [ $actual_task -ge $all_task  ]
then
	echo 'check the task number is correct ' 
	for host in $nod_all
	do
		echo $host
		ssh $host "$dispatch_dir/nod_pre.sh $host" 2> /dev/null
	done
else
	echo 'check the task number is error'
fi

for nod in $nod_all
do
        while [ 1 -gt 0  ]
        do

                if [ -f $dispatch_dir/$nod.done ]
                then
                        echo $nod'.done'
                        break
                else
                        sleep 1
                fi
        done
done

cat $dispatch_dir/task_log/* >$dispatch_dir/all_log	
cp $dispatch_dir/all_log $dispatch_dir/active_log
echo 'Task to create success !'
exit 0


