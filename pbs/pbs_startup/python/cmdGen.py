#!/usr/bin/python
'''

'''


import shlex
import re
import subprocess
class cmdGen: 
	def __init__(self):
		self.data_table={};
		self.template=[];
		
	def update_data_table(self,key,value): 
		self.data_table[key]=value;
	def update_template(self,template_list): 
		self.template=template_list;
	def convert_argv(self,argv): 
		pass;


	def strip_argv(self,argv): 
		if self.is_argv_optional(argv):
			return argv[1:];
		return argv;
	def is_argv_optional(self,argv): 
		if argv[0]=='?': 
			return True;
		return False

	def symbol_sub (self,argv, dict): 
		re_symbol=re.compile("@([A-Za-z\-_\+]+)@"); 
		symbol_match=True
		while (symbol_match) : 
			symbol_match=re_symbol.search(argv)
			if symbol_match: 
				key=symbol_match.group(1);
				if not dict.has_key(key): 
					if self.is_argv_optional(argv): 
						return '' ;
					break
				re_this=re.compile("@"+key+"@")
				argv=re.sub(re_this,dict[key],argv)
					
		return self.strip_argv(argv)
		
	def symbol_replace(self,argv):
		return self.symbol_sub(argv,self.data_table);

	def list_sub(self,list): 
		for i in range(len(list)): 	
			list[i]=self.symbol_replace(list[i]);
		
		return shlex.split(" ".join(list));

	def cmd_gen(self): 
		return self.list_sub(self.template);

					
	
'''
b=cmdGen();
a={}

a['EXEC']="AAA"
a['CPU']="ABC"
print b.list_sub(['@EXEC@','-cpu @CPU@','?-len @MEM@'])

'''
