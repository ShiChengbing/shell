#!/bin/bash


logname="/root/tmp_data/instrctions.log"

compare_speed()
{
	#for i in `seq 0 9`
	for i in 0 1
	do
	        grep -i "test  $i" /var/log/messages |sed 's/kernel:/#/g'|awk -F "#" '{print $2}'|tail -n 1 |tee -a $logname
	done
	#for i in `seq 10 21`
	for i in 20 21
	do
	        grep -i "test $i" /var/log/messages |sed 's/kernel:/#/g'|awk -F "#" '{print $2}'|tail -n 1 |tee -a $logname
	done	
}

boot_config_check()
{
	check_module=$1
	if [ -f /boot/config-$(uname -r) ]
	then
		#echo "#grep -i "${check_module}" /boot/config-$( uname -r )"
		grep -i "${check_module}" /boot/config-$( uname -r )
		module_other=`grep -o "${check_module}" /boot/config-$( uname -r )|head -n 1`
		if [ -z $module_other ];then echo "${check_module} is not set in config !";fi
	fi
	if [ -f /proc/config.gz ]
	then
		rm ./config
		cp /proc/config.gz ./
		gzip -d config.gz
		#echo "grep -i "${check_module}" ./config"
		grep -i "${check_module}" ./config
		module_wr=`grep -o "${check_module}" ./config|head -n 1`
		if [ -z $module_wr ];then echo ""${check_module}" is not set in config !";fi
fi
}



basepath=$(cd `dirname $0`;pwd)
cd $basepath

echo "Instrctions test at $( date +%T_%D )"
uname -a


ls /root/tmp_data || mkdir -p /root/tmp_data
> $logname

echo -e "\n###################     CRC32C  load    ##################" |tee -a $logname
echo '''#grep -i CONFIG_CRYPTO_CRC32C /boot/config-`uname -r`''' |tee -a $logname
#grep -i CONFIG_CRYPTO_CRC32C /boot/config-`uname -r` |tee -a $logname
boot_config_check CONFIG_CRYPTO_CRC32C
echo '''#modprobe crc32c_intel''' |tee -a $logname
modprobe crc32c_intel
echo '#modprobe tcrypt mode=319' |tee -a $logname
modprobe tcrypt mode=319  | tee -a $logname
compare_speed
echo -e "\n###################     CRC32C  unload    ##################" |tee -a $logname
echo '''#modprobe -r crc32c_intel ''' |tee -a $logname
modprobe -r crc32c_intel
echo '#modprobe tcrypt mode=319' |tee -a $logname
modprobe tcrypt mode=319  | tee -a $logname
compare_speed


echo -e "\n###################     CRCT10DIF  load    ##################" |tee -a $logname
echo '''#grep -i CONFIG_CRYPTO_crct10dif /boot/config-`uname -r`''' |tee -a $logname
#grep -i CONFIG_CRYPTO_crct10dif /boot/config-`uname -r` |tee -a $logname
boot_config_check CONFIG_CRYPTO_crct10dif
echo '#modprobe crct10dif_pclmul' |tee -a $logname
modprobe crct10dif_pclmul
echo '#modprobe tcrypt mode=320' |tee -a $logname
modprobe tcrypt mode=320 | tee -a $logname
compare_speed
echo -e "\n###################     CRCT10DIF unload    ##################" |tee -a $logname
echo '#modprobe -r crct10dif_pclmul ' |tee -a $logname
modprobe -r crct10dif_pclmul
echo '#modprobe tcrypt mode=320' |tee -a $logname
modprobe tcrypt mode=320  | tee -a $logname
compare_speed


echo -e "\n###################   SHA256 load    ##################" |tee -a $logname
echo '''#grep -i CONFIG_CRYPTO_SHA256  /boot/config-`uname -r`''' |tee -a $logname
#grep -i CONFIG_CRYPTO_SHA256  /boot/config-`uname -r` |tee -a $logname
boot_config_check CONFIG_CRYPTO_SHA256
echo '# modprobe sha256' |tee -a $logname
modprobe sha256
echo '#modprobe tcrypt mode=304' |tee -a $logname
modprobe tcrypt mode=304 | tee -a $logname
compare_speed
echo -e "\n###################   SHA256  unload    ##################" |tee -a $logname
echo '# modprobe -r sha256' |tee -a $logname
modprobe -r sha256
echo '#modprobe tcrypt mode=304' |tee -a $logname
modprobe tcrypt mode=304  | tee -a $logname
compare_speed


echo -e "\n###################   SHA512 load    ##################" |tee -a $logname
echo '''#grep -i CONFIG_CRYPTO_SHA512  /boot/config-`uname -r`''' |tee -a $logname
#grep -i CONFIG_CRYPTO_SHA512  /boot/config-`uname -r` |tee -a $logname
boot_config_check CONFIG_CRYPTO_SHA512
echo '#modprobe sha512' |tee -a $logname
modprobe sha512
echo '#modprobe tcrypt mode=306' |tee -a $logname
modprobe tcrypt mode=306 | tee -a $logname
compare_speed
echo -e "\n###################   SHA512  unload    ##################" |tee -a $logname
echo '#modprobe -r sha512' |tee -a $logname
modprobe -r sha512
echo '#modprobe tcrypt mode=306' |tee -a $logname
modprobe tcrypt mode=306  | tee -a $logname
compare_speed

echo -e "\n###################   movbe    ##################" |tee -a $logname
zypper in -y kernel-devel kernel-default-devel &>/dev/null
cat /usr/src/linux/include/linux/compiler-intel.h |grep -i "ifndef __HAVE_BUILTIN_BSWAP16__" -A5 |tee -a $logname


