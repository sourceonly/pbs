#!/bin/bash
node_name=$1;
app_name=$2
. /etc/pbs.conf
export PATH=$PATH:$PBS_EXEC/bin
qmgr -c "s n $node_name resources_available.pas_applications_enabled=\"$app_name\""
