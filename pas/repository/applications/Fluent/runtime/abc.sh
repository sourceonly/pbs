#!/bin/bash
#PBS_JOBID=22.ee
export TERM=xterm
export PATH=/app/vnc/TurboVNC/bin:$PATH
. /etc/X11/xorg.conf
vncserver -noauth -noxstartup 2>${PBS_JOBID}.vnc
#vncserver -auth 2>err
VNCHOST=`hostname`
vncid=`cat ${PBS_JOBID}.vnc|grep "desktop is $VNCHOST"|awk -F":" '{print $2}'`
echo $VNCHOST":"$vncid >vncid
export DISPLAY=$VNCHOST":"$vncid
rm -f ${PBS_JOBID}.vnc
cpus=`expr $AIF_HOSTS \* $AIF_CORES`
[ -n "$JOURNAL" ] && JOURNAL="-i $JOURNAL"
#sleep 10000
$AIF_EXECUTABLE 3d -t${cpus} -cnf=$PBS_NODEFILE $JOURNAL
exit 0
