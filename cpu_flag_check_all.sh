#!/bin/bash
#======================================================
#This script tested in the platform of SharkBay 
#Broadwell and Skylake 
#if met any problem please contact chengbingx.y.shi@intel.com
#
#=======================================================

basepath=$(cd `dirname $0`;pwd)
cd $basepath


hsw_features=("FMA" "MOVBE" "BMI1" "BMI2" "AVX2" "HLE" "INVPCID" "RTM")
bdw_client_features=("Rdseed" "smap" "adx" "3dnowprefetch")
bdw_server_features=("Rdseed" "smap" "adx" "3dnowprefetch" "hwp")
skl_client_features=("mpx" "xsavec" "xgetbv1" "xsaves")
skl_server_features=("clwb" "AVX512F" "clflushopt" "pcommit")



cpu_type()
{
        cpu_model=`grep "model" /proc/cpuinfo | sort | uniq | sed -e '/name/d' | awk -F ': ' '{ print $2 }'`
        cpu_family=`grep "cpu family" /proc/cpuinfo | sort | uniq | awk -F ': ' '{ print $2 }'`
        #return $cpu_model $cpu_family
}


flag_check()
{
features=($1)
counts=${#features[@]}

for i in `seq $counts`
do

        if [[ `cat /proc/cpuinfo|grep -i ${features[$i-1]}` ]]
        then
                echo "Pass:   The feature ${features[$i-1]} exposed in /proc/cpuinfo."
        else
                echo "Failed:   The feature ${features[$i-1]} is not exposed in /proc/cpuinfo. Please record it."
        fi

done


}

LZCNT()
{
	#The item LZCNT(ABM) should be a special.
	if [[ `cat /proc/cpuinfo|grep -i LZCNT` ]] || [[ `cat /proc/cpuinfo|grep -i ABM` ]]
	then
	        echo "Pass:   The feature \"LZCNT(ABM)\" exposed in /proc/cpuinfo."
	else
	        echo "Failed:   The feature \"LZCNT(ABM)\" is not exposed in /proc/cpuinfo. Please record it."
	fi
}


Server_check()
{
	cpu_type
	model=$cpu_model
	family=$cpu_family	
	case "${family}.${model}" in
	"6.58" | "6.60" | "6.62" | "6.63" | "6.69" | "6.70")  # Haswell
		echo "Haswell Server cpu flag check"
		echo "==============================="
		flag_check "${hsw_features[*]}"
		LZCNT
	;;
	"6.86" | "6.71" | "6.79")    # Broadwell
		echo "Broadwell Server cpu flag check"
		echo "==============================="
		flag_check "${bdw_server_features[*]}"
		LZCNT
        ;;
	"6.94") #skylake
		echo "Skylake Server cpu flag check"
		echo "==============================="
		flag_check "${skl_server_features[*]}"
	
	;;
	  *)
        echo Please help to add CPU model specific tests here!
        ;;
esac
}



Client_check()
{
	cpu_type
	model=$cpu_model
	family=$cpu_family	
	case "${family}.${model}" in
	"6.58" | "6.62" | "6.60" | "6.63" | "6.69" | "6.70")  # Haswell
		echo "Haswell Client cpu flag check"
		echo "==============================="
		flag_check "${hsw_features[*]}"
		LZCNT
	;;
	"6.61" | "6.86" | "6.71" | "6.79")    # Broadwell
		echo "Broadwell Client cpu flag check"
		echo "==============================="
		flag_check "${bdw_client_features[*]}"
		LZCNT
        ;;
	"6.94" | "6.78") #skylake
		echo "Skylake Client cpu flag check"
		echo "==============================="
		flag_check "${skl_client_features[*]}"
	;;
  	*)
        echo Please help to add CPU model specific tests here!
        ;;
esac
}


main()
{
Suse=`uname -r|grep -o 'default'`
Ubuntu=`uname -r|grep -o 'generic'`
Redhat=`uname -r|grep -o 'el7'`
Windriver=`uname -r|grep -o 'standard'`
#Windriver="standard"
#Ubuntu=""
echo "==============================="
echo "DATE:"`date +'%F %T'`
echo `uname -a`


if [ "@$Suse" = "@default" ]
then
	suse_type=`cat /etc/issue |sed -e '/^$/d'|awk '{print $6}'`
	case $suse_type in
	Desktop)
		echo "Suse client"
		Client_check
	;;
	Server)
		echo "Suse server"
		Server_check	
	;;
	*)
		echo "erro:Suse release unknow "
	esac

elif [ "@$Ubuntu" = "@generic" ]
then
	if [ -f /etc/init.d/lightdm ]
	then
		echo "Ubuntu client"
		Client_check
	else
		echo "Ubuntu server"
		Server_check
	fi	

elif [ "@$Redhat" = "@el7" ]
then
	red_type=`cat /etc/redhat-release |awk '{print $5}'`
	case $red_type in
	Client)
		echo "redhat client"
		Client_check
	;;
	Server)
		Server_check	
	;;
	*)
		echo "erro:Redhat release unknow "
	esac

elif [ "@$Windriver" = "@standard" ]
then
	echo
	echo "Usage for Windriver:"
	echo "================================================"
	echo "Notice: you will check cpu flag in windriver"
	echo "1) if you test Client platform please input [1] "
	echo "2) if you test Server platform please input [2] "
	echo "================================================"
	echo "Platform:"
	read windriver_type
	case $windriver_type in
	"1" | "client" | "Client" | "CLIENT")
		echo "windriver client"
		Client_check
	;;
	"2" | "server"|"Server" | "SERVER")
		echo "windriver server"
		Server_check	
	;;
	*)
		echo "erro:windriver release unknow "
	esac
else
	echo "error:[[[ OS Unkonw  ]]]"
fi

}


main


