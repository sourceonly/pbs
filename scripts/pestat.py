#!/usr/bin/python
import sys
import os

cmd=sys.argv[0];
cmd_dir=os.path.dirname(cmd);
sys.path+=[cmd_dir];


import pbs_tools

pestat=pbs_tools.pbs_tools();
print "mom,platform,applications,state,mem,mem_usage,disk_usage,cpu_usage,ncpus,assign_ncpus,jobs"
pestat.set_pestatf(['Mom','resources_available.platform','resources_available.pas_applications_enabled','state','resources_available.mem','resources_available.mem_usage','resources_available.disk_usage','resources_available.cpu_usage','resources_available.ncpus','resources_assigned.ncpus','jobs'])
pestat.pestat()
