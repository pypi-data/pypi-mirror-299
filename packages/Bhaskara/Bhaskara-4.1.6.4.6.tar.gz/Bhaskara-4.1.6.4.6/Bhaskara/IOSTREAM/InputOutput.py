

def split(line,char=',') :
	new_line = []
	found_b = False
	params = ''
	open_b = ['[','(','{']
	closing_b = [']',')','}']
	N = len(line)
		
	for i in range(len(line)) :
		if line[i] in open_b :
			params += line[i]
			found_b = True
			continue
		if line[i] in closing_b :
			params += line[i]
			found_b = False
			if i+1 == N :
				new_line.append(params)
			continue
		if found_b :
			if line[i] == ' ' :
				if i+1 == N :
					new_line.append(params)
				continue
			params += line[i]
			continue
		if line[i] == char :
			new_line.append(params)
			params = ''
			continue
		params += line[i]
		if i+1 == len(line) :
			new_line.append(params)
	return new_line
	

def get_func_param(line) :
	name = ''
	param = ''
	is_found = False
	#f(g(x))
	ob_count = 0
	N = len(line)
	for i in range(N-1) :
		if line[i] == '(' :
			if ob_count == 1 :
				param += line[i]
				continue
			ob_count += 1
			is_found = True
			continue
		if not is_found :
			name += line[i]
			continue
		param += line[i]
	
	return name,param

class InputOutputStream :
	
	def __init__(self,compiler=None) :
		self.compiler = compiler
		self.output_function_name = 'ans'
		self.input_function_name = 'ask'
		
	def execute(self,line) :
		pass
				
	def ans(self,line,scope='',scope_name='') :
		if len(line.split()) > 1 :
			return
		syntax = line.split()[0]
		name,params = get_func_param(line.split()[0])
		
		if name != self.output_function_name :
			return

		params = split(params,',')
		params_value = []
		for param in params :
			if param in self.compiler.mathematical_constants.keys() :
				params_value.append(str(self.compiler.mathematical_constants[param]))
			elif self.compiler.is_char(param) :
				params_value.append(param)
			elif self.compiler.is_function(param) :
				params_value.append(str(self.compiler.execute_Functions(param)))
			elif self.compiler.get_arr_index(param) and not '.' in param :
				value,_ = self.compiler.process_array(param,scope=scope,scope_name=scope_name)
				params_value.append(value)
			elif self.compiler.is_number(param) :
				params_value.append(param)
			elif self.compiler.check_variable_name(param) :
				value,_= self.compiler.fetch_variable(param,scope=scope,scope_name=scope_name)
				params_value.append(value)
			elif '.' in param and not self.compiler.is_a_number(param) :
				value = self.compiler.line_to_execute(param,scope,scope_name,'accessing_attributes')
				params_value.append(value)
			elif len(self.compiler.function_to_execute(param,scope,scope_name,'condition_split')) > 1 :
				params.append(str(self.compiler.compute_index(param,scope=scope,scope_name=scope_name)))
			
			else :
				print("error incorrect input to ans function :- {}".format(param))
				return
		
		parameters = ""
		for param in params_value :
			parameters += str(param) + " "
		print(parameters)
		return True
	
	def ask(self,line,scope='',scope_name='') :
		if len(line.split()) > 1 :
			return
		#ask(variable,string)
		syntax = line.split()[0]
		name,params,_ = self.compiler.get_func_param(syntax)
		if name != self.input_function_name :
			return
		params = params.split(',')
		variable = params[0]
		string = params[1] if len(params) > 1 else ""
		value = input(string)
		
		#if the variable is an array so here we have to use different approach
		if self.compiler.get_arr_index(variable) :
		 	line = variable + ' ' + '=' +'  '+ value
		 	self.compiler.process_array(line,scope=scope,scope_name=scope_name)
		 	return True
		self.compiler.assign_value(variable,value,scope=scope,scope_name=scope_name)
		return True