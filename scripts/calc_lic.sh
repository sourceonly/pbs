#!/bin/sh
# author: Wang Yihua [wangyihua@altair.com.cn]
# date:09:20 2012-9-2
# version:2.1
# purpose: return the license feature infomation and available token
if [ $# -lt 1 ]
then
echo "Example: calc_lic.sh star [ccmppower|ccmpsuite]
star: ccmppower|ccmpsuite|starpar|starsuite|hpcdomains
ansys: ansys|acfd_fluent|anshpc|mechhpc
esi: CRASHSAF_SMP_BASE|vaone_sea|sysweld|sysweld.linux86.sp
msc: CAMPUS|MD_NASTRAN|MDAdv|NASTRAN
nxnastran: nx_nas_basic_ent
madymo: MADYMO-Token
altair: GridWorks
altair11: HyperWorks
altair12: HyperWorks
exa: ExaSIM
amls: omp
avl: cfd_mpi|cfd_solver
abaqus: abaqus|standard"
exit 1
fi
exe=/usr/local/bin/lmutil
exe2=/usr/local/bin/lmxendutil
exe3=/usr/local/bin/lstc_qrun
lic_server=gn01
lic_server2=pbsserver
lic_server3=192.168.40.67
lic_server4=jacpbs
lic_server5=jachpc5
case $1 in
    star)  server=1999@$lic_server ;;
    ansys) server=1055@$lic_server2 ;;
    msc) server=27500@$lic_server4 ;;
    msc2) server=27500@$lic_server5 ;;
    nxnastran) server=28000@$lic_server4 ;;
    madymo) server=26000@$lic_server2 ;;
    abaqus)  server=27000@$lic_server2 ;;
    altair)  server=7788@$lic_server3 ;;
    altair11)  server=6200@$lic_server3 ;;
    altair12)  server=6200@$lic_server ;;
    esi)  server=7789@$lic_server ;;
    amls)  server=27000@$lic_server5 ;;
    primer)  server=27000@$lic_server7 ;;
    femzip)  server=27001@$lic_server7 ;;
    lsdyna)  server=$lic_server
		total_dyna=104 ;;
    star)  server=1999@$lic_server8 ;;
    avl)  server=27001@$lic_server3 ;;
    *)  echo "$1 is Invalid license!"
	exit 1 ;;

esac
if [ $# = 1 ];
then
        case $1 in
        altair11|altair12)   server=`echo $server|awk -F@ '{print $2}'`
		$exe2 -licstat -host $server ;;
        lsdyna)   export LSTC_LICENSE_SERVER=$server
		  export LSTC_LICENSE=network
		  used_dyna=`calc_lic.sh lsdyna lsdyna`
		  used_percent=`gawk -v x=$used_dyna -v y=$total_dyna 'BEGIN{printf "%.2f%%",x*100/y}'`
		$exe3 
		  printf '=========================\n'
		  printf '%5i %4s %4i %8s %12s %8s %4s (%5s) \n' $used_dyna of $total_dyna Total Dyna License Used $used_percent
		  printf '=========================\n' ;;
        nxnastran) $exe lmstat -c $server -f nx_nas_basic_ent ;; 
        abaqus) $exe lmstat -c $server -f abaqus ;; 
#        msc) $exe lmstat -c $server - ;; 
        *)      $exe lmstat -c $server -a ;;
        esac
else
        case $1 in
        altair11|altair12)  server=`echo $server|awk -F@ '{print $2}'`
		   $exe2 -licstat -host $server>/tmp/$$_log
		altair11_total=`cat /tmp/$$_log|grep "Feature: HyperWorks" -A5|grep "license(s) used"|awk '{print $3}'`
		avail_token=`cat /tmp/$$_log|grep " of $altair11_total license(s) used:"|awk  '{avail=($3 - $1)/10}END{print avail}'`
                if [ "$avail_token" == "" ]; then
                avail_token=$altair11_total
                else avail_token=$avail_token
                fi
		   rm -f /tmp/$$_log
                echo $avail_token ;;
        lsdyna) export LSTC_LICENSE_SERVER=$server
		export LSTC_LICENSE=network
		 LSTC_SECURITY_DIR=/stage/apps/lsdyna/license
		 DYNAPATH=/stage/apps/lsdyna/license
		export LSTC_SECURITY_DIR
		tmpF=/tmp/dynalic$$
		lstc_qrun > $tmpF 2>/dev/null
		isRunning=`grep -q 'No programs running' $tmpF && echo 0 || echo 1`
		if [ $isRunning -eq 0 ] ; then 
		rm -rf $tmpF
		echo $[$total_dyna*1] 
		exit 0
		fi
		isQueued=`grep -q 'No programs queued' $tmpF && echo 0 || echo 1`

		case $isQueued in
		0)	lstLength=`wc -l $tmpF | awk '{print $1}'`
			lstLength=$[$lstLength-1] ;;
		1)	lstLength=`nl -ba $tmpF | grep "Queued Programs" | awk '{print $1}'`
			lstLength=$[$lstLength-3] ;;
		esac
		usedt=`nl -ba $tmpF | sed -n "7,$lstLength""p" | cut -c 76- | awk '{tokns+=$1}END{print tokns}'`
		norm1=$[$total_dyna-$usedt]
		rm -rf $tmpF
		#norm1=$[$norm1*1]
		echo $norm1  ;;
        *)      feature=$2
                $exe lmstat -c $server -f $feature |grep "Users of $feature" |awk '{avail=$6 - $11}END{print avail}' ;;
        esac
fi



