#!/bin/bash


for confname in `ls ./4F_old`
do
	echo $confname 
	./vaconf_add.py ./4F_old/$confname
	#./vaconf_dump.py $confname
	
done
