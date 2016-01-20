#!/bin/bash
#############################################
#                                           #
#  FileName:  basci_test.sh                 #
#  Author:    chengbingx.y.shi@intel.com    #
#  Time:      2015/03/11                    #
#  Description: bat test client             #
#                                           #
#############################################





pass_msg()
{
        echo -e "\033[42;30m $* Check Pass!  \033[0m"
}

fail_msg()
{
        echo -e "\033[41;30m $* Check Failed!  \033[0m"
}

suse_addrepo()
{
	showmount -e svn-osve
	if [ $? = 0 ]
	then
	        umount svn-osve:/home/test/Share
	        mkdir -p /mnt/iso
		mount svn-osve:/home/test/Share /mnt/iso
	else
		mkdir -p /mnt/iso
	        mount svn-osve:/home/test/Share /mnt/iso
	fi
	killall zypper
	pkill -9 zypper
	rm -rf /etc/zypp/repos.d/*
#	str=`cat /etc/issue |sed -e '/^$/d'|awk '{print $6}'`
#	iso1=`ls /mnt/iso |grep $str`
#	iso2=`ls /mnt/iso/ |grep -i SDK |grep -i DVD1`
#	iso3=`ls /mnt/iso |grep Server`
	
	for i in `ls /mnt/iso |grep -i '.iso'`
	do
	        echo "zypper ar iso:///?iso=/mnt/iso/$i $i"
	        zypper ar iso:///?iso=/mnt/iso/$i $i
	done
	zypper refresh
}

add_repofile()
{
	#WR=`cat /etc/issue |sed -e '/^$/d'|awk '{print $1,$2}'`
	if [ "$OS_NAME" == "Wind River" ]
	then
		echo "you will test wind river !!! "
	else
		#OS_NAME=`lsb_release -i|awk '{print $3}'`
		#OS_NAME="RedHatEnterpriseServer"
		case $OS_NAME in
		Ubuntu)
			echo "Ubuntu"
			#cp ./../apt.conf /etc/apt/
			APT_DIR="/etc/apt/apt.conf"
			> $APT_DIR
			echo '''Acquire::http::proxy "http://proxy.cd.intel.com:911/";''' >> $APT_DIR
			echo '''Acquire::https::proxy "https://proxy.cd.intel.com:912/";''' >> $APT_DIR
			echo '''Acquire::ftp::proxy "ftp://proxy.cd.intel.com:21/";''' >> $APT_DIR
			echo '''Acquire::socks::proxy "socks://proxy.cd.intel.com:1080/";''' >> $APT_DIR
			#apt-get update && apt-get dist-upgrade -y
			apt-get install linux-tools-common linux-tools-`uname -r` -y
			apt-get install gcc make -y
			apt-get install powertop oprofile -y
			apt-get install libncurses5-dev libncursesw5-dev -y
		;;
		SUSE)
			suse_addrepo
			zypper in -y kernel-default-devel
			zypper in -y perf 
			zypper in -y automake
			zypper in -y oprofile 
			zypper in -y powertop	
		;;
		RedHatEnterpriseClient)
			echo "you will test redhat!"
			echo "please input test OS version:"
			echo "eg:"RHEL-7.1-Beta-1""
			read REDHAT_VERSION
			#cp ./../linux-ftp.repo /etc/yum.repos.d/
			LINUX_FTP="/etc/yum.repos.d/linux-ftp.repo"
			> $LINUX_FTP
			echo '''[linux-ftp]''' >> $LINUX_FTP 
			echo '''name=linux-ftp''' >> $LINUX_FTP 
			echo "baseurl=http://linux-ftp.bj.intel.com/pub/ISO/redhat/redhat-rhel/$REDHAT_VERSION/Client/x86_64/os/" >> $LINUX_FTP 
			#echo "baseurl=http://linux-ftp.bj.intel.com/pub/ISO/redhat/redhat-rhel/$REDHAT_VERSION/Server-optional/" >> $LINUX_FTP 
			echo '''enabled=1''' >> $LINUX_FTP 
			echo '''gpgcheck=0''' >> $LINUX_FTP
			yum update
			yum install  gcc perf powertop oprofile -y 
		;;
		RedHatEnterpriseServer)
			echo "you will test redhat!"
			echo "please input test OS version:"
			echo "eg:"RHEL-7.1-Beta-1""
			read REDHAT_VERSION 
			#cp ./../linux-ftp.repo /etc/yum.repos.d/
			LINUX_FTP="/etc/yum.repos.d/linux-ftp.repo"
			> $LINUX_FTP
			echo '''[linux-ftp]''' >> $LINUX_FTP 
			echo '''name=linux-ftp''' >> $LINUX_FTP 
			echo "baseurl=http://linux-ftp.bj.intel.com/pub/ISO/redhat/redhat-rhel6/$REDHAT_VERSION/Server/x86_64/os/" >> $LINUX_FTP 
			echo "baseurl=http://linux-ftp.bj.intel.com/pub/ISO/redhat/redhat-rhel/$REDHAT_VERSION/Server-optional/" >> $LINUX_FTP 
			echo '''enabled=1''' >> $LINUX_FTP 
			echo '''gpgcheck=0''' >> $LINUX_FTP
			yum update
			yum install gcc perf powertop oprofile -y
		;;
		*)
			echo "OS_NAME: $OS_NAME not found!"
		esac
	fi
}

bios_check()
{
	echo -e  "\n##########  BIOS VERSION ##########" |tee -a $LOG_NAME 
	#WR=`cat /etc/issue |sed -e '/^$/d'|awk '{print $1,$2}'`
	if [ "$OS_NAME" == "Wind River" ]
	then
		echo "wind river no dmidecode command,please check bios!" |tee -a $LOG_NAME
	else
		#OS_NAME=`lsb_release -i|awk '{print $3}'`
		which dmidecode &>/dev/null
		if [ $? -ne 0 ]
		then
		        case $OS_NAME in
		        Ubuntu)
		                echo "Ubuntu"
		                apt-get install dmidecode -y
		        ;;
		        SUSE)   
		                echo "dmidecode command not found!"
		                echo "installing dmidecode....."
		                zypper install -y dmidecode
		        ;;
		        RedHatEnterpriseClient)
		                echo "RedHatEnterpriseClient"
				yum install dmidecode -y
				
		        ;;
		        *)
		                echo "OS_NAME: $OS_NAME not found!"
		        esac
		fi
		
		BIOS_VERSION=`dmidecode -s bios-version` 
		if [ $? -eq 0 ]
		then
			pass_msg BIOS Version |tee -a $LOG_NAME 
			echo "BIOS_VERSION:$BIOS_VERSION" |tee -a $LOG_NAME 
			dmidecode |grep -i "bios information" -A3 >> $LOG_NAME
		else
			fail_msg BIOS Version |tee -a $LOG_NAME
		fi
	fi	
}

dmesg_check()
{
        echo -e "\n##########  DMESG CHECK  ###########" |tee -a $LOG_NAME
        DMESG_ERR_STR=`dmesg |grep -io "error\|failed" -C1 | head -n 1|awk '{print $1}'`
        DMESG_CALL_TRACE_STR=`dmesg | grep -o "Call Trace" | head -n 1|awk '{print $1}'`
        if [ -z $DMESG_ERR_STR ]
        then
                pass_msg DMESG |tee -a $LOG_NAME
        else
                fail_msg DMESG |tee -a $LOG_NAME
                dmesg |grep -i "error\|failed" -C1 |tee -a $LOG_NAME
        fi
        if [ -z $DMESG_CALL_TRACE_STR ]
        then
                pass_msg DMESG Call Trace |tee -a $LOG_NAME
        else
                fail_msg DMESG Call Trace |tee -a $LOG_NAME
		dmesg > dmesg.log
                CT_START=`cat -n dmesg.log|grep "Call Trace"|head -n 1|awk '{print $1}'`
                CT_END=`cat -n dmesg.log|grep "end trace"|head -n 1|awk '{print $1}'`
		rm -rf dmesg.log
                #if [ $CT_START -gt 0 -a $CT_END -gt 0 -a $CT_END -gt $CT_START  ]
                if [ -z $CT_END ]
                then
                        dmesg | grep -B5 -A20 "Call Trace" |tee -a $LOG_NAME

                elif [ $CT_START -gt 0 -a $CT_END -gt 0 -a $CT_END -gt $CT_START  ]
                then
                        CT_ROWS=`expr $CT_END - $CT_START`
                        dmesg | grep -B5 -A$CT_ROWS "Call Trace" |tee -a $LOG_NAME
                else
                        echo "errrrrrrrrrrrrrrrrrrrrrrrror"     
                fi
        fi
}





devices_check()
{ 
	echo -e "\n##########  DEVICES CHECK  ##########" |tee -a $LOG_NAME 
	#DEVICES_ERR=`lspci | grep -E "( |^)[0-9a-z]{4}( |$)" | grep -vE "( |^)[0-9]{4}( |$)"`
	DEVICES_ERR_STR=`lspci | grep -io "Intel Corporation Device"|head -n 1|awk '{print $1}'`
	DEVICES_UNKNOWN_STR=`lspci | grep -io unknown|head -n 1|awk '{print $1}'`
	if [ -z "$DEVICES_ERR_STR" -a -z "$DEVICES_UNKNOWN_STR" ]
	then
		pass_msg Devices |tee -a $LOG_NAME 
	else 
		fail_msg Devices 
		lspci | grep -i "Intel Corporation Device" |tee -a $LOG_NAME
		lspci | grep -i "unknown"  |tee -a $LOG_NAME
	fi
	
}

network_check()
{
        ### network check
        echo -e "\n##########  NETWORK INFORMATION  ##########" |tee -a $LOG_NAME
        NETWORK_CONTROLLER_num=`lspci |grep -i intel|grep -i "Ethernet controller"|grep -iv "Intel Corporation Device"|wc -l`
        NETWORK_CONTROLLER_ALL_STR=`lspci |grep -i intel|grep -i "Ethernet controller"|grep -iv "Intel Corporation Device"|awk '{print $1}'`
        if [ $NETWORK_CONTROLLER_num -le 0 ]
        then
                fail_msg Intel Network Devices |tee -a $LOG_NAME                
                lspci |grep -i "Ethernet controller"|tee -a $LOG_NAME
        else
                for NETWORK_CONTROLLER_STR in $NETWORK_CONTROLLER_ALL_STR
                do
                        NETWORK_KERNEL_DRIVER=`lspci -xxx -s $NETWORK_CONTROLLER_STR  -v |grep -i "kernel driver"|awk -F ":" '{print $2}'`
                        if [ -z $NETWORK_KERNEL_DRIVER ]
                        then
                                fail_msg Intel Network Driver
                                lspci|grep $NETWORK_CONTROLLER_STR |tee -a $LOG_NAME
                                lspci -xxx -s $NETWORK_CONTROLLER_STR  -v |tee -a $LOG_NAME
                                ifconfig -a >> $LOG_NAME
                        else
                                pass_msg Intel Network Driver
                                lspci|grep $NETWORK_CONTROLLER_STR |tee -a $LOG_NAME
                                lspci -xxx -s $NETWORK_CONTROLLER_STR  -v >> $LOG_NAME
                                echo `ifconfig -a |grep -i "inet addr"|awk -F " " '{print $1,$2}'`
                        fi

                done
        fi

        GATEWAY=`ip route show |awk '/default/{print $3}'`
        TRANS_PACKETS_NUM=`ping -c 1 $GATEWAY |awk '/transmitted/{print $4}'`
        if [ $TRANS_PACKETS_NUM -eq 1 ]
        then
                pass_msg ping gatway $GATEWAY
        else
                fail_msg ping gateway $GATEWAY
        fi

}

graphic_check()
{
	### Basic Graphic testing
	echo -e "\n##########  VGA INFORMATION  ##########" |tee -a $LOG_NAME 
	VGA_CONTROLLER_num=`lspci |grep -i intel|grep -i "VGA"|awk '{print $1}'|wc -l`
	VGA_CONTROLLER_all_STR=`lspci |grep -i intel|grep -i "VGA"|awk '{print $1}'`
	if [ $VGA_CONTROLLER_num -le 0 ]
	then
		fail_msg Graphic Devices |tee -a $LOG_NAME
		lspci|grep -i "VGA"|tee -a $LOG_NAME
		#lspci -xxx -s `lspci |grep -i "VGA"|awk '{print $1}'`  -v |tee -a $LOG_NAME
	else
		for VGA_CONTROLLER_STR in $VGA_CONTROLLER_all_STR
		do
			VGA_KERNEL_DRIVER=`lspci -xxx -s $VGA_CONTROLLER_STR  -v |grep -i "kernel driver"|awk -F ":" '{print $2}'`
			if [ -z $VGA_KERNEL_DRIVER ]
			then
				fail_msg Graphic driver |tee -a $LOG_NAME
				lspci|grep $VGA_CONTROLLER_STR |tee -a $LOG_NAME
				lspci -xxx -s $VGA_CONTROLLER_STR  -v |tee -a $LOG_NAME
			
			else
				pass_msg Graphic driver |tee -a $LOG_NAME
				lspci|grep $VGA_CONTROLLER_STR |tee -a $LOG_NAME
				lspci -xxx -s $VGA_CONTROLLER_STR  -v >> $LOG_NAME
			fi
		done
	fi
}

audio_check()
{
	### Audio check
	echo -e "\n##########  AUDIO CHECK  ##########" |tee -a $LOG_NAME
	
	AUDIO_STR_num=`lspci |grep -i intel|grep -i "Audio"|awk '{print $1}'|wc -l`
	AUDIO_ALL_STR=`lspci |grep -i intel|grep -i "Audio"|awk '{print $1}'`
	if [ $AUDIO_STR_num -le 0 ]
	then
		fail_msg Audio Devices |tee -a $LOG_NAME
		echo "This system no Audio device !"|tee -a $LOG_NAME
		lspci|grep -i "Audio" |tee -a $LOG_NAME
		#lspci -xxx -s `lspci |grep -i "Audio"|awk '{print $1}'`  -v |tee -a $LOG_NAME

	else
		for AUDIO_STR in $AUDIO_ALL_STR
		do

			AUDIO_KERNEL_DRIVER=`lspci -xxx -s $AUDIO_STR  -v |grep -i "kernel driver"|awk -F ":" '{print $2}'`
			if [ -z $AUDIO_KERNEL_DRIVER ]
			then
				fail_msg Audio driver |tee -a $LOG_NAME
				lspci|grep $AUDIO_STR |tee -a $LOG_NAME
				lspci -xxx -s $AUDIO_STR  -v |tee -a $LOG_NAME
			else
				pass_msg Audio driver |tee -a $LOG_NAME
				lspci|grep $AUDIO_STR |tee -a $LOG_NAME
				lspci -xxx -s $AUDIO_STR  -v >> $LOG_NAME
			fi
		done
	fi
}
usb_check()
{
	### usb3.0 check
	echo -e "\n##########  USB 3.0 CHECK ##########" |tee -a $LOG_NAME

	XHCI_STR=`lspci |grep -i intel|grep -i "XHCI"|head -n 1|awk '{print $1}'`
	if [ -z $XHCI_STR ]
	then
		fail_msg Usb XHCI Devices |tee -a $LOG_NAME
		lspci |grep -i usb|grep -i intel |tee -a $LOG_NAME
		lspci -s `lspci |grep -i usb|grep -i intel|awk '{print $1}'|head -n 1` -v |tee -a $LOG_NAME
		lsusb -t |tee -a $LOG_NAME
	else
		XHCI_KERNEL_DRIVER=`lspci -xxx -s $XHCI_STR  -v |grep -i "kernel driver"|awk -F ":" '{print $2}'`
		if [ -z $XHCI_KERNEL_DRIVER ]
		then
			fail_msg Usb XHCI driver |tee -a $LOG_NAME
			lspci|grep $XHCI_STR |tee -a $LOG_NAME
			lspci -xxx -s $XHCI_STR  -v |tee -a $LOG_NAME
			lsusb -t |tee -a $LOG_NAME
		else
			pass_msg Usb XHCI driver |tee -a $LOG_NAME
			lspci|grep $XHCI_STR |tee -a $LOG_NAME
			lspci -xxx -s $XHCI_STR  -v >> $LOG_NAME
			lsusb -t |tee -a $LOG_NAME
		fi
	fi
}

intel_idle_check()
{
	echo -e "\n##########  Intel_idle CHECK ##########" |tee -a $LOG_NAME
	idle_type=`cat /sys/devices/system/cpu/cpuidle/current_driver`
	if [ $idle_type = intel_idle ]
	then
		pass_msg Intel_idle |tee -a $LOG_NAME
		echo "#cat /sys/devices/system/cpu/cpuidle/current_driver" |tee -a $LOG_NAME
		echo $idle_type |tee -a $LOG_NAME
	else
		fail_msg Intel_idle |tee -a $LOG_NAME
		echo "#cat /sys/devices/system/cpu/cpuidle/current_driver" |tee -a $LOG_NAME
		echo $idle_type |tee -a $LOG_NAME
		
	fi
	
}

c_state()
{
	echo -e "\n##########  turbostat CHECK ##########" |tee -a $LOG_NAME
	echo " #cat /sys/devices/system/cpu/cpu0/cpuidle/state*/name" |tee -a $LOG_NAME
	cat /sys/devices/system/cpu/cpu0/cpuidle/state*/name |tee -a $LOG_NAME
	echo "#modprobe msr" |tee -a $LOG_NAME
	modprobe msr
	echo "#turbostat" |tee -a $LOG_NAME
	turbostat  |tee -a $LOG_NAME &
	#sleep 7 && kill -SIGINT $!
	sleep 7 && kill -9 $! &>/dev/null
	wait $! &>/dev/null
}

p_state_check()
{
	echo -e "\n##########  p_state CHECK ##########" |tee -a $LOG_NAME
	#echo "# cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_driver" |tee -a $LOG_NAME
	#cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_driver |tee -a $LOG_NAME
	p_state_type=`cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_driver|head -n 1`
	if [ "w$p_state_type" = "wintel_pstate" ]
	then
		pass_msg p_state |tee -a $LOG_NAME
		echo "#cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_driver|head -n 1" |tee -a $LOG_NAME
		echo $p_state_type |tee -a $LOG_NAME
	else
		fail_msg p_state |tee -a $LOG_NAME
		echo "#cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_driver|head -n 1" |tee -a $LOG_NAME
		echo $p_state_type |tee -a $LOG_NAME
	fi
		
}
powertop_check()
{
	echo -e "\n##########  powertop CHECK ##########" |tee -a $LOG_NAME
	#WR=`cat /etc/issue |sed -e '/^$/d'|awk '{print $1,$2}'`
	if [ "$OS_NAME" == "Wind River" ]
	then
		echo "powertop has installed !"
	else
		#OS_NAME=`lsb_release -i|awk '{print $3}'`
		case $OS_NAME in
		Ubuntu)
			echo "Ubuntu"
			echo "powertop ???"
		;;
		SUSE)   
			tar -mzxvf ./powertop-2.7.tar.gz &>/dev/null
			#chown -R root:root ./powertop-2.7
			> powertop.log
			if [ -f ./powertop-2.7/run.sh ];then echo "#./powertop-2.7/run.sh";./powertop-2.7/run.sh |tee -a $LOG_NAME; fi
			wait $! &> /dev/null
		;;
		RedHatEnterpriseClient)
			echo "RedHatEnterpriseClient"
			echo "powertop ???"
			
		;;
		*)
			echo "OS_NAME: $OS_NAME not found!"
		esac
	fi
	
}

oprofile_test()
{
	echo -e "\n##########  oprofile CHECK ##########" |tee -a $LOG_NAME
	operf -s &
	sleep 3 && kill -9 $! &> /dev/null
	wait $! &> /dev/null
	#echo -e "\n # opreport |grep CPU|grep Intel " |tee -a $LOG_NAME
	#opreport |grep CPU|grep Intel |tee -a $LOG_NAME
	echo -e "\n#opcontrol -l |head -n 1||opreport -l |head -n 1" |tee -a $LOG_NAME
	which opcontrol && opcontrol -l |head -n 1 |tee -a $LOG_NAME || which opreport && opreport -l |head -n 1 |tee -a $LOG_NAME
	
}
microcode_test()
{
	echo -e "\n##########  microcode CHECK ##########" |tee -a $LOG_NAME
	tar -mzxvf /root/test_data/microcode.tar.gz &> /dev/null
	cd /root/test_data/microcode
	./suse_run.sh |tee -a $LOG_NAME
	cd /root/test_data
}
early_microcode()
{
	echo -e "\n##########  early microcode CHECK ##########" |tee -a $LOG_NAME
	dmesg|grep -i "Microcode Update" |tee -a $LOG_NAME
}

cpu_online_offline()
{
	echo -e "\n##########  CPU Oneline Offline CHECK ##########" |tee -a $LOG_NAME
	dmesg -c &> /dev/null
	for i in 0 1
	do
		echo "#cat /sys/devices/system/cpu/cpu${i}/online" |tee -a $LOG_NAME
		cat /sys/devices/system/cpu/cpu${i}/online |tee -a $LOG_NAME
		echo "#echo 0 >/sys/devices/system/cpu/cpu${i}/online" |tee -a $LOG_NAME
		echo 0 >/sys/devices/system/cpu/cpu${i}/online |tee -a $LOG_NAME
		echo "#dmesg -c" |tee -a $LOG_NAME
		dmesg -c |tee -a $LOG_NAME
		echo |tee -a $LOG_NAME
		echo "#echo 1 >/sys/devices/system/cpu/cpu${i}/online" |tee -a $LOG_NAME
		echo 1 >/sys/devices/system/cpu/cpu$i/online |tee -a $LOG_NAME
		echo "#dmesg -c" |tee -a $LOG_NAME
		dmesg -c |tee -a $LOG_NAME
		echo  |tee -a $LOG_NAME
	done
}

modify_boot_param()
{
	add_param="cpu0_hotplug console=tty0 console=ttyS0,115200 "
	kernel_version=`uname -r`
	grub_dir=`find /boot -name grub.cfg|grep -v efi`
	if [ -f $grub_dir ]
	then 
		mod_line=`cat -n $grub_dir |grep ${kernel_version}|grep quiet|awk '{print $1}'|head -n 1`
		if [ -n $mod_line ]
		then
			sed -i "${mod_line}s/quiet/${add_param}/" $grub_dir
			echo "=============== boot param ===============" |tee -a $LOG_NAME
			cat -n $grub_dir |grep ${kernel_version} |tee -a $LOG_NAME
		else
			echo " quiet not found !"
		fi
	else
		echo "grub.cfg file not found!"
	fi
}

rapl_check()
{
	echo -e "\n##########  RAPL CHECK ##########" |tee -a $LOG_NAME
	if [ -f ./rapl/check_rapl.sh ];then echo "#./rapl/check_rapl.sh";./rapl/check_rapl.sh |tee -a $LOG_NAME; fi
}

rdrand_check()
{
	echo -e "\n##########  RDRAND CHECK ##########" |tee -a $LOG_NAME
	if [ -f ./rdrand/run.sh ];then echo "#./rdrand/run.sh";./rdrand/run.sh |tee -a $LOG_NAME; fi
}
cpu_flags_check()
{
	echo -e "\n##########  CPU FLAGES CHECK ##########" |tee -a $LOG_NAME
	if [ -f ./cpu_flag/cpu_flag_check_all.sh ];then echo "#./cpu_flag/cpu_flag_check_all.sh";./cpu_flag/cpu_flag_check_all.sh |tee -a $LOG_NAME; fi

}

main()
{
	echo "1:RedHatEnterpriseServer"
	echo "2:RedHatEnterpriseClient"
	echo "3:Ubuntu"
	echo "4:SUSE"
	echo "5:Wind River"
	echo "Which OS do you want to test ?"
	echo "please input you selected number."
	read NUM
	case $NUM in
	1)
		OS_NAME="RedHatEnterpriseServer"
	;;
	2)
		OS_NAME="RedHatEnterpriseClient"
	;;
	3)
		OS_NAME="Ubuntu"
	;;
	4)
		OS_NAME="SUSE"
	;;
	5)
		OS_NAME="Wind River"
	;;
	*)
		echo "$NUM is invalid !"
	esac
	
	echo "========  hostname  ======="
	echo `hostname`
	echo "Do you want to modify hostname?(y/n)"
	read DECIDE
	if [ "${DECIDE}" = "y" -o "${DECIDE}" = "Y" ]
	then
		echo "pease input your hostname."
		echo "#hostname "
		read HOST_NAME
		hostname $HOST_NAME
		if [ -f /etc/HOSTNAME ];then echo $HOST_NAME >/etc/HOSTNAME;fi
		if [ -f /etc/hostname ];then echo $HOST_NAME >/etc/hostname;fi
	fi
	if [ "${DECIDE}" = "n" -o "${DECIDE}" = "N"  ]
	then
		echo `hostname`
	fi
	LOG_NAME="/root/tmp_data/test_basic_`hostname`_`uname -r`.log"
	ls /root/tmp_data &>/dev/null || mkdir -p /root/tmp_data
	> $LOG_NAME
	dmesg >/root/tmp_data/dmesg

	modify_boot_param
	add_repofile
	bios_check
	dmesg_check
	devices_check
	network_check
	graphic_check
	audio_check	
	usb_check
	c_state
	p_state_check
	intel_idle_check
	oprofile_test
	#microcode_test
	early_microcode
	powertop_check
	rapl_check
	rdrand_check
	cpu_flags_check
	#cpu_online_offline
}
main


