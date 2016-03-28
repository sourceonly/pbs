



class pattern () : 
	def __init__(self): 
		self.type='or'	
		return 
	def __enumerate__(self,table): 
		keys=table.keys();
		keys.sort();
		return keys
	def __filter__(self,predict,obj): 
		return apply(predict,[obj])
	def indentity(self,obj): 
		return obj 
	def __acc__(self,init_value,op,trans,key,obj): 
		accer=apply(trans,(key,obj));
		return apply(op,(init_value,accer));
	
	def identity(self,key,obj): 
		return key,obj
	def add_to_dict(self,dict,pair): 
		if pair[1]=={}: 
			return dict
		dict[pair[0]]=pair[1]
		return dict
	def dict_acc(self,init_value,key,obj): 
		return apply(self.__acc__,(init_value, self.add_to_dict, self.identity, key, obj));
	
		
	def dict_orvalue_filter(self,dict_filter,obj): 
		for f_key in dict_filter: 
			if not obj.has_key(f_key): 
				return {}
			if len(list(set(obj[f_key]+dict_filter[f_key]))) == len(list(set(obj[f_key])))+len(list(set(dict_filter[f_key]))): 
				return {}
	
		return obj
	def dict_andvalue_filter(self,dict_filter,obj): 
		for f_key in dict_filter: 
			if not obj.has_key(f_key): 
				return {}
			if len(list(set(obj[f_key]+dict_filter[f_key]))) != len(list(set(obj[f_key]))):
				return {}
	
		return obj
		
