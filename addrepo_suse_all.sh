#!/bin/bash


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
for i in `ls /mnt/iso |grep -i ".iso"` 
do 
	iso=$i  
	echo "zypper ar iso:///?iso=/mnt/iso/$iso $i"
	zypper ar iso:///?iso=/mnt/iso/$iso $i

done
zypper refresh
