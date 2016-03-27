import pbs_tools

import pattern

pt=pbs_tools.pbs_tools();

t=pt.table['job']
filter={}
filter['Job_Name']=['aa','Hyperworks','STDIN']
filter['queue']=['iworkq','workq']
res_table={}
pattern=pattern.pattern();

#for i in pattern.__map__(t): 
#	obj=t[i];
#	res=pattern.__filter__(obj,filter);
#	pattern.__acc__(res_table,i,res);

#a=res_table.keys()
#a.sort()
#print a
	


node_table={}
n=pt.table['pbsnodes']
n_filter={}
n_filter['resources_available.pas_applications_enabled']=['Optistruct']
for j in pattern.__map__(n): 
	obj=n[j]
	res=pattern.__filter__(obj,n_filter);
	pattern.__acc__(node_table,j,res);

a=node_table.keys()
a.sort()
print a
