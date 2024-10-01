from ExpressionTree1 import ExpressionTree
from StringAlgorithm.ConditionSplit import condition_split

def get_char_upto_n(compiler,line) :
	N  = len(line)
	k = 0
	chars  = ''
	for i in range(N) :
		if line[i] in compiler.int_literals+'-*/+' :
			k = i
			break
		chars += line[i]
	return chars,k

def process_functions(compiler,line,scope='global',scope_name='',exe=False) :
	
	if type(line) == type('a') :
		line = line.split()
	
	if len(line) == 1 and exe:
		#f(x)
		line = line[0]
		if not compiler.is_function(line) :
			return
		
		name,params_value,_ = compiler.get_func_param(line)
		
		if not name in compiler.func_body.keys() :
			return
		
		params_value = params_value.split(',')
		params_keys = compiler.func_body[name]['params']
		params = {}
		k = 0

		for i in range(len(params_value)) :
			val  = None
			if compiler.is_number(params_value[i]) :
				 val = params_value[i]
			elif compiler.check_variable_name(params_value[i]) :
				value = compiler.fetch_var_value(params_value[i],scope=scope,scope_name=scope_name)
				val = value
			params[params_keys[i]] = val
		
		expression  = compiler.func_body[name]['expression']
		N = len(expression)
		numerised_expression = ''
		
		if expression == "" :
			return
		
		for i in range(N) :
			if i+k >= N :
				break
				
			if expression[i+k] in compiler.alpha :
				chars,k = get_char_upto_n(compiler,expression[i+k:])
				k = k + 1
				if chars in params.keys() :
					numerised_expression += params[chars]
			numerised_expression += expression[i+k]		
		
		print(numerised_expression)
		value = compiler.compute_index(numerised_expression,scope=scope,scope_name=scope_name)
		return value
	
	if len(line) == 4 :
		#func f(x,y) = 2*x+3*y
		
		if line[0] != 'func' :
			return
		
		name,params,_= compiler.get_func_param(line[1])
		compiler.func_body[name] = {}
		compiler.func_body[name]['expression'] = line[-1]
		params = params.split(',')
		compiler.func_body[name]['params']  = params
		return

	if len(line) == 3 :
		#y = f(x)
		#y = f(x)/g(x)
		var_y = line[0]
		is_array = False
		index = None
		
		if '=' != line[1] :
			return
		
		if compiler.get_arr_index(var_y) :
			name,index,_ = compiler.get_arr_index(var_y)
			is_array = True
			var_y = name
			index = compiler.compute_index(index,scope=scope,scope_name=scope_name)
		
		
		if not compiler.fetch_variable(var_y,scope=scope,scope_name=scope_name) :
			print("error variable {} is not defined [process_function]".format(var_y))
			return
		
		value = line[2]
		
		if compiler.check_variable_name(value) :
			return
		
		has_op = False
		if len(condition_split(value,'any')) > 1 :
			has_op = True
		
		if has_op :
			value = compiler.compute_index(value,scope=scope,scope_name=scope_name,type='float')
		else :
			if not compiler.is_function(value) :
				return
			name,p,_ = compiler.get_func_param(value)
			if not name in compiler.func_body.keys() :
				return
			#that means it's single function
			value = process_functions(compiler,value,scope=scope,scope_name=scope_name,exe=True)
		
		#now assign the computed value to the variable y
		if is_array :
			compiler.assign_array(var_y,value,index=index,scope=scope,scope_name=scope_name)
			return
		compiler.assign_value(var_y,value,scope=scope,scope_name=scope_name)
		return	