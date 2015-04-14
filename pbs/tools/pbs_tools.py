#!/usr/bin/python 


import sys;
import os;
import subprocess
import re;



class pbs_tools(): 
	def __init__ (self):
		self.set_pbs_env;	
		self.pbsnodes_table=self.get_node_table();
		self.sep=';'
	def set_pbs_env(self):
		f=open("/etc/pbs.conf","w");
		for i in f.readlines(): 
			pair=i.split("=");
			os.environ[pair[0]]=pair[1];
		os.environ['PATH']=os.environ['PBS_EXEC']+"bin:"+os.environ['PATH'];
	def pbsnodes (self, args='-av'): 
		cmd=['pbsnodes' , args];
		pbsnodes_task=subprocess.Popen(cmd,shell=False, stdout=subprocess.PIPE);
		pbs_node_out,pbs_node_err=pbsnodes_task.communicate();
		return pbs_node_out,pbs_node_err
		
	def get_node_table(self): 
		pbs_nodes_table={}
		current_host='';
		output,error=self.pbsnodes();
		for i in output.split('\n'):
			if not i : 
				continue
			host_reg=re.compile("^[A-Za-z0-9]+");
			host_match=host_reg.search(i);	
			if host_match: 
				current_host=host_match.group(0);
				pbs_nodes_table[current_host]={};
			res_reg=re.compile("\s+([^=]+)=([^=]+)");
			res_match=res_reg.search(i.strip('\n'));

			if res_match : 
				if not (current_host == "" ) :
					key=res_match.group(1);
					value=res_match.group(2).strip(' ').split(',');
					pbs_nodes_table[current_host][key]=value;
		return pbs_nodes_table;
				
			
		
