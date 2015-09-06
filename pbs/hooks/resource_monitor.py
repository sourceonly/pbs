#!/usr/bin/python
import pbs
import os 
import sys 
sys.path+=['', '/opt/pbs/default/python/lib/python25.zip', '/opt/pbs/default/python/lib/python2.5', '/opt/pbs/default/python/lib/python2.5/plat-linux2', '/opt/pbs/default/python/lib/python2.5/lib-tk', '/opt/pbs/default/python/lib/python2.5/lib-dynload', '/opt/pbs/default/python/lib/python2.5/site-packages']
import subprocess
import re
	
	
class mom_info(): 
	def __init__(self):
		self.event=pbs.event();
		self.nodename=self.get_node_name();
		
	def get_node_name(self): 
		return self.event.vnode_list.keys()[0];

	def get_resource(self, resource_type,resource_name): 	
		return self.event.vnode_list[self.nodename].resources_available["ncpus"]
	def set_resource_available(self,resource_name,resource_value): 
		self.event.vnode_list[self.nodename].resources_available[resource_name]=resource_value;
		return resource_value;
	def get_cpu_info(self): 
		cpu_run=subprocess.Popen(['/usr/bin/top','-b','-n2','-d1'],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		out,err=cpu_run.communicate();
		reg_ex=re.compile("^Cpu\(s\):\s+([0-9\.]+)%us");
		res=[];
		for i in out.split('\n'): 
			reg_match=reg_ex.search(i); 
			if reg_match: 
				res+=reg_match.groups(1);	
		return res[-1];
		
	def get_mem_info(self): 
		mem_run=subprocess.Popen(['/usr/bin/free'],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		out,err=mem_run.communicate();
		reg_ex=re.compile("^Mem:");
		res=[];
		for i in out.split('\n'): 
			reg_match=reg_ex.search(i); 
			if reg_match: 
				return re.split('\s+',i.split(':')[1]);
		
			
mom=mom_info();

mom.set_resource_available("cpu_usage",mom.get_cpu_info());
mom.set_resource_available("mem_usage",mom.get_mem_info()[1]);
#mom.get_resource("resources_available","ncpus");





# import subprocess;

# node_map=pbs.event().vnode_list;
# node=node_map.keys()[0];


# #rc=subprocess.Popen(['/bin/df','-Plh'], shell=False, stdout=subprocess.PIPE);
# #out,err=rc.communicate();

# cpu_info=subprocess.Popen("/usr/bin/top -b -n 2 -d 1 |grep 'Cpu(s)' | tail -1 ",shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE);
# out,err=cpu_info.communicate();
# cpu_info=out.split(':')[1].split(',')[0].strip(' ');


# mem_info=subprocess.Popen("/usr/bin/top -b -n 2 -d 1 |grep 'Mem' | tail -1 ",shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE);
# out,err=mem_info.communicate();

# mem_info=out.split(':')[1].split(',')[2].split("free")[0].strip(" ");



# #cpu_info=out.strip(' ');
# #node_map[node].resources_available["pas_applications_enabled"]=usage


# node_map[node].resources_available["cpu_usage"]=cpu_info
# node_map[node].resources_available["mem_usage"]=mem_info

# #f=open("/tmp/test1","w");
# #f.write(node);
# #f.close




