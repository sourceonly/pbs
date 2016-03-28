import pbs_tools
import pattern

pt=pbs_tools.pbs_tools();
t=pt.table['job']
filter={}
filter['queue']=['iworkq','testq']
res_table={}
pattern=pattern.pattern();

for i in pattern.__enumerate__(t): 
	obj=t[i];
	res=pattern.__filter__(lambda x:pattern.dict_orvalue_filter(filter,x),obj)
	res_table=pattern.dict_acc(res_table,i,res);


print res_table.keys()
ncpus=0
def get_ncpus(key,obj): 
	if obj.has_key('Resource_List.ncpus'):
		return int(obj['Resource_List.ncpus'][0])
	return 0

for i in pattern.__enumerate__(t): 
	obj=t[i];
	res=pattern.__filter__(lambda x:pattern.dict_orvalue_filter(filter,x),obj)
	ncpus=pattern.__acc__(ncpus,lambda x,y:x+y,get_ncpus,i,res);

print ncpus
		





