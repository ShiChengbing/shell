#!/bin/bash

rm f10_od_conf.txt
echo `date '+ %F %T'`
./od_data_f10.py 20131008143000 20131008153000 30 10 f10_line_list
echo `date '+ %F %T'`
