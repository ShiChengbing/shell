#!/bin/bash


power_clamp_log="`pwd`/power_clamp.log"
echo $power_clamp_log
> $power_clamp_log


if [ -f /boot/config-$(uname -r) ]
then
	echo "# cat /boot/config-$( uname -r ) | grep POWERCLAMP" |tee -a $power_clamp_log
	cat /boot/config-$( uname -r ) | grep POWERCLAMP |tee -a $power_clamp_log
	intel_rapl_wr=`grep -o "POWERCLAMP" /boot/config-$( uname -r )|head -n 1`
	if [ -z $intel_rapl_wr ];then echo '''"POWERCLAMP" is not set in config !''';fi
fi
if [ -f /proc/config.gz ]
then
        rm ./config
        echo "# cp /proc/config.gz ./" |tee -a $power_clamp_log
        cp /proc/config.gz ./
        echo "# gzip -d config.gz" |tee -a $power_clamp_log
        gzip -d config.gz
        echo "#grep "POWERCLAMP" ./config" |tee -a $power_clamp_log
        grep -i "POWERCLAMP" ./config |tee -a $power_clamp_log
        intel_rapl_wr=`grep -o "POWERCLAMP" ./config|head -n 1`
        if [ -z $intel_rapl_wr ];then echo '''"POWERCLAMP" is not set in config !''';fi
fi



echo "# lsmod | grep powerclamp" |tee -a $power_clamp_log
lsmod | grep powerclamp |tee -a $power_clamp_log
lsmod_str=`lsmod | grep -o powerclamp|head -n 1`
if [ "$lsmod_str"x != "powerclamp"x ]
then
	echo "#modprobe intel_powerclamp"
	modprobe intel_powerclamp
fi
echo '''# thermal_root=/sys/devices/virtual/thermal; for cooldev in $( ls $thermal_root | grep "cooling_device*" ); do printf "$cooldev: $( cat $thermal_root/$cooldev/type )\n"; done''' |tee -a $power_clamp_log
thermal_root=/sys/devices/virtual/thermal; for cooldev in $( ls $thermal_root | grep "cooling_device*" ); do printf "$cooldev: $( cat $thermal_root/$cooldev/type )\n"; done |tee -a $power_clamp_log
cooling_number=`thermal_root=/sys/devices/virtual/thermal; for cooldev in $( ls $thermal_root | grep "cooling_device*" ); do printf "$cooldev: $( cat $thermal_root/$cooldev/type )\n"; done|grep intel_powerclamp|cut -d : -f1`
echo "cooling_number:"$cooling_number |tee -a $power_clamp_log

if [ -z $cooling_number ]
then
	echo -e "The platform not support power_clamp !!!\n" |tee -a $power_clamp_log

else
	echo "# cd /sys/devices/virtual/thermal/${cooling_number}/" |tee -a $power_clamp_log
	cd /sys/devices/virtual/thermal/${cooling_number}
	echo "# cat cur_state" |tee -a $power_clamp_log
	cat cur_state |tee -a $power_clamp_log
	echo "# cat max_state" |tee -a $power_clamp_log
	cat max_state |tee -a $power_clamp_log
	modprobe msr
	for i in 0 25 50
	do
		echo "# pwd" |tee -a $power_clamp_log
		pwd |tee -a $power_clamp_log
		echo "# echo ${i} > cur_state; sleep 2; cat cur_state; turbostat" |tee -a $power_clamp_log
		echo ${i} > cur_state; sleep 2; cat cur_state; turbostat --debug |tee -a $power_clamp_log &
		sleep 10 && kill $! &>/dev/null
		wait $! &>/dev/null
	done
	
fi

