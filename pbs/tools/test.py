#!/usr/bin/python


import pbs_tools
A=pbs_tools.pbs_tools();


#print A.get_app_platform("Optistruct")
#p=A.get_node_table();
#print p
#a,b=A.pbsnodes();
#print a




#A.pestat()
#print A.table['user_project']
#print A.job_table()
#print A.qstat()
#print A.table['pbsnodes']
#print A.table['platform']

#platform=A.get_app_platform("Optistruct")



#print A.get_platform_status(platform);


#B=pbs_tools.RefreshModule('a','b');

#print B.strip_platform(A.get_platform_status(platform)[0]);

#print A.pbsnodes_table


#print a[0]

#print A.table['queue']
print A.get_user_queue('test1')

