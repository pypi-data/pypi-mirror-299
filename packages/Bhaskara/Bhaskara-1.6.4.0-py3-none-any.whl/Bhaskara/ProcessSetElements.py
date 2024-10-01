from StringAlgorithm.ConditionSplit import condition_split

def process_logic_element(compiler,line,scope='global',scope_name='') :
	
	element = '∈'
	not_element = '∉'
	
	if  element in line :
		if type(line) == type('a') :
			line = line.split()
		
		# a1 ∈ S
		#a[i] ∈ S // this mean i_th element of set S is assigned to variable a
		name = ""
		index = ""
		
		variable = line[0]
		set = line[2]
		has_bracket = False
		
		for char in variable :
		 	 if char == ']' :
		 	 	break
		 	 if char == '[' :
		 	 	has_bracket = True
		 	 	continue
		 	 if has_bracket :
		 	 	index += char
		 	 	continue
		 	 if char in compiler.alpha :
		 	 	name += char
		 	 elif char in compiler.int_literals :
		 	 	index += char
		
		if has_bracket :
			if len(condition_split(index,'any')) > 1 :
				index = compiler.compute_index(index,scope=scope,scope_name=scope_name)
			elif compiler.check_variable_name(index) :
				index = compiler.fetch_var_value(index,scope=scope,scope_name=scope_name)
		
		index = int(index)
		#fetching element at a given index 
		value = compiler.get_arr_element(set,index,scope=scope,scope_name=scope_name)
		#fetching data type of the set
		_,data_type = compiler.fetch_variable(set,scope=scope,scope_name=scope_name)
		
		dt  = ""
		#int_arr
		#int
		for char in data_type :
			if char == '_' :
				break
			dt += char
		data_type = dt
		del dt
		
		if compiler.is_variable_in_scope(name,scope=scope,scope_name=scope_name) :
			compiler.assign_value(name,value,scope=scope,scope_name=scope_name)
			return
		
		compiler.define_variable(name,value,data_type,scope=scope,scope_name=scope_name)
	
	return