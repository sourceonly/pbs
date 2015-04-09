#!/usr/bin/python
# purpose: update job attributes if required
#
# the following objects are available during script execution:
# "job": PBS job which is ready for submission
# "userInputs": dictionary with all inputs from user
# "policies": dictionary with all policies as defined in AIF
# 

import time
import os
import sys

import aaa

job.attr_resource='select='+aaa.cpus

f=open("/tmp/test1","w")
for i in sys.path:
	f.write(i);
	f.write("\n");


print "Executing presubmit.py script for setting Account Name\n"

job.attr_accounting_label =  userInputs['JOB_ACCOUNT']
f=open("/tmp/test","w")
for i in dir(job):
	f.write(i);
	f.write("\n");
f.close()	

os.system("/bin/sleep 6s");

sys.stdout.flush()

