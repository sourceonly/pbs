#!/usr/bin/python




import re
import os
import sys
import subprocess
class taskManage():
    def __init__ (self):
        self.para={};
        self.snapshot={};
        self.rc=1;
        self.history=[];
    
    def spawn_cmd (self, cmd):
        self.history.append(" ".join(cmd));
	ptask=subprocess.Popen(cmd,shell=False);
	self.pid=ptask.pid
	if bg == False : 
            ptask.communicate();
            self.rc=ptask.returncode
        
	return ptask.returncode;
    def get_cmd_result(self,cmd): 
        ptask=subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE)
        return ptask.communicate();
 
    


		
        
        
        
