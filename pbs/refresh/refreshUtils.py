#!/usr/bin/python

import subprocess;



class refreshUtils:
	def __init__ (self): 
		pbs_config_file="/etc/pbs.conf"
		pbs_env={};
	def run_cmd (self, cmd) : 
		res=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE);
		res.communicate();
		return res.stdout.read();
	


	
