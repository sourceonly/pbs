#!/usr/bin/python 
import sys
sys.path.append(scriptDir)
import pbs_tools
import RefreshUtils


opti_refresh=pbs_tools.RefreshModule( applicationArgs, refreshSourceName);

opti_refresh.create_platform();
opti_refresh.refresh_jobname();
