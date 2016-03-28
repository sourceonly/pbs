import pbs_tools
import pattern
import os
class snapshot(): 
	def __init__(self): 
		tools=pbs_tools.pbs_tools()
		self.job_table=tools.table['job'];
		self.node_table=tools.table['pbsnodes'];
		self.init_job_filter();	
		self.init_node_filter();
		self.pattern=pattern.pattern();
	def init_job_filter(self): 
		self.job_filter={}
		self.job_filter['queue']=['iworkq']
			
	def set_job_filter (self,dict) :
		self.job_filter={};
		self.job_filter=dict;

	def init_node_filter(self): 
		self.node_filter={}
	def set_node_filter(self,dict): 
		self.job_filter=dict

	
	def safe_get_int_key(self,keyname,node_obj):
		if node_obj.has_key(keyname): 
			return int(node_obj[keyname][0]);
		return 0
	def safe_get_string_list(self,keyname,node_obj): 	
		if node_obj.has_key(keyname): 
			return node_obj[keyname];
		return ['']
	def get_filted_job(self): 
		t=self.job_table
		res_table={};
		filter=self.job_filter;
		pattern1=self.pattern;
		for i in pattern1.__enumerate__(t):
        		obj=t[i];
        		res=pattern1.__filter__(lambda x:pattern1.dict_orvalue_filter(filter,x),obj)
        		res_table=pattern1.dict_acc(res_table,i,res);
		return res_table	
	
	def get_filted_node(self): 
		t=self.node_table
		res_table={};
		filter=self.node_filter;
		pattern1=self.pattern;
		for i in pattern1.__enumerate__(t):
        		obj=t[i];
        		res=pattern1.__filter__(lambda x:pattern1.dict_orvalue_filter(filter,x),obj)
        		res_table=pattern1.dict_acc(res_table,i,res);
		return res_table	
		
	def get_node_obj_free_cpus(self,key,node_obj): 
		if node_obj.has_key('resources_available.ncpus'):
               		return int(node_obj['resources_available.ncpus'][0])
	       	return 0
	def get_node_free_cpus(self):
		t=self.node_table	
		pattern1=self.pattern
		filter=self.node_filter
		ncpus=0
		for i in pattern1.__enumerate__(t): 
			obj=t[i];
	       		res=pattern1.__filter__(lambda x:pattern1.dict_orvalue_filter(filter,x),obj)
			ncpus=pattern1.__acc__(ncpus,lambda x,y:x+y,self.get_node_obj_free_cpus,i,res);
		return ncpus
	
					
				
import time
import gc;
import subprocess

class sched(): 
	def __init__(self): 
		self.sched_cycle=10;
		self.orig_queue=['workq'] 
		self.dest_queue=['iworkq']
		self.init_snap()
	def init_snap(self): 
		self.snapshot=snapshot();
		node_filter={};
		node_filter['queue']=self.dest_queue;
		self.snapshot.node_filter=node_filter
		job_filter={};
		job_filter['queue']=self.orig_queue
		job_filter['job_state']=['Q']
		self.snapshot.job_filter=job_filter	
			
				
	def move_job(self,destination,jobid): 
		os.system('qmove ' + destination + ' ' + jobid);
		time.sleep(1);
		self.init_snap();
	
	def do_sched(self):
		snap=self.snapshot 
		to_deliver=self.snapshot.get_filted_job()
		list_job=to_deliver.keys()
		list_job.sort() 
		print list_job
		job_to_d=list_job.pop(5);
		print job_to_d
		
		cpu_req=self.snapshot.safe_get_int_key("Resource_List.ncpus",to_deliver[job_to_d])
		
		cpu_free=self.snapshot.get_node_free_cpus()
		
		print cpu_req,cpu_free
				
		self.move_job(self.dest_queue[0],job_to_d)
				
		pass
	def main_loop(self):	
		while True: 
			self.do_sched();
			time.sleep(self.sched_cycle)
			gc.collect()
				
