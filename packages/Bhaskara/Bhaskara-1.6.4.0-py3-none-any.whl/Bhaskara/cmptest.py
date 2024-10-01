from ExpressionTree1 import ExpressionTree
from FunctionalProcessingUnit import FunctionProcessingUnit as FPU
from LoopProcessingUnit2 import LoopProcessingUnit
from ConditonalProcessingUnit import ConditionalProcessingUnit as CPU
from StringAlgorithm.ConditionSplit import condition_split

class Compiler :
	
	def __init__(self,indent=4) :
		self.indent = indent
		self.loop_types = ['for','while']
		self.DataTypes = ['int','float','chars']
		self.ArrayDataTypes = ['int_arr','float_arr']
		self.int_literals = '0123456789'
		self.alpha = 'abcdefghijklmnopqrstuvwxyz'
		self.char_literals = 'abcdefghijklmnopqrstuvwxyz' + self.int_literals
		self.variable_error = "Error variable {} is not defined "
		self.value_error = "Incorrect value {}assigned to the variable {}"
		self.comment_syntax = '%'
		self.symbols = ["'",' ','.',">",'<','<=','=','/','?','*','-']
		self.func_body = {}
		self.functions = {}
		self.localVariables = {}
		self.func_scope = {}
		self.arithmetic_op = ['+','-','*','/']
		self.loop_scope = {}
		self.local_scope = {'func_scope' : self.func_scope,'loop_scope':self.loop_scope}
		self.localVariables = {'local_scope' : self.local_scope}
		self.globalVariables = {}
		self.Variables = {'global' : self.globalVariables,'local' : self.localVariables}
		self.literals = {'int' :self.int_literals,'float' : self.int_literals,'chars' : self.char_literals}
	
	def check_variable_name(self,name) :
		if name == '' :
			print("Error Name has not provided to the variable")
			return False
		if name[0] in self.alpha :
			for i in range(1,len(name)) :
				if not name[i].lower() in self.char_literals :
					print("Incorrect Variable name {}".format(name))
					return False
			return True
		print("Incorrect variable name {}".format(name))
		return False
	
	def has_indent(self,line,indent=0) :
		count = 0
		for l in line :
			if l == ' ' :
				count += 1
				continue
			break
		if count == self.indent+indent :
			return True
		return False
	
	def get_func_param(self,line) :
		if type(line) != type('a') :
			return 0,0,False
		name = ""
		param = ""
		is_found = False
		for i in line :
			if i == '(' :
				is_found = True
				continue
			if is_found :
				if i == ')' :
					break
				param += i
				continue
			name += i
		return name,param,is_found
	
	def fetch_var_value(self,name,scope='global',scope_name='') :
		is_var = False
		for n in name  :
			if n in self.alpha :
				is_var = True
				break
		if is_var :
			if scope == 'local' :
				var_scope = self.Variables[scope]['local_scope'][scope_name]
				if name in var_scope.keys() :
					val,_ = var_scope[name]
					return val
				if name in self.Variables[scope].keys() :
					val,_ = self.Variables[scope][name]
					return val
				print("Error variable {} is not defined".format(name))
				return
			if scope == 'global' :
				if name in self.Variables[scope].keys() :
					val,_ = self.Variables[scope][name]
					return val
				print("Error variable {} is not defined ".format(name))
				return
			return name
	
	def is_number(self,num) :
		is_num = True
		for n in num :
			if n == '.' :
				continue
			if not n in self.int_literals :
				is_num = False
				break
		return is_num
	
	def process_function(self,line,scope='global',scope_name='',exe=False,obj=None) :
		#func f(x) = 2*3+1
		line = line.split()
		st = "Error incorrect Syntax {}"
		if line == [] :
			return
		if len(line) == 1 :
			#f(x)
			name,param,_ = self.get_func_param(line[0])
			if name in self.func_body.keys() :
				#f(x,y)
				#f(res,2)
				tree,dic,param_f = self.func_body[name]
				params = param.split(',')
				for key,val in zip(param_f,params) :
					if self.is_number(val) :
						dic[key] = val
						continue
					value = self.fetch_var_value(val,scope=scope,scope_name=scope_name)
					dic[key] = value
				dic_ = dic
				tree.param_values = dic
				val = str(tree.computeTree(tree.head))
				tree.param_values = dic_
				return val
					
		if exe :
			#f(x) = g(x)*2
			#f(x,y) = x*g(y)/2
			#f(x) = x*g(res)/2
			#g(X)
			if not obj :
				return
			if type(line) == type('a') :
				line =line.split()
			if len(line) != 1 :
				print('Error function is not given alone {}'.format(line))
				return
			name,param,is_found = self.get_func_param(line[0])
			
			if not name in self.func_body.keys() :
				print("Error function {} is not defined".format(name))
				return
			tree_,g_dict,g_params = self.func_body[name]
			g_dict_ = g_dict
			has_found_all = True
			to_find = []
			for key in param :	
				if key in obj.param_values.keys() :
					g_dict[key] = obj.param_values[key]
					continue
				else :
					to_find.append(key)
					has_found_all = False
			
			if not has_found_all :
				for key in to_find :
					g_dict[key] = self.fetch_var_value(key,scope=scope,scope_name=scope_name)
					has_found_all = True
			tree_.param_values = g_dict
			output = str(tree_.computeTree(tree_.head))
			tree_.param_values = g_dict_
			return output
			
		if len(line) == 4 :
			if line[0] != 'func' :
				#print(st.format(line))
				return
			func_syntax = line[1]
			name = ""
			param = ""
			is_found = False
			name,param,is_found = self.get_func_param(line[1])
			
			if not is_found :
				print(st.format(line))
				return
			
			if not self.check_variable_name(name) :
				print("Error incorrect function name {}".format(name))
				return
			self.param_dict = {}
			for i in param :
				if i == ',' :
					continue
				if not i in self.alpha :
					print("Error parameter must be alphabets {}".format(param))
					return
			
			params = param.split(',')
			for p in params :
				self.param_dict[p] = ''
			expr = line[3]
			
			if line[2] != '=' :
				print(st.format(line))
				return
			
			has_op = False
			
			for op in self.arithmetic_op :
				if op in expr :
					has_op = True
			if has_op :
				tree = ExpressionTree(self.Variables,is_func=True,parameters=params,obj=self)
				tree.buildTree(expr)
				self.func_body[name] = [tree,self.param_dict,params]
				return
			self.func_body[name] = expr
			return
		if len(line) == 3 :
			#y = f(x)
			
			name,_,_ = self.get_func_param(line[2])
			if not name in self.func_body.keys() :
				return
			
			for op in self.arithmetic_op :
			    if op in line[2] :
			        return
			var_y = line[0]
			var_scope = None
			if scope == 'local' :
				is_found = False
				if var_y in self.Variables['local']['local_scope'][scope_name].keys() :
					var_scope = self.Variables['local']['local_scope'][scope_name]
					is_found = True
				if not is_found :
					if var_y in self.Variables['global'].keys() :
						var_scope = self.Variables['global']
						is_found = True
				if not is_found :
					print("Error variable {} is not defined".format(var_y))
					return	
			if scope == 'global' :
				if not var_y in self.Variables['global'].keys() :
					print("Error variable {} is not defined".format(var_y))
					return
				var_scope = self.Variables['global']
			name,param,is_found = self.get_func_param(line[2])
			if not is_found :
				#print(st.format(line))
				return
			if not name in self.func_body.keys() :
				print("Error function with name {} is not defined".format(name))
				return
			params = param.split(',')
			params_ = self.func_body[name][2]
			param_dict = self.func_body[name][1]
			for i,p in enumerate(params) :
				is_var = False
				for e in p :
					if e in self.alpha :
						is_var = True
						break
				if is_var :
					if scope == 'local' :
						if p in self.Variables['local']['local_scope'][scope_name].keys() :
							v,_ = self.Variables['local']['local_scope'][scope_name][p]
							param_dict[params_[i]] = v
							continue
						if p in self.Variables['global'].keys() :
							v,_= self.Variables['global'][p]
							param_dict[params_[i]] = v
							continue
						print("Error variable {} is not defined".format(p))
						return
					if scope == 'global' :
						if p in self.Variables['global'].keys() :
							v,_= self.Variables['global'][p]
							param_dict[params_[i]] = v
							continue
						print("Error variable {} is not defined".format(p))
						return
				param_dict[params_[i]] = params[i]
				
			tree = self.func_body[name][0]
			tree.param_values = param_dict
			value = str(tree.computeTree(tree.head))
			_,dt = var_scope[var_y]
			var_scope[var_y] = [value,dt]
			return True
			
	def process_Func(self,line,scope='global') :
			#y = pow(x)
			#where pow is a multiline function
			line = line.split()
			
			# y = 2*pow(x)
			if len(line) != 3 :
				return
			func_name = line[-1]
			name,param,_ = self.get_func_param(func_name)
			if name in self.functions.keys() :
				func = self.functions[name]
				val = func.executeTree(line)
				var_y = line[0]
				if scope == 'global' :
					if var_y in self.Variables['global'].keys() :
						_,dt = self.Variables['global'][var_y]
						self.Variables['global'][var_y] = [val,dt]
						return
				if var_y in self.Variables['local']['local_scope'][name].keys() :
					_,dt = self.Variables['local']['local_scope'][name][var_y]
					self.Variables['local']['local_scope'][name][var_y] = [val,dt]
					return
				if var_y in self.Variables['global'].keys() :
					_,dt = self.Variables['global'][var_y]
					self.Variables['global'][var_y] = [val,dt]
					return
			else :
				return
	
	def clean_line_from_op(self,line) :
		clean_line = ''
		for l in line :
			if l in self.arithmetic_op :
				clean_line += " "
				continue
			clean_line += l
		return clean_line
	
	def get_arr_index(self,arr) :
		name = ""
		index = ""
		count = 0
		is_arr = False
		found_brack = False
		N = len(arr)
		if arr[-1] != ']' :
			return False
		count = 1
		for i in range(N-1) :
			if arr[i] == '[' :
				count += 1
				found_brack = True
				continue
			if not found_brack :
				name += arr[i]
				continue
			index += arr[i]
		
		if count == 2 :
			is_arr = True
		if not self.check_variable_name(name) :
			is_arr = False
		
		return name,index,is_arr
		
	def have_two_brackets(self,var) :
		count = 0
		for i in var :
			if i == '[' or i == ']' :
				count += 1
		if count == 2 :
			return True
		return False
		
	def is_var_exist(self,var,scope='global',scope_name='') :
		if scope == 'global' :
			if var in self.Variables[scope].keys() :
				return True
			return False
		if var in self.Variables[scope]['local_scope'][scope_name].keys() :
			return True
		return self.is_var_exist(var,scope='global')
	
	def fetch_variable(self,var,scope='global',scope_name='') :
		if scope == 'global' :
			return self.Variables[scope][var]
		if var in self.Variables[scope]['local_scope'][scope_name].keys() :
			return self.Variables[scope]['local_scope'][scope_name][var]
		return self.fetch_variable(var,scope='global')
		
	def assign_array(self,name,value,index=None,scope='global',scope_name="") :
		if index :
			if scope == 'local' :
				if self.is_var_exist(name,scope=scope,scope_name=scope_name) :
					elements,dt = self.Variables['local']['local_scope'][scope_name][name]
					elements[index] = value
					self.Variables['local']['local_scope'][scope_name][name] = [elements,dt]
					return
			if self.is_var_exist(name,scope='global') :
				elements,dt = self.fetch_variable(name,scope='global')
				elements[index] = value
				self.Variables['global'][name] = [elements,dt]
				return
		return self.assign_value(name,value,scope=scope,scope_name=scope_name)
		
	def define_variable(self,variable,value,data_type,scope='global',scope_name="") :
		if scope == 'global' :
			self.Variables[scope][variable] = [value,data_type]
			return
		if scope == 'local' :
			self.Variables[scope]['local_scope'][scope_name][variable] = [value,data_type]
			return
		
	def assign_value(self,var,val,scope='global',scope_name='') :
		if scope == 'global' :
			if not self.is_var_exist(var) :
				print("Variable {} is not defined ".format(var))
				return
			_,dt = self.Variables[scope][var]
			self.Variables[scope][var] = [val,dt]
			return
		if var in self.Variables[scope]['local_scope'][scope_name].keys() :
			_,dt  = self.Variables[scope]['local_scope'][scope_name][var]
			self.Variables[scope]['local_scope'][scope_name][var] = [val,dt]
			return
		return self.assign_value(var,val,scope='global')
		
	def compute_index(self,index,scope='global',scope_name='',type='int') :
		if index :
			if self.is_number(index) :
				return int(index)
			has_op = False
			for op in self.arithmetic_op :
				if op in index :
					has_op  = True
					break
			if has_op :
				tree = ExpressionTree(Variables=self.Variables,scope=scope,scope_name=scope_name,obj=self)
				tree.buildTree(index)
				return_value = tree.computeTree(tree.head)
				if type == 'int' :
					return int(return_value)
				if type == 'float' :
					return float(return_value)
			return_value = self.fetch_var_value(index,scope=scope,scope_name=scope_name)
			if type == 'int' :
				return int(return_value)
			if type == 'float' :
				return float(return_value)
			
	def get_arr_element(self,name,index,scope='global',scope_name="") :
		if type(index) == type('a') :
			index = self.compute_index(index,scope=scope,scope_name=scope_name)
		elements,_ = self.fetch_variable(name,scope=scope,scope_name=scope_name)
		if index < len(elements) :
			return elements[index]
		print("index {} out of range for array of size {}".format(index,len(elements)))
		
	def has_arithmetic_op(self,line) :
		for op in self.arithmetic_op :
			if op in line :
				return True
		return False
		
	def process_array(self,line,scope='global',scope_name='') :
		if type(line) == type('a') :
			line = line.split()
		#int_arr arr[] = (1,2,3,4,5,6)
		#arr[6] = 7
		#arr = (1,2,3,4,5)
		if len(line) == 1 :
			#arr[i]
			# i E W
			if not self.get_arr_index(line[0]) :
				return
			name,index,_ = self.get_arr_index(line[0])
			elements = []
			data_type = None
			line_op = condition_split(index,'any')
			has_op = False
			if len(line_op) > 1:
				index = self.compute_index(index,scope=scope,scope_name=scope_name)
				has_op = True
			elements,data_type = self.fetch_variable(name,scope=scope,scope_name=scope_name)
			if not has_op :
				if not index in self.int_literals :
					if self.check_variable_name(index) :
						index = self.fetch_var_value(index,scope=scope,scope_name=scope_name)
			index = int(index)
			if index < len(elements) :
				return elements[index],data_type
			print("error index {} out of range in array {}".format(index,line[0]))
			return
		
		if len(line) == 4 :
			#int_arr arr[] = (1,2,3,4,5,6,7)
			#float_arr arr[] = (1.23,9.9)
			#int arr[5+1] = (1,2,3,4,5)
			if line[0] in self.ArrayDataTypes :
				data_type = line[0]
				name = line[1]
				is_arr= self.get_arr_index(name)
				if not is_arr :
					return
				name,index,_ = self.get_arr_index(name)
				index = self.compute_index(index,scope=scope,scope_name=scope_name)
				temp_elements = ''
				count = 0
				for e in line[-1] :
					if e == '('  :
						count += 1
						continue
					if e == ')' :
						count += 1
						continue
					temp_elements += e 
				elements_delta = []
				for e in temp_elements.split(',') :
					if self.is_number(e) :
						elements_delta.append(e)
						continue
					elements_delta.append(self.fetch_var_value(e))
				#fetched values of the element	
				if not count >= 2 :
					print("Syntax error {}".format(line))
					return
				if index :
					if index != len(elements_delta) :
						print("index {} does not match the number of elements in the array {}".format(index,elements))
						return
				if scope == 'local' :
					self.Variables['local']['local_scope'][scope_name][name] = [elements_delta,data_type]
					return
				data_type = data_type
				self.Variables['global'][name] = [elements_delta,data_type]
				return
		
		if len(line) == 3 :
			# y = arr[i]
			#arr[i] = y
			# t = arr[]
			#res = 2+arr[i]
			y = line[0]
			arr = line[2]
			clean_line = condition_split(arr,'any')
			have_arr = False
			for element in clean_line :
				if self.get_arr_index(element) :
					have_arr = True
					break				
			if not have_arr :
				return
			has_op = True
			if len(clean_line) == 1 :
				has_op = False
				
			if has_op :
				#var = arr[i+k]*arr[h+k]
				tree = ExpressionTree(Variables=self.Variables,scope=scope,scope_name=scope_name,obj=self)
				tree.buildTree(arr)
				val  = str(tree.computeTree(tree.head))
				#if y is an array then this will be executed
				if self.get_arr_index(y) :
					name,index_y,_ = self.get_arr_index(y)
					return_value = condition_split(index_y,'any')
					if len(return_value) > 1 :
						index_y = self.compute_index(index_y,scope=scope,scope_name=scope_name)
					if self.is_number(str(index_y)) :
						pass
					else :
						index_y = self.fetch_var_value(index_y,scope=scope,scope_name=scope_name)
					index_y = int(index_y)
					self.assign_array(name,val,index=index_y,scope=scope,scope_name=scope_name)
					return True
				#if y is a variable then this line will be executed
				self.assign_value(y,val,scope=scope,scope_name=scope_name)
				return True
			
			if  self.get_arr_index(arr) or  self.get_arr_index(y) :
				pass
			else :
				return
			#arr[i] = y
			if self.get_arr_index(y)  :
				name,index,_ = self.get_arr_index(y)
				index = self.compute_index(index,scope=scope,scope_name=scope_name)
				elements,dt  = self.fetch_variable(name,scope=scope,scope_name=scope_name)
				
				if self.check_variable_name(arr) :
					arr,_ = self.fetch_variable(arr,scope=scope,scope_name=scope_name)
				
				elif self.get_arr_index(arr) :
					#arr[i] = arr[j]
					name_j,j_index,_= self.get_arr_index(arr)
					j_index = self.compute_index(j_index,scope=scope,scope_name=scope_name)
					j_arr = self.get_arr_element(name_j,j_index,scope=scope,scope_name=scope_name)
					print(j_index)
					self.assign_array(name,j_arr,index=index,scope=scope,scope_name=scope_name)
					return
				self.assign_array(name,arr,index=index,scope=scope,scope_name=scope_name)
				return
			#y = arr[i]
			return_val = self.process_array(arr,scope=scope,scope_name=scope_name)
			if not return_val :
				return
			data_type = return_val[1].split('_')[0]
			self.assign_value(y,return_val[0],scope=scope,scope_name=scope_name)
			return
			
	def is_array(self,line) :
		for l in line :
			if l.split() == [] :
				continue
			if self.get_arr_index(l.split()[0]) :
				return True
		return False
		
	def is_function(self,line) :
		line = line.split('=')
		if len(line) == 1 :
			return True
		line  = line[1]
		# a = pow(2,3)
		if line.split('(')[0] in self.functions :
			return True
		if line.split('(')[0] in self.func_body :
			return True
		return False
		
	def check_number_literals(self,var,value) :
		for v in value :
			if v == '.' :
				continue
			if v == '-' :
				continue
			if not v in self.int_literals :
				print(self.value_error.format(value,var))
				return False
		return True
		
	def check_char_literals(self,var,value) :
		if value[0] != "'" or value[-1] != "'"  :
			print(self.value_error.format(value,var))
			return
		for v in value :
			if v in self.symbols :
				continue
			if not v.lower() in self.char_literals + self.int_literals :
				print(self.value_error.format(value,var))
				return False
		return True
		
	def format_char_literals(self,chars) :
		line = ''
		for i,char in enumerate(chars) :
			if i + 1 == len(chars) :
				line += char
				break
			line += char
			line += ' '
		return line
	
	def process_variable(self,line,scope='global',scope_name='') :
		if self.is_array(line.split('=')) :
			return
		if self.is_function(line) :
			return
		line = line.split()
		if len(line) <= 2 :
			return
		N = len(line)
		#DataTypes Var_name = Value
		#Var_name = value
		if line[0] == 'func':
		    return
		if line[0] in self.DataTypes :
			N = 4
		else :
			N = 3
		
		if N == 4 :
			data_type = line[0]
			if data_type in self.ArrayDataTypes :
				return
			
			name = line[1]
			value = line[3]
			if line[2] != '=' :
				print("Syntax Error from process_variable unit {}".format(line))
				return
			if not self.check_variable_name(name) :
				return
			
			if data_type in ['int','float'] :
				has_operator = False
				val = condition_split(value,'any')
				if len(val) > 1 :
					has_operator = True
				del val
				if has_operator :
					value = str(self.compute_index(value,scope=scope,scope_name=scope_name,type='float'))
				if not self.check_number_literals(name,value) :
					return
				self.define_variable(name,value,data_type,scope=scope,scope_name=scope_name)
				return True
				
			if data_type == 'chars' :
				value = self.format_char_literals(line[3:])
				if not self.check_char_literals(name,value) :
					return
				self.define_variable(name,value,data_type,scope=scope,scope_name=scope_name)
				return True
				
		if N == 3 :
			# a = 3
			if scope == 'local' :
				if scope_name == '' :
					 print("Error from process_variable unit please provide the name of the scope ")
					 return
				name = line[0]
				value = line[2]
				val = condition_split(value,'any')
				if len(val) > 1 :
					have_array = False
					for each_ele in val :
						if self.get_arr_index(each_ele) :
							return
				else :
					if self.get_arr_index(val[0]) :
						return
				
				if name in self.Variables[scope]['local_scope'][scope_name].keys() :
				   _,data_type = self.Variables[scope]['local_scope'][scope_name][name]
				   
				   if data_type in ['int','float'] :
				   	has_operator = False
				   	val = condition_split(value,'any')
				   	if len(val) > 1 :
				   		has_operator = True
				   	if has_operator :
				   	    value = str(self.compute_index(value,scope=scope,scope_name=scope_name,type='float'))
				   	if not self.check_number_literals(name,value) :
				   		return    
				   	self.assign_value(name,value,scope=scope,scope_name=scope_name)
				   	return True
				   if data_type == 'chars' :
				       value = self.format_char_literals(line[2:])
				       if not self.check_char_literals(name,value) :
				       	return
				       self.assign_value(name,value,scope=scope,scope_name=scope_name)
				       return True
				else :
					 line = self.format_char_literals(line)
					 return self.process_variable(line,scope='global')
					 if name in self.Variables['global'].keys() :
					 	_,data_type = self.Variables['global'][name]
					 	if data_type in ['int','float'] :
					 		has_op = False
					 		val = condition_split(value,'any')
					 		if len(val) > 1 :
					 			have_op = True
					 		if has_op :
					 			value = str(self.compute_index(value,scope=scope,scope_name=scope_name,type='float'))
					 		if not self.check_number_literals(name,value) :
					 			return
					 		self.assign_value(name,value,scope=scope,scope_name=scope_name)
					 		return True
					 	if data_type == 'chars' :
					 		value = self.format_char_literals(line[2:])
					 		if not self.check_char_literals(name,value) :
					 			return
					 		self.assign_value(name,value,scope=scope,scope_name=scope_name)
					 		return True	
					 print("Error assigning value before defining a variable {}".format(line))
					 return
			if scope == 'global' :
				name = line[0]
				value = line[2]
				if line[1] != '=' :
					print("Syntax Error {}".format(line))
					return	
				if name in self.Variables[scope].keys() :
					_,data_type = self.Variables[scope][name]
					if data_type in ['int','float'] :
						has_operator = False
						val = condition_split(value,'any')
						if len(val) > 1 :
							has_operator = True
						del val
						if has_operator :
							value = str(self.compute_index(value,scope=scope,scope_name=scope_name,type='float'))
						if not self.check_number_literals(name,value) :
							return
						self.assign_value(name,value,scope=scope,scope_name=scope_name)
						return True
					if data_type == 'chars' :
						value = self.format_char_literals(line[2:])
						if not self.check_char_literals(name,value) :
							return
						self.assign_value(name,value,scope=scope,scope_name=scope_name)
						return True
				else :
				 	print("Error variable is not defined {}".format(line))
				 	return
	
	def output_func(self,line,scope='global',scope_name='') :
		if '(' in line :
			line = line.split()
			if len(line) > 1 :
				return
			l = ""
			for i in line :
				l += i
			line = l
			del l
			expr = ''
			has_found = False
			for i in range(len(line)-1) :
				if line[i] == '(' :
					has_found = True
					continue
				if has_found :
					expr += line[i]
			if expr == '' :
				return
			if expr[0] == "'" and expr[-1] == "'" :
				print(expr)
				return
			expr = expr.split(',')
			if len(expr) >= 1 :
				for v in expr :
					has_op = False
					for op in ['*','/','+','-'] :
						if op in v :
							has_op = True
							break
					if has_op :
						if " " in v :
							e = v.split()
							expr_ = ''
							for i in e :
								expr_ += i
							v = expr_
						tree = ExpressionTree(Variables=self.Variables,scope=scope,scope_name=scope_name)
						tree.buildTree(v)
						print(tree.computeTree(tree.head))
						continue
					for i in v :
						if i in self.alpha :
							if scope == 'global' :
								try :
									val,_ = self.Variables[scope][v]
									print(val,' ')
									break
								except :
									pass
							if scope == 'local' :
								if v in self.Variables['local']['local_scope'][scope_name].keys():
									val,_ = self.Variables[scope]['local_scope'][scope_name][v]
									print(val," ")
									break
								if v in self.Variables['global'].keys() :
									v,_  = self.Variables['global'][v]
									print(v)
									break
						else :
							print(v," ")
							break
			return
	
	def output(self,line,scope="global",scope_name="") :
		pass
		
	def has_comment(self,line) :
		if self.comment_syntax in line.split()[0] :
			return True
		return False
	
	def ProcessLine(self,line,scope='',scope_name='') :
		if self.has_comment(line) :
			return	
		self.process_variable(line,scope=scope,scope_name=scope_name)
		self.process_Func(line,scope=scope)
		self.process_function(line,scope=scope,scope_name=scope_name)
		self.output_func(line,scope=scope,scope_name=scope_name)
		self.process_array(line,scope=scope,scope_name=scope_name)
	
	def ProcessLines(self,lines) :
		if type(lines) == type('a') :
			if '\n' in lines :
				lines = lines.split('\n')
		count = 0
		i = 0
		loop_count = 0
		N = len(lines)
		while i < N :
			line = lines[i]
			if line.split() == [] :
				i = i + 1
				continue
			if line.split()[0] == 'terminate' :
				return
			if line.split()[0] == 'Func' :
				name,_,_ = self.get_func_param(line)
				if len(name.split()) > 1 :
					name = name.split()[1]
				self.Variables['local']['local_scope'][name] = {}
				Func = FPU(compiler=self,scope='local',scope_name=name)
				self.functions[name] = Func
				_,pos = Func.buildTree(lines[i:],indent=self.indent)
				i = i + pos
				continue
			if line.split()[0] in self.loop_types :
				self.Variables['local']['local_scope']['for'+str(loop_count)] = {}
				loop = LoopProcessingUnit(self.Variables,scope_name='for'+str(loop_count),indent=self.indent,process_variable=self.process_variable,output_func=self.output_func,obj=self)
				pos = loop.buildTree(lines[i:])
				loop.executeTree(node=loop.loop_node)
				i = i + pos
				continue
			if line.split()[0]  == 'if' :
				self.Variables['local']['local_scope']['if_0'] =  {}
				cpu = CPU(scope='local',scope_name='if_0',compiler=self)
				cpu.indent = 0
				pos = cpu.buildTree(lines[i:],indent=self.indent)
				cpu.executeTree(cpu.head)
				i  = i + pos
				continue
			self.ProcessLine(line,scope='global')
			i= i + 1
		return
		
	def compile(self,lines) :
		pass
		
compiler = Compiler()
Lines = """
int a = 2
chars name = 'Pinku Khare'
func f(x) = x*x+2+4/3
float s = a*2
int res = 0
name = 'Prakamya Khare'
int num = s*a+3*a
print("Prakamya")
for i = 1 to a :
    int a = 2
    for j = 1 to 10 :
        func g(x) = 8*x
        a = g(j)
        print(a)
        for k = 1 to 3 :
            res = res+1
            a = f(k)
            print(a)
        a = a+2
        res = res+1
        print("Pinku",j)
    print(a)
print(a)
print(name)
print('res',res)
for i = 1 to 5 :
    print(i)
print(s)
res = f(3)
print(res)
func pow(n) = n*n
int res = 0
res = pow(5)
print(res)
func multivar(x,y) = x+x*y+y
res = multivar(3,4)
print(res)
res = f(3)
func two(x) = pow(x)/f(x)
print(res)
res = two(2)
print(res)
print('eeeee')
func fun(x) = 2*x
func hh(x) = fun(x)/pow(x)
int ss = 0
ss = pow(2)
print(ss)
ss = hh(2)
print(ss)
func gg(x) = 3*fun(x)*multivar(x,x)
ss = gg(2)
print(ss)

Func demo(x)  :
    int a = 0
    for i = 1 to x :
        a = a+i
    return a
ss = demo(2)
print('ss')
print(ss)
print('ss')
print(ss)
print('name')
""" 

L1 = """
func g(x) = x*x
func h(x) = 9*x
Func f(x) :
    int res = 1
    for i = 1 to x :
        res = res*i
    print('res')
    print(res)
    return res
Func pow(x,r) :
    float res = x-0
    int b = r-1
    for i = 1 to b :
        res = res*x
    return res

int a = 0
int res = 0
res = f(10)
print(res)
a = h(44)
print(a)
res = 2*h(a)/f(2)
print(res)
res = pow(2,5)
print(res)
print('here')
for i = 1 to 10 :
    print('here')
    for j = 1 to 10 :
        print(j)
"""

L2 = """
Func f(x,y) :
    int res = 0
    for i = x to y :
        res = res+i
    print(res)
    for i = x to y :
        print("here")
        for j = x to y :
            for k = 1 to 4 :
                print(k)
            print('nes')
            res = res+j
    print(res)
    return res

int val = 0
val = f(1,10)
print(val)

Func pow(x,r) :
    int res = x-0
    int r = r-1
    for i = 1 to r :
        res = res*x
    return res
func f(x) = 2*x
func g(x) = 3*x
float res = 0.0
res  = f(2)+f(3)
print(res)

"""

L3 = """
func f(x) = 2*x
func g(x) = 3*x
float res = 0.0
float x = 3
res = g(3)
float res1 = 0.0
res1 = f(3)
float a = 0.0
res1 = res/res1
print(res1)
res = f(2)+g(3)
"""
L4 = """
func s(k) = k+1
Func pow(x,r) :
    int res = x-0
    r = r-1
    int v = 0
    v = s(x)
    for i = 1 to r :
        res = res*x
    return res
func f(x) = 2*x
func g(x) = 4*x
int res = 0.0
int y = 4
int h = 2
res = f(4)+g(2)
print(res)
int res1 = f(res)+g(res)
print(res)
print(res1)
int a = 0
a = pow(2,5)
print(a)
int x = 2
int r = 2
int value = x*3/pow(x,r)
print(value)
int value = pow(x,r)*pow(x,r)/g(x)+f(4)
print(value)
int a = 3
int b = 4
if a |= b :
    for i = 1 to 10 :
        print(i)
        print('1')
        if i == 8 :
            print('i == 8')
        else :
            print(i)
    a = pow(a,a)
    print(a)
    print('True')
else :
    a = pow(2,2)
    print(a)
    print('False')

print('here')
"""
L5 = """
int a = 5
for i = 1 to 5 :
    if i == 4 :
        if i == 2 :
            print('here')
            print('22222')
        print('if')
    else :
        if i == 3 :
            print('aaaaa')
        print('else')
        if i == 3 :
            print('trueeeee')
    print(i)
print('here')

Func condt(x) :
    int istrue = 0
    if x == 1 :
        istrue = 1
        print('true')
    return istrue

int val = 0
val = condt(1)
print(val)

int a = 3
int n = 4
if a |= n :
    if a < n :
        print(a)
        print('a')
    else :
        print(n)
        print('m'n)
else :
    print('aaa')
print('heeeeeey')
"""

L6 = """
for i = 1 to 10 :
    if i == 5 :
        if i |= 4 :
            print('true')
        print('isone')
        print(i)
    else :
        if i == 2 :
            print('isone')
            print(i)
            print('i==2')
        else :
            print(i)
    print(i)

print('heyitsworking')
"""
L7 = """
int x = 2

Func poww(x,r) :
    int res = x-0
    int r = r-1
    for i = 1 to r :
        res = res*x
    print(res)
    return res

Func pow(x,r) :
    if r == 0 :
        print('hereso')
        return 1
    int res = x-0
    int val = 0
    if r < 0 :
        res = pow(x,-r)
        res = 1/res
        return res
    if r == 1 :
        print('here')
        return x
    if r == 0 :
        print('hereo')
        return 1
    r = r-1
    for i = 1 to r :
        res = res*x
    return res        

float val = 0
val = pow(2,-1)
print(val)
for i = 1 to 10 :
    print(i)
int i = 2
if i |= 1 :
    print('yes')
"""
L9 = """
Func pow(x,r) :
    if r == 0 :
        return 1
    if r == 1 :
        print('hereinsideif')
        return x
    print('hereout')
    int res = x-0
    r = r-1
    for i = 1 to r :
        res = res*x
    return res
chars name = 'Prakamya Khare'
int res = 0
int e = 0
res = pow(2,e)
print(res)

Func fact(x) :
    if x == 1 :
        return x
    int res = 0
    int a = x-0
    x = x-1
    res = a*fact(x)
    return res

int fac = 0
fac = fact(6)
print(fac)
int n = 5
int_arr arr[n] = (1,2,3,2324,5)
print(arr)
int y = 0
int i = 2
y = arr[i*2]
print(y)
int j = 1
arr[j+j+j] = arr[j+1]
print(arr)
for i = 1 to n :
    print(arr[i])
Func mean(arr,n) :
    int res = 0
    for i = 1 to n :
        res = res+arr[i-1]
    res = res/n
    return res
int res = 0
res = mean(arr,n)
int k = 3
int j = 0
print(arr)
arr[j+1] = arr[k+1]*arr[k-1]
print(res)
print(arr)
if k == 1 :
    print(k)
else :
    if j == 0 :
        if k == 3 :
            print('here')
    else :
        print('else')
float a = arr[k+1]*arr[k-1]
print(a)
"""

L10 = """
func f(x,y) = 2*x+y
Func g(x,y,z) :
    float res = 0
    res = 2*x+y*z
    return res
int_arr arr[] = (1,2,3,4,5)
print(arr)
float res = 0.0
int k = 0
int l = 1
arr[k+1] = arr[k]*arr[k+2*l]
k = arr[k+1]
res = f(k,5)
print('res')
print(res)
print(arr)
res = g(3,2,3)
print(res)
"""
compiler.ProcessLines(L1)
#print(compiler.Variables['global'])