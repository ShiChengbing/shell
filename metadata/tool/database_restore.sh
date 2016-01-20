#!/bin/bash

backup_dir="/home/labadmin/mysql_backups"

echo -n "Enter username name:"   
read  username   
echo -n "Enter password name:"   
read  password   
echo -n "Enter database name:"   
read  databasename   

#******************************** 

if [ -f $databasename.sql ]
then
	echo "hello $username,welcome to database restore program" 
	echo "The restore program is running"
	dataif=`sudo ls /var/lib/mysql/ |grep $databasename`
	if [ -z $dataif ]
	then
		echo " Database does not exist ! "
		mysql -u$username -p$password -e" create database $databasename;"
		mysqldump -u$username -p$password  < $backup_dir/$databasename.sql
	else
		echo " Database is exist ! "
		mysqldump -u$username -p$password  < $backup_dir/$databasename.sql
	fi
	echo "database restore is complete!"
else
	echo "Do not find $databasename.sql file in the $backup_dir directory"
fi


