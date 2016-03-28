import pbs_tools
import pattern


class snapshot(): 
	def __init__(self): 
		tools=pbs_tools.pbs_tools()
		self.job_table=tools.table['job'];
		self.node_table=tools.table['pbsnodes'];
	
	
	

import time
import gc;
class sched(): 
	def __init__(self): 
		self.sched_cycle=10;
		self.snapshot=snapshot();	
	def do_sched(self): 
		pass
	def main_loop(self):	
		while True: 
			self.do_sched();
			time.sleep(self.sched_cycle)
			gc.collect()
				
		
		
