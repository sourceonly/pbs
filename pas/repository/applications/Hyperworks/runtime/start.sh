#!/bin/bash
export LMX_LICENSE_PATH=6200@gn01
#export LMX_LICENSE_PATH=6200@192.168.40.68
export PATH=/opt/TurboVNC/bin/:$PATH
/opt/TurboVNC/bin/vncserver -noauth -geometry $PAS_GEOMETRY -noxstartup 2>vnc.log
DISPLAY=`cat vnc.log | grep Desktop | grep "started on" ` 
DISPLAY=${DISPLAY##*:}
echo `hostname`:$DISPLAY > vncid
export DISPLAY=`hostname`:$DISPLAY
gnome-wm &
#xclock 

export bgFlag=0


if [ $PAS_JOB_TYPE == 'hyperview' ] 
then 
	soft='hv'
elif [ $PAS_JOB_TYPE == 'hypermesh' ] 
then 
	soft='hm'
	job_script=`basename $JOB_SCRIPT`
	echo $job_script
	if [ -f $job_script ] 
	then 
		soft="$soft -tcl $job_script"
	fi
fi
vglclient --force &
vglrun -nodl +v  /data/apps/hw12.0/altair/scripts/${soft}










