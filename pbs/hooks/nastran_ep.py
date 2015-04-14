#!/usr/bin/python 

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

	
			


