import LoopProcessingUnit2 as LPU
from StringAlgorithm.ConditionSplit import condition_split


class ConditionalNode :
	
	def __init__(self,) :
		"""
		if :- True block
		else :- False block
		
		"""
		self.syntax = []
		self.body = {'if' : [],'else' : []}
		

class ConditionalProcessingUnit :
	
	def __init__(self,scope='',scope_name='',compiler=None,indent=0) :
		self.indent = compiler.indent
		self.scope  = scope
		self.for_loop = LPU.LoopProcessingUnit(compiler.Variables,scope=scope,scope_name=scope_name)
		self.scope_name = scope_name
		self.indent  = compiler.indent
		self.compiler = compiler
		self.has_loop = False
		self.nums = '0123456789'
		self.alpha = 'abcdefghijklmnopqrstuvwxyz'
		self.syntax_error = 'Syntax error {}'
		self.is_char = False
		self.boolean_ops = ['==','|=','<=','>=','<=','<','>','≠','≤','≥','∈','∉']
		
	def check_variable(self,name) :
		if name[0] in self.alpha +'_':
			for n in range(1,len(name)) :
				if not name[n].lower() in self.nums+self.alpha +'_':
					return False
			return True
		return False
		
	def has_indent(self,line,indent) :
		count = 0
		for l in line :
			if l == ' ' :
				count += 1
				continue
			break
		if count == indent+self.indent :
			return True
		return False
		
	def check_syntax(self,line) :
		if type(line) == type('a') :
			line = line.split()
		if line[0] != 'if' :
			if line[0] == 'else' and line[1] == ':' :
				if len(line) == 2 :
					return True
				return False
			print(self.syntax_error.format(line))
			return
		 #if a  == b :
		if len(line) != 5 :
		 	return
		bool_op = line[2]
		if not bool_op in self.boolean_ops :
		 	print(self.syntax_error.format(line))
		 	return
		if line[-1] != ':' :
			print(self.syntax_error.format(line))
			return
		a = line[1]
		b = line[3]
		vars = [a,b]
		for var in vars :
		 	if self.compiler.get_arr_index(var) :
		 		continue
		 	if var[0] in self.nums :
		 		continue
		 	if self.compiler.is_char(var) :
		 		self.is_char = True
		 		continue
		 	else :
		 		if not self.check_variable(var) :
		 			print("{} Incorrect variable name {}".format(line,var))
		 			return
		return True
		 
	def buildTree(self,lines,prev_node=None,mode='if',prev_mode="",indent=0) :
		line = lines[0]
		node = None
		if mode == 'if' :
			node = ConditionalNode()
			if not self.check_syntax(line) :
				return
			node.syntax = line.split()
			if prev_node :
				prev_node.body[prev_mode].append(node)
			else :
				self.head = node
		else :
			if not self.check_syntax(line) :
				print(self.syntax_error.format(line))
				return
			node = prev_node
		i = 1
		N = len(lines)
		
		while i < N :
			line = lines[i]
			if line.split() == [] :
				i  = i + 1
				continue
			if not self.has_indent(line,indent) :
				if self.has_indent(line,indent-self.compiler.indent) :
					if line.split()[0] == 'else' :
						pass
					else :
						break
				else :
					break
			if line.split()[0] == 'if' :
				pos = self.buildTree(lines[i:],prev_node=node,mode='if',prev_mode=mode,indent=indent+self.compiler.indent)
				i  = i + pos
				continue
			if line.split()[0] == 'else' :
				pos = self.buildTree(lines[i:],prev_node=node,mode='else',prev_mode=mode,indent=indent)
				i  = i + pos
				continue
			if line.split()[0] == 'for' :
				for_loop = LPU.LoopProcessingUnit(Variables=self.compiler.Variables,indent=self.compiler.indent,scope=self.scope,scope_name=self.scope_name,process_variable=self.compiler.process_variable,output_func=self.compiler.output_func,obj=self.compiler)
				
				pos  = for_loop.buildTree(lines[i:],indent=indent)
				node.body[mode].append(for_loop)
				i = i + pos
				continue
			node.body[mode].append(line)
			i = i + 1
		return i
		
	def fetchValue(self,var) :
		
		if self.compiler.is_char(var) :
			N = len(var)-1
			var = var[1:N]
			return var
		
		if self.compiler.get_arr_index(var) :
			name,index,_ = self.compiler.get_arr_index(var)
			if len(condition_split(index,'any')) > 1 :
				index = self.compiler.compute_index(index,scope=self.scope,scope_name=self.scope_name)
			elif self.check_variable(index) :
				index = self.compiler.fetch_var_value(index,scope=self.scope,scope_name=self.scope_name)
			index = int(index)
			return self.compiler.get_arr_element(name,index=index,scope=self.scope,scope_name=self.scope_name)
			
		if self.check_variable(var) :
			if self.scope == 'local' :
				if var in self.compiler.Variables['local']['local_scope'][self.scope_name].keys() :
					v,_ = self.compiler.Variables['local']['local_scope'][self.scope_name][var]
					return v
			if var in self.compiler.Variables['global'].keys() :
				v,_ = self.compiler.Variables['global'][var]
				return v
			print("Error variable {} is not defined".format(var))
			return
		return var
		
	def check_condition(self,a,b,op='==') :
		if op == '==' :
			return a==b
		if op == '|=' or op == '≠' :
			return a != b
		if op == '<' :
			return a < b
		if op == '<=' or op == "≤" :
			return a <= b
		if op == '>' :
			return a > b
		if op == '>=' or op == "≥" :
			return a >= b
		if op == '∈' :
			if a in b :
				return True
			return False
		if op == '∉' :
			if a in b :
				return False
			return True

	def compute_return_value(self,value) :
		if len(condition_split(value,'any')) > 1 :
			val = self.compiler.compute_index(value,scope='local',scope_name=self.scope_name,type='float')
			return str(val)
		if self.compiler.is_number(value) :
			return value
		return self.compiler.fetch_variable(value,scope='local',scope_name=self.scope_name)[0]
	
	def executeTree(self,node=None) :
		if node :
			#if a == b :
			syntax = node.syntax
			a = None
			b = None
			if self.is_char :
				if not self.compiler.is_char(syntax[1]) :
					a = self.compiler.fetch_var_value(syntax[1],scope=self.scope,scope_name=self.scope_name)
				else :
					a = syntax[1]
					n = len(a)-1
					a = a[1:n]
				if not self.compiler.is_char(syntax[3]) :
					b = self.compiler.fetch_var_value(syntax[3],scope=self.scope,scope_name=self.scope_name)
				else :
					b = syntax[3]
					n = len(b)-1
					b = b[1:n]
				
			elif syntax[2] in ['∈','∉'] :
				a = str(int(float(self.fetchValue(syntax[1]))))
				b = self.fetchValue(syntax[3])
			else :
				a = float(self.fetchValue(syntax[1]))
				b  = float(self.fetchValue(syntax[3]))
			
			op = syntax[2]
			if self.check_condition(a,b,op) :
				body = node.body['if']
				for line in body :
					if type(line) == type('a') :
						if line.split()[0] == 'return' :
							if len(line.split()) == 1 :
								return line
							if self.compiler.is_function(line.split()[1]) :
								name,_,_ = self.compiler.get_func_param(line.split()[1])
								if name in self.compiler.functions.keys() :
									func = self.compiler.functions[name]
									func.outer_scope = self.scope_name
									return func.executeTree(line.split()[1])
								if name in self.compiler.func_body.keys() :
									return self.compiler.process_functions(line.split()[1],scope=self.scope,scope_name=self.scope_name,exe=True)
							if len(line.split(',')) > 1 :
								line = line.split()[1].split(',')
								return_value = []
								for var in line :
									if self.compiler.is_number(var) :
										return_value.append(var)
										continue
									return_value.append(self.compiler.fetch_variable(var,scope='local',scope_name=self.scope_name)[0])
								return return_value
							if self.has_loop :
								return line
							return self.compute_return_value(line.split()[1])
							
					if type(line) == type(node) :
						v = self.executeTree(node=line)
						if v :
							return v
						continue
					if type(line) == type(self.for_loop) :
						line.executeTree(line.loop_node)
						continue
					return_val =self.compiler.ProcessLine(line,scope=self.scope,scope_name=self.scope_name)
					if return_val == self.compiler.break_statement :
						if self.has_loop :
							return return_val
					elif return_val == self.compiler.continue_statement:
						if self.has_loop :
							return return_val
				return
			else :
				body  = node.body['else']
				if body == [] :
					return
				for line in body :
					if type(line) == type('a') :
						if line.split()[0] == 'return' :
							if len(line.split()) == 1  :
								return 'return'
							if len(line.split(',')) > 1 :
								return_value = []
								line = line.split()[1].split(',')
								for var in line :
									if self.compiler.is_number(var) :
										return_value.append(var)
										continue
									return_value.append(self.compiler.fetch_variable(var,scope='local',scope_name=self.scope_name)[0])
								return return_value
							return self.compute_return_value(line.split()[1])
							
					if type(line) == type(node) :
						val = self.executeTree(line)
						if val :
							return val
						continue
					if type(line) == type(self.for_loop) :
						line.executeTree(line.loop_node)
						continue
					return_val = self.compiler.ProcessLine(line,scope=self.scope,scope_name=self.scope_name)			
					if return_val == self.compiler.break_statement :
						if self.has_loop :
							return return_val
					elif return_val == self.compiler.continue_statement :
						if self.has_loop :
							return_val
				return
			return