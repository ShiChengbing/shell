#!/bin/bash

for confname in `ls /apps_root/env_setup/4F/`
do
	echo 4F $confname 
        ./vaconf_dump.py 4F $confname

done
