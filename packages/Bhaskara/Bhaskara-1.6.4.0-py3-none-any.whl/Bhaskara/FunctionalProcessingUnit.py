from LoopProcessingUnit2 import LoopProcessingUnit as LPU
from ExpressionTree1 import ExpressionTree as ET
from ConditonalProcessingUnit import ConditionalProcessingUnit as CPU
from StringAlgorithm.ConditionSplit import condition_split
from StringAlgorithm.ConditionSplitV3 import condition_split_v2 
from StringAlgorithm.ExtractFuncNameParams import extract_name_param
from StringAlgorithm.SplitString import split

class FuncNode() :
	
	def __init__(self,) :
		self.name = ''
		self.body = []
		self.params = ''
	
class FunctionProcessingUnit :
	
	def __init__(self,scope='',scope_name='',compiler=None,indent=0) :
		self.head = None
		self.compiler = compiler
		self.For = LPU(compiler.Variables,scope_name=scope_name)
		self.cpu = None
		self.scope = scope
		self.indent = indent
		self.nums = '0123456789'
		self.scope_name = scope_name
		self.outer_scope = None
	
	
	def has_indent(self,line,indent) :
		count = 0
		for i in line :
			if i == ' ' :
				count += 1
				continue
			break
		if count == indent :
			return True
		return False
		
	def format_line(self,line) :
		new_line = []
		for e in line :
			if e == ' ' or e == '' :
				continue
			new_line.append(e)
		return new_line
	
	def check_syntax(self,line) :
		#Func Name(a1,a2,a3) :
		#Name(a1,a2,a3)
		line = condition_split(line,' ')
		line = self.format_line(line)
		
		if len(line) == 1 :
			name,param,found = extract_name_param(line[0])
			if not found :
				print("Error not a function from FPU :- check_syntax")
				return
			if name != self.head.name :
				print("error function {} is not defined".format(name))
				return
			if not self.compiler.check_variable_name(name) :
				print("Incorrect name {} given to the function".format(name))
				return
			p = param.split(',')
			for e in p :
				if not self.compiler.check_variable_name(e) :
					print("Incorrect paramater name {}".format(e))
					return
			return True
		
		if line[0] != 'Func' :
			return
		name,param,found = extract_name_param(line[1])
		
		if not found :
			return
		if not self.compiler.check_variable_name(name) :
			print("Incorrect name {} given to the function".format(name))
			return
		p = param.split(',')
		for e in p :
			e = e.split()[1]
			if not self.compiler.check_variable_name(e) :
				print("Incorrect paramater name {}".format(e))
				return
		if line[2] != ':' :
			print("Syntax Errror {}".format(line))
			return
		return True
	
	def buildTree(self,lines,prev_node=None,indent=0) :
		node = FuncNode()
		if type(lines) == type('a') :
			lines = lines.split('\n')
		if not self.check_syntax(lines[0]) :
			return
		name,params,_= self.compiler.get_func_param(lines[0])
		node.name = name.split()[1]
		node.params = params
		if not prev_node :
			for param in params.split(',') :
				data_type = param.split()[0]
				variable = param.split()[1]
				self.compiler.define_variable(variable,"",data_type,scope='local',scope_name=self.scope_name)
		if prev_node :
			prev_node.body.append(node)
		else :
			self.head = node
		i = 1
		N = len(lines)
		while i < N :
			line = lines[i]
			if line.split() == [] :
				i = i + 1
				continue
			if not self.has_indent(line,indent) :
				break
			if line.split()[0] == 'Func' :
				_,pos = self.buildTree(lines[i:],prev_node=node,indent=indent+self.compiler.indent)
				i = i + pos
				continue
			if line.split()[0] == 'for' :
				for_obj = LPU(self.compiler.Variables,scope=self.scope,scope_name=self.scope_name,indent=self.compiler.indent,process_variable=self.compiler.process_variable,output_func=self.compiler.output_func,obj=self.compiler,is_func=True)
				node.body.append(for_obj)
				for_obj.indent = 0
				pos = for_obj.buildTree(lines[i:],indent=indent+self.compiler.indent)
				i = i + pos
				continue
			if line.split()[0] == 'if' :
				cpu = CPU(scope=self.scope,scope_name=self.scope_name,compiler=self.compiler)
				cpu.indent = 0
				pos = cpu.buildTree(lines[i:],indent=indent+self.compiler.indent)
				node.body.append(cpu)
				i = i + pos
				if not self.cpu :
					self.cpu = cpu
				continue
			node.body.append(line)
			i = i + 1
			continue
		return 0,i
		
	def is_def(self,var) :
		if var in self.compiler.Variables['local']['local_scope'][self.scope_name].keys() :
			return True
		if var in self.compiler.Variables['global'].keys() :
			return True
		return False
	
	def minus_minus_plus(self,num) :
		if len(num) >= 3 :
			if num[0] == '-' and num[1] == '-' :
				return num[2:]
		return num
	
	def fetchValue(self,var) :
		if var in self.compiler.Variables['local']['local_scope'][self.scope_name].keys() :
			return self.compiler.Variables['local']['local_scope'][self.scope_name][var]
		if var in self.compiler.Variables['global'].keys() :
			return self.compiler.Variables['global'][var]
		print("Error variable {} is not defined ".format(var))
		return
		
	def print_variable(self,name,scope) :
		print(self.compiler.Variables['local']['local_scope'][scope][name])
	
	def format_negative_variables(self,variable) :
		if variable == "" :
			return
		#r = -r
		# -r =-val
		if variable[0] == '-' :
			return variable[1:]
		return
	
	def executeTree(self,line,has_scope=False) :
		# y = f(2)
		"""
		Func f(x) :
			int a = 0
			for i =1 to 10 :
				a = a + 1
			return a*x
		
		res = 2+f(2)
		"""
		
		if type(line) == type('a') :
			line = line.split()
			
		
		if len(line) == 1 :
			#f(2)
			#f(2,3)
			#f(x,y)
			#param_val = [2,3]
			#param_name = [x,y]

			name,param,_ = extract_name_param(line[0])
			params_val = split(param,',')
			params_name = self.head.params.split(',')

			for key,val in zip(params_name,params_val) :
				key = key.split()[1]
				is_negative = False

				if self.compiler.is_function(val) :
					val = self.compiler.execute_Functions(val,scope=self.scope,scope_name=self.scope_name)
					self.compiler.assign_value(key,val,scope=self.scope,scope_name=self.scope_name)
					continue
					
				if self.compiler.get_arr_index(val) and not '.' in val :
					try :
						val,_ = self.compiler.process_array(val,scope=self.scope,scope_name=self.scope_name)
					except :
						val,_ = self.compiler.process_array(val,scope=self.scope,scope_name=self.outer_scope)
					self.compiler.assign_value(key,val,scope=self.scope,scope_name=self.scope_name)
					continue
					
				
				if self.compiler.is_number(val) :
					self.compiler.assign_value(key,val,scope='local',scope_name=self.scope_name)
					continue
					
				if len(condition_split(val,'any')) > 1 :
					val = self.compiler.compute_index(val,scope=self.scope,scope_name=self.scope_name)
					self.compiler.assign_value(key,val,scope='local',scope_name=self.scope_name)
					continue
				
				if '.' in val :
					val_ = self.compiler.line_to_execute(val,'local',self.scope_name,'accessing_attributes')
					if val_ == None :
						if self.outer_scope :
							val_ = self.compiler.line_to_execute(val,'local',self.outer_scope,'accessing_attributes')
					self.compiler.assign_value(key,val_,scope='local',scope_name=self.scope_name)
					continue
				
				if self.format_negative_variables(val) :
					val = self.format_negative_variables(val)
					is_negative = True
				
				if self.outer_scope == self.scope_name :
					#recursion case
					if val in self.compiler.Variables['local']['local_scope'][self.scope_name].keys() :
						data,dt = self.compiler.fetch_variable(val,scope='local',scope_name=self.scope_name)
						if data != '' or data != None :
							if is_negative :
								data = '-' + data
								data = self.minus_minus_plus(data)
							self.compiler.assign_value(key,data,scope='local',scope_name=self.scope_name)
							continue
					if val in self.compiler.Variables['global'].keys() :
						data,dt = self.compiler.fetch_variable(val,scope='global')
						if is_negative :
							data = '-' + data
							data = self.minus_minus_plus(data)
						self.compiler.assign_value(key,data,scope=self.scope,scope_name=self.scope_name)
						continue
						
				
				if self.outer_scope :
					
					if val in self.compiler.Variables['local']['local_scope'][self.outer_scope].keys() :
						data,dt = self.compiler.fetch_variable(val,scope=self.scope,scope_name=self.outer_scope)
						if data == '' or data == None :
							pass
						else :
							if is_negative :
								data = '-' + data
								data = self.minus_minus_plus(data)
							self.compiler.Variables['local']['local_scope'][self.scope_name][key] = [data,dt]
							continue
				
				if val in self.compiler.Variables['global'].keys() :
					v,dt = self.compiler.Variables['global'][val]
					if v == '' or v == None :
						continue
					if is_negative :
						v = '-' + v
						v = self.minus_minus_plus(v)
					self.compiler.assign_value(key,v,scope='local',scope_name=self.scope_name)
					continue

				"""
				if val in self.compiler.Variables['local']['local_scope'][self.scope_name].keys() :
					data,dt = self.compiler.fetch_variable(val,scope='local',scope_name=self.scope_name)
					if data != '' or data != None :
						if is_negative :
							data = '-' + data
							data = self.minus_minus_plus(data)
						self.compiler.Variables['local']['local_scope'][self.scope_name][val] = [data,dt]
						continue
				"""
				

				"""	
				if self.format_negative_variables(val) :
					name = self.format_negative_variables(val)
					v,dt = self.fetchValue(name)
					v = '-'+v
					self.compiler.assign_value(key,v,scope='local',scope_name=self.scope_name)
					continue
				"""
				print("error param {} is not given any defined value or variable {}".format(key,val))
				return
			#print(self.compiler.Variables['local']['local_scope'][name]
			v = self.execute(self.head)
			if type(v) == type([1]) :
				if len(v) == 1 :
					return v[0]
					
			return v

		y = line[0]
		if line[1] != '=' :
			print("Invalid Syntax from FPU {}".format(line))
			return
		fun = line[2]
		
		name,param,found = extract_name_param(fun)
		
		if name != self.head.name :
			print("Error function {} is not defined".format(name))
			return

		params_val = split(param,',')
		params = self.head.params.split(',')
		#print(self.compiler.Variables['local']['local_scope'][name])
		#f(x,y)
		#f(1,2)
		#params_val = [1,2]
		#params = [x,y]
		Vars = self.compiler.Variables['local']['local_scope'][self.scope_name]
		
		for val,key in zip(params_val,params) :
			key = key.split()[1]
			is_negative = False
			
			if self.compiler.is_function(val) :
				
				val = self.compiler.execute_Functions(val,scope=self.scope,scope_name=self.scope_name)
				self.compiler.assign_value(key,val,scope=self.scope,scope_name=self.scope_name)
				continue
				
			if self.compiler.get_arr_index(val) and not '.' in val :
				try :
					val,_ = self.compiler.process_array(val,scope=self.scope,scope_name=self.scope_name)
				except :
					if self.outer_scope == 'global' :
						val,_ = self.compiler.process_array(val,scope='global')
					else :
						val,_ = self.compiler.process_array(val,scope=self.scope,scope_name=self.outer_scope)
				self.compiler.assign_value(key,val,scope=self.scope,scope_name=self.scope_name)
				continue
				
			if self.compiler.is_number(val) :
				self.compiler.assign_value(key,val,scope='local',scope_name=self.scope_name)
				continue
				
			
			if len(condition_split(val,'any')) > 1 :
				val = self.compiler.compute_index(val,scope='local',scope_name=self.scope_name)
				self.compiler.assign_value(key,val,scope='local',scope_name=self.scope_name)
				continue
				
			if '.' in val :
				val_ = self.compiler.line_to_execute(val,'local',self.scope_name,'accessing_attributes')
				if val_ == None :
					if self.outer_scope :
						val_ = self.compiler.line_to_execute(val,'local',self.outer_scope,'accessing_attributes')
				self.compiler.assign_value(key,val_,scope='local',scope_name=self.scope_name)
				continue
				
			if self.format_negative_variables(val) :
				val  = self.format_negative_variables(val)
				is_negative = True
				
			if self.outer_scope == self.scope_name :
				if val in Vars.keys() :
					data,dt = self.compiler.fetch_variable(val,scope='local',scope_name=self.scope_name)
					if is_negative :
						data = '-' + data
						data = self.minus_minus_plus(data)
					self.compiler.Variables['local']['local_scope'][self.scope_name][key] = [data,dt]
					#self.compiler.assign_value(key,data,scope='local',scope_name=self.scope_name)
					continue
				if val in self.compiler.Variables['global'].keys() :
					data,dt = self.compiler.fetch_variable(val,scope='global')
					if is_negative :
						data = '-' + data
						data = self.minus_minus_plus(data)
					self.compiler.Variables['global'][key] = [data,dt]
					#self.compiler.assign_value(key,data,scope='local',scope_name=self.scope_name)
					continue
			
			
			if self.outer_scope :
				if val in self.compiler.Variables['local']['local_scope'][self.outer_scope].keys() :
					data,dt = self.compiler.Variables['local']['local_scope'][self.outer_scope][val]
					if data != '' or data != None :
						if is_negative :
							data = '-' + data
							data = self.minus_minus_plus(data)
						self.compiler.Variables['local']['local_scope'][self.scope_name][key] = [data,dt]
						continue
						
			
			if val in self.compiler.Variables['global'].keys() :
				v,dt = self.compiler.Variables['global'][val]
				if v == '' or v == None :
					pass
				else :
					if is_negative :
						v = '-' + v
						v = self.minus_minus_plus(v)
						v = str(float(v))
					self.compiler.Variables['local']['local_scope'][self.scope_name][key] = [v,dt]
					continue
			"""
			
			if val in self.compiler.Variables['local']['local_scope'][self.scope_name].keys() :
				data,dt = self.compiler.fetch_variable(val,scope=self.scope,scope_name=self.scope_name)
				if data == '' or data == None :
					pass
				else :
					if is_negative :
						data ='-' + data
						data = self.minus_minus_plus(data)
						data = str(float(data))
					self.compiler.Variables['local']['local_scope'][self.scope_name][val] = [data,dt]
					continue
			"""
			
				
			#if val in self.compiler.Variables['local']['local_scope'][self.scope_name].keys() :
				#v,dt = self.compiler.Variables['local']['local_scope'][self.scope_name][val]
				#self.assign_value(key,v,scope='local',scope_name=self.scope_name)
				#continue
				
			


			"""
			if self.format_negative_variables(val) :
				v = self.format_negative_variables(val)
				v,dt = self.compiler.fetch_variable(v,scope='local',scope_name=self.scope_name)
				v = '-'+v
				self.compiler.Variables['local']['local_scope'][self.scope_name][val] = [v,dt]
			"""
			print("Error parameter {} is not given any value that is defined {} ".format(key,val))
			
			
		v = self.execute(self.head)
		if type(v) == type(['1']) :
			if len(v) == 1 :
				return v[0]
		return v
		
	def execute(self,node=None) :
		if node :
			for line in node.body :
				if type(line) == type('a') :
					if line.split()[0] == 'return' :
						l = line.split()
						if len(l) == 1 :
							return 1
						vals = l[1]
						return_list = []
						if len(condition_split_v2(vals,'any')) > 1 :
							#has arithmetic op
							val = self.compiler.compute_index(vals,scope='local',scope_name=self.scope_name,type='float')
							return val
						if self.compiler.is_function(vals) :
							name,params,_ = self.compiler.get_func_param(vals)
							if name in self.compiler.functions.keys() :
								func = self.compiler.functions[name]
								func.outer_scope = self.scope_name
								return func.executeTree(vals)
							if name in self.compiler.func_body.keys() :
								return self.compiler.process_functions(vals,scope=self.scope,scope_name=self.scope_name,exe=True)
						vals = vals.split(',')
						for val in vals :
							if self.compiler.is_number(val) :
								return_list.append(val)
								continue
							return_list.append(self.fetchValue(val)[0])
						return return_list
				if type(line) == type(self.For) :
					line.executeTree(line.loop_node)
					continue
				if type(line) == type(self.cpu) :
					v = line.executeTree(line.head)
					if v :
						return v
					continue
				if type(line) == type(node) :
					v = self.execute(line)
					if v :
						return v
					continue
				self.compiler.ProcessLine(line,scope='local',scope_name=self.scope_name)