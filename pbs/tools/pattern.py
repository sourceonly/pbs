



class pattern () : 
	def __init__(self): 
		self.type='or'	
		return 
	def set_pattern_type(self,type='or'): 
		self.type=type
	def __map__(self,table): 
		keys=table.keys();
		keys.sort();
		return keys
	def __filter__(self,obj,filter) : 
		for f_key in filter: 
			print f_key
			if not obj.has_key(f_key): 
				return {}
			else: 
				if self.type=='or':		
					if len(list(set(obj[f_key]+filter[f_key]))) == len(obj[f_key])+len(filter[f_key]): 
						return {}
				elif self.type=='and': 
					if len(list(set(obj[f_key]+filter[f_key]))) != len(obj[f_key]):
						return {}
		return	obj
	def __acc__(self,init_value,key,obj): 
		if obj== {} : 
			return;
		init_value[key]=obj
	
		
