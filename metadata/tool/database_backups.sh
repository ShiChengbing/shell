#!/bin/bash

backup_dir="/home/labadmin/mysql_backups"
echo -n "Enter username name:"   
read  username   
echo -n "Enter password name:"   
read  password   
echo -n "Enter database name:"   
read  databasename   


echo "hello $username,welcome to database backups program" 
echo "The restore program is running"

#******************************** 
mkdir -p $backup_dir
mysqldump -u$username -p$password $databasename > $backup_dir/$databasename.sql


