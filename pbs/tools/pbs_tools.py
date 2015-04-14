#!/usr/bin/python 


import sys;
import os;
import subprocess
import re;
try: 
	import RefreshUtils
except: 	
	pass

class pbs_tools(): 
	def __init__ (self):
		self.set_pbs_env;	
		self.table={};
		self.table['pbsnodes']=self.get_node_table();
		self.sep=';'
		self.pestat_default=['Mom','state','resources_available.pas_applications_enabled','resources_available.platform','resources_available.ncpus','resources_assigned.ncpus','resources_available.mem','resources_assigned.mem','jobs']
		self.jobinfo_default=['Job_Name','Job_Owner']
		self.table['job']=self.get_job_table();
                self.table['platform']=self.get_platform_table();

                
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
		
	def qstat(self, args='-f') : 
		cmd=['qstat', args];
		qstat_task=subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE);
		qstat_out,qstat_err=qstat_task.communicate();
		cl_reg=re.compile("\n\t");
		qstat_out_2=cl_reg.sub("",qstat_out);
		return qstat_out_2,qstat_err
		
	def get_node_table(self): 
		pbs_nodes_table={}
		current_host='';
		output,error=self.pbsnodes();
		host_reg=re.compile("^[A-Za-z0-9_\-]+");
		res_reg=re.compile("\s+([^=]+)=([^=]+)");
		for i in output.split('\n'):
			if not i : 
				continue
			host_match=host_reg.search(i);	
			if host_match: 
				current_host=host_match.group(0);
				pbs_nodes_table[current_host]={};
			res_match=res_reg.search(i.strip('\n'));

			if res_match : 
				if not (current_host == "" ) :
					key=res_match.group(1).strip(' ');
					value=res_match.group(2).strip(' ').split(',');
					pbs_nodes_table[current_host][key]=value;
		return pbs_nodes_table;
					
	def pestat (self):
		keylist=self.pestat_default; 
		short=self.table['pbsnodes'];
		content=''
		for i in short.keys():
			for j in keylist: 
				if short[i].has_key(j):	
					content+=','.join(short[i][j])+self.sep;
				else: 
					content+='-'+self.sep
			content+='\n'
		print content
		return ;
	def get_job_table (self,args='-f'): 
		qstat_f={};
		jobid_reg=re.compile("^Job Id");
		res_reg=re.compile("\s+([^=]+)=(.+)");
		qstat_out,qstat_err=self.qstat(args);
		current_id="";
		for i in qstat_out.split('\n'):
			id_match=jobid_reg.search(i);
			if id_match: 
				jobid=i.split(':')[-1].strip(' ');	
				qstat_f[jobid]={};
				current_jobid=jobid
			res_match=res_reg.search(i.strip('\n'));
			if res_match:
				if not (current_jobid == "") :
					key=res_match.group(1).strip(' ');
					value=res_match.group(2).strip(' ').split(',');
					qstat_f[current_jobid][key]=value;
		return qstat_f
	def get_platform_table(self): 
		node_table=self.table['pbsnodes'];
                platform={};
                for i in node_table.keys():
                        if not node_table[i].has_key("resources_available.platform"):
                                continue
                        
                        for j in node_table[i]["resources_available.platform"]:
                                if not platform.has_key(j):

                                        platform[j]={};
                                        platform[j]['total']=0;
                                        platform[j]['used']=0;
                                        platform[j]['free']=0;

                                if node_table[i].has_key("resources_available.ncpus"):
                                        node_cpu_total=int(node_table[i]["resources_available.ncpus"][0]);
                                else :
                                        node_cpu_total=0;
                                if node_table[i].has_key("resources_assigned.ncpus"):
                                        node_cpu_assign=int(node_table[i]["resources_assigned.ncpus"][0]);
                                else :
                                        node_cpu_assign=0;
                                                
                                platform[j]['total']+=node_cpu_total;
                                platform[j]['used']+=node_cpu_assign;
                                #platform[j]['free']+=platform[j]['total']-platform[j]['used'];
                                platform[j]['free']+=node_cpu_total-node_cpu_assign;

                                       


                return platform

	def get_app_platform(self, apps, match_key="resources_available.pas_applications_enabled", platform_key="resources_available.platform"): 
		table=self.table['pbsnodes']; 
		platform_list=[];
		for node in table.keys() : 
			if table[node].has_key(match_key) : 
				if apps in table[node][match_key]: 
					if table[node].has_key(platform_key): 
						platform_list+=table[node][platform_key];
		return list(set(platform_list));
	def get_platform_status (self, list=[] ): 
		platform_list=self.table['platform'];
		if len(list)==0: 
			list=platform_list.keys();
		valid_keys=[ var for var in list if var in platform_list.keys()	] ;
		platform_info=[];
		for key in valid_keys :  
			platform_string="%-20s ( used: %6d | free: %6d | total: %6d ) "	 % ( key, platform_list[key]['used'],platform_list[key]['free'], platform_list[key]['total'])
			platform_info.append(platform_string);
		return platform_info;
			
		
				

class RefreshModule() : 
	def __init__ (self, applicationArgs, refreshSourceName) :  
		self.applicationArgs=applicationArgs;
		self.refreshSourceName=refreshSourceName;
		return 
        def create_platform (self,apps='Optistruct',platform='PLATFORM') :
		if self.refreshSourceName != platform : 
			return None
                Debug = True
                if (Debug == True):
                        refreshUtils = RefreshUtils.RefreshUtils(self.applicationArgs, self.refreshSourceName, Debug)
                        
                else:
                        refreshUtils = RefreshUtils.RefreshUtils(self.applicationArgs, self.refreshSourceName)
                        
                try:
                        refreshUtils.deleteApplicationArg(platform);
                except:
                        pass

                A=pbs_tools();
                available_platform=A.get_app_platform(apps);
                options=A.get_platform_status(available_platform); 
		if len(options) > 0 : 
                	newArg = refreshUtils.createArgumentStringEnum(platform, options,  options[0], options[0], platform, platform, True, True)
                	refreshUtils.addApplicationArg(newArg, 3);
			return newArg
                return None;
	def strip_platform(self,string) : 
		reg_platform=re.compile("[A-Za-z0-9\-]+");
		reg_match=reg_platform.search(string);
		if reg_match: 
			return reg_match.group(0);	
		return None;

	def refresh_jobname(self,jobname='JOB_NAME',file='MASTER'):  
                Debug = True
                if (Debug == True):
                        refreshUtils = RefreshUtils.RefreshUtils(self.applicationArgs, self.refreshSourceName, Debug)
                        
                else:
                        refreshUtils = RefreshUtils.RefreshUtils(self.applicationArgs, self.refreshSourceName)
                        
		if not self.refreshSourceName == file: 
			return ;
		
		job_name=refreshUtils.getValue(jobname);
		if job_name  : 	
			return 
		master_list=refreshUtils.getValue(file).split("/")[-1].split(".")
		if len(master_list[0]) > 0  : 
			master=master_list[0]
		else : 
			master=re.sub(r"\.","_","_".join(master_list));
	
		job_name_node=self.get_node(jobname);
		if job_name_node : 
			job_name_node.setValue(master);
		
	def get_node (self, nodename) : 
		for i in self.applicationArgs: 
			if i.name == nodename : 
				return i;
	
			
class license():
        def __init__ (self) :
                self.lmstat='/usr/local/bin/lmstat'
                self.lmxendutils='/usr/local/bin/lmxutils'
        def check_lm_lic(self, target) :
                pass
