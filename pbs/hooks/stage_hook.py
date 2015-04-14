#!/usr/bin/python
import os
import pbs 
#import subprocess
import sys


e=pbs.event();
j=e.job;

stageout_list=j.stageout._value


try: 
	submit_dir=j.Variable_List['PAS_SUBMISSION_DIRECTORY']
	submit_list=submit_dir.split("/");
	submit_host=submit_list[2];
	submit_list[2]='';
	del(submit_list[0]);
	del(submit_list[0]);
	submit_local_dir='/'.join(submit_list);


	mkdir_cmd=['su', '-' , str(j.Job_Owner).split('@')[0], "-c", '"mkdir -p ' + submit_local_dir + '"' ];
	os.system(" ".join(mkdir_cmd));


	cmd=['mv',j.jobdir+"/*",submit_local_dir];
	os.system(" ".join(cmd));
	
except:
	submit_dir=''


