#!/bin/bash


kill_process_tree() {
curPid=$1
Pids="$curPid "
childPids=`ps -o pid --no-headers --ppid ${curPid}`
#echo "p $curPid has p(s) $childPids"
for childPid in $childPids
do
AA="$Pids $childPid"
cPids=`ps -o pid --no-headers --ppid ${childPid}`
#echo "p $childPid has p(s) $cPids"
#echo "$AA : $cPids"
Pids="$AA $cPids"
done
echo "kill -9 $Pids"
kill -9 $Pids 2> /dev/null
}


kill_process_tree $1

