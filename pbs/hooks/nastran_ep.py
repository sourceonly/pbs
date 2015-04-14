#!/usr/bin/python 
'''
This hook used to terminate hooks with Nastran jobs ( qsub -l software=Nastran ) 
if a nastran job failed, it only keeps the solver deck 'bdf' file , 'f04' and 'f06' for details,  and remove other temp file in the solver to save time 

default order of this hook is 1

if you want to keep more files with failed nastran jobs, please add extra file extentions to  reserve_ext 
please follow those step to take effect
	qmgr -c " c h nastran_ep" 
	qmgr -c " s h nastran_ep event=execjob_epilogue" 
	qmgr -c " i h nastran_ep application/x-python default nastran_ep.py"
'''
import os 
import sys
import pbs 

j=pbs.event().job
j_query=pbs.server().job(j.id);


soft=j_query.Resource_List["software"].__str__();


if not soft == 'Nastran' : 
	sys.exit(0);
	

reserve_ext=['f04','f06','bdf'];

j_id=j.id.split(".")[0];
reserve_ext.append("o"+j_id);
reserve_ext.append("e"+j_id);

if j.Exit_status!=0 : 
	job_dir=j.jobdir;
	for root,dirs,files in os.walk(job_dir): 
		for f in files: 
			ext=f.split(".")[-1];
			if not ext in reserve_ext: 
				os.remove(root+"/"+f);

	
			


