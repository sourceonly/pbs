#!/usr/bin/python
'''
	we use this hook to use 'mv' file , it would significally raise the performance while stagein and stageout are at same io devices , if you don't want to use move, then just delete mv line. 
	we want to this hook to executable as late as possible. set  default order to 10; 


	qmgr -c " c h  stage_hook" 
	qmgr -c " s h  stage_hook event=execjob_epilogue" 
	qmgr -c " i h  stage_hook application/x-python default stage_hook.py" 
	qmgr -c " s h  stage_hook order=10"
'''
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


	cmd=['su','-', str(j.Job_Owner).split('@')[0],'mv',j.jobdir+"/*",submit_local_dir];
	os.system(" ".join(cmd));
	
except:
	submit_dir=''


