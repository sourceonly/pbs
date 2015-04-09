#!/bin/bash 

# qlaunch.sh
#
# PBS Professional process launcher that utilizes the Task Manager interface
#
# For use ONLY inside of a PBS Professional job.  The qlaunch.sh command will spawn
# processes on nodes in the current job WITHOUT relying on rsh/ssh.  Any spawned
# process will be tracked by the pbs_mom under the proper job.
#
# When invoked with just a command to run, qlaunch.sh will use PBS_NODEFILE as the
# list of hosts.
#
# Options:
#
#  -o
#     Only run the specified command ONCE per host specified (as opposed to as
#     many times as that hostname appears in the list of hosts).
#
#  -u nodefile
#     Provide a list of the hosts to use in a file.  The hostnames can either be
#     one per line, or space seperated.
#
#  -z host_list
#     Provide a list of hosts to run on directly in the command.  This list can
#     either be a space seperated quoted string, or a comma seperated list
#     containing no spaces.  Examples:
#
#     qlaunch.sh -z "ecib01 ecib04" MySolver
#     qlaunch.sh -z ecib01,ecib04 MySolver
#
#  -n
#     Tells qlaunch.sh not to start the specified command in a shell on the
#     remote host.  WARNING: Using this option can have adverse effects on
#     error reporting and may cause problems if the command being run
#     depends on certain environmient variables/limits being in place.

if [ -z $PBS_ENVIRONMENT ] ; then
        echo "This command must be run from a PBS job only" 1>&2
        exit 2
fi

conf=${PBS_CONF_FILE:-/etc/pbs.conf}
. $conf

tmrsh=$PBS_EXEC/bin/pbs_tmrsh

launch_shell="/bin/sh -c "

while getopts "u:z:no" opt; do
        case $opt in
                u )
                optu=$OPTARG;;
                z )
                optz="$optz","$OPTARG";;
                n )
                launch_shell="";;
                o )
                once="true";;
                \? )
                echo "Usage: qlaunch.sh [options] <command>" 1>&2
                echo "see comments in script for options" 1>&2
                exit 1
        esac
done
shift $(($OPTIND - 1))

if [ -n "$optu" ] && [ -n "$optz" ] ; then
        echo "Both -u and -z options specified, ignoring -z" 1>&2
        unset optz
fi

if [ -n "$optz" ] ; then
        host_list=$(echo $optz | tr "," "\n")
elif [ -n "$optu" ] ; then
        host_list=$(cat $optu)
else
        host_list=$(cat $PBS_NODEFILE)
fi

if [ -n "$once" ] ; then
        sorted=$(echo $host_list | tr " " "\n" | sort | uniq)
        host_list=$sorted
fi

for host in $host_list ; do
        $tmrsh $host $launch_shell "$*"&
done
wait

