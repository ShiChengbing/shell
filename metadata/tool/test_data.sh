#!/bin/bash

data_dir='/var/lib/mysql/'
echo -n "Enter database name:"   
read  databasename   

#******************************** 

dataif=`sudo ls $data_dir |grep $databasename`
if [ -z $dataif ]
then
	echo " Database does not exist ! "
	mysql -u$username -p$password -e" create database $databasename;"
else
	echo " Database is exist !"
fi


