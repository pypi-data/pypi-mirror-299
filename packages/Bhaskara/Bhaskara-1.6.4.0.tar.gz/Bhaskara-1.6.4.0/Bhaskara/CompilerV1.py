import sys
sys.setrecursionlimit(10**2)
import random

from ExpressionTree1 import ExpressionTree
from FunctionalProcessingUnit import FunctionProcessingUnit as FPU
from LoopProcessingUnit2 import LoopProcessingUnit
from ConditonalProcessingUnit import ConditionalProcessingUnit as CPU
from StringAlgorithm.ConditionSplit import  condition_split
from StringAlgorithm.TokenizeVariableDefinition import tokenize_defining_variable
from IOSTREAM.InputOutput import InputOutputStream as iostream
from ProcessSetElements import process_logic_element
from ProcessFunction import  process_functions
from StringAlgorithm.ExtractFuncNameParams import extract_name_param
from StringAlgorithm.SplitString import split
from ClassProcessingUnit import accessing_attributes
from ClassProcessingUnit import ClassProcessingUnit as CLSPU


class Compiler :
	
	def __init__(self,indent=4) :
		self.indent = indent
		self.loop_types = ['for','while']
		self.DataTypes = ['int','float','chars','let']
		self.ArrayDataTypes = ['int_arr','float_arr']
		self.int_literals = '0123456789'
		self.logic_elements = '∈∀∅∃∧∨∉'
		self.element = self.logic_elements[0]
		self.mathematical_constants = {'π' : 3.14159265,'ë' : 2.71828182}
		self.alpha = 'abcdefghijklmnopqrstuvwxyz'
		self.char_literals = 'abcdefghijklmnopqrstuvwxyz' + self.int_literals+'*/+-_^'
		self.variable_error = "Error variable {} is not defined "
		self.value_error = "Incorrect value {}assigned to the variable {}"
		self.break_statement  = 'over'
		self.continue_statement = 'skip'
		self.comment_syntax = '%'
		self.symbols = ["'",' ','.',">",'<','<=','=','/','?','*','-']
		self.iostream = iostream(self)
		self.func_body = {}
		self.functions = {}
		self.localVariables = {}
		self.func_scope = {}
		self.arithmetic_op = ['+','-','*','/','^']
		self.loop_scope = {}
		self.special_variables = '∆≠≥≤<'
		self.char_literals = self.char_literals + self.special_variables
		self.local_scope = {'func_scope' : self.func_scope,'loop_scope':self.loop_scope}
		self.localVariables = {'local_scope' : self.local_scope}
		self.globalVariables = {}
		self.Variables = {'global' : self.globalVariables,'local' : self.localVariables}
		self.literals = {'int' :self.int_literals,'float' : self.int_literals,'chars' : self.char_literals}
	
	def check_variable_name(self,name) :
		if name == '' :
			print("Error Name has not provided to the variable")
			return False
		if name[0].lower() in self.alpha +'_' :
			for i in range(1,len(name)) :
				if not name[i].lower() in self.alpha+self.int_literals+'_' :
					return False
			return True
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
		ob_count = 0
		is_found = False
		N = len(line)
		
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
		if self.check_variable_name(name) :
				is_var = True
		if is_var :
			if scope == 'local' :
				var_scope = self.Variables[scope]['local_scope'][scope_name]
				if name in var_scope.keys() :
					val,_ = var_scope[name]
					return val
				if name in self.Variables['global'].keys() :
					val,_ = self.Variables['global'][name]
					return val
				#print("Error from fetch_var_value variable {} is not defined".format(name))
				return
			if scope == 'global' :
				if name in self.Variables[scope].keys() :
					val,_ = self.Variables[scope][name]
					return val
				#print("Error variable from fetch_var_value {} is not defined ".format(name))
				return
			return name
	
	def is_number(self,num) :
		is_num = True
		try :
			num = float(num)
			return True
		except :
			return False
		
		for n in num :
			if n == '.' :
				continue
			if not n in self.int_literals :
				is_num = False
				break
		return is_num
	
	def process_functions(self,line,scope='global',scope_name='',exe=False) :
			#func f(x) = 2*x+3
			if type(line) == type('a') :
				line = line.split()
			
			if len(line) == 1 and exe :
				#f(x)
				#f(3,x)
				if not self.is_function(line[0]) :
					return
				line = line[0]

				name,params,_ = extract_name_param(line)
				params = split(params,',')
				if not name in self.func_body.keys() :
					return
				params_value = []

				for param in params :
					if self.is_number(param) :
						params_value.append(param)
					if self.is_function(param) :
						params_value.append(self.execute_Functions(param,scope=scope,scope_name=scope_name))
					elif self.check_variable_name(param) :
						
						val,_ = self.fetch_variable(param,scope=scope,scope_name=scope_name)
						params_value.append(val)
				params_key = self.func_body[name]['params']
				
				for key,val in zip(params_key,params_value) :
					self.Variables['local']['local_scope']['func_'+name][key] = [val,'float']
				
				expression = self.func_body[name]['expression']
				
				tree = ExpressionTree(scope='local',scope_name='func_'+name,obj=self)
				tree.buildTree(expression)
				value = tree.computeTree(tree.head)
				return str(value)
				
			if len(line) == 4 :
				#func f(x) = 2*x
				if line[0] != 'func' :
					return
				name,params,_ = self.get_func_param(line[1])
				params = params.split(',')
				
				if not self.check_variable_name(name) :
					return
				
				self.func_body[name] = {}
				self.func_body[name]['params'] = params
				self.func_body[name]['expression'] = line[-1]
				
				self.Variables['local']['local_scope']['func_'+name] = {}
				
				return
				
			
	
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
					print("Error from process_func variable  {} is not defined".format(var_y))
					return	
			if scope == 'global' :
				if not var_y in self.Variables['global'].keys() :
					print("Error from process_unit variable  {} is not defined".format(var_y))
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
						print("Error variable from process_func unit {} is not defined".format(p))
						return
					if scope == 'global' :
						if p in self.Variables['global'].keys() :
							v,_= self.Variables['global'][p]
							param_dict[params_[i]] = v
							continue
						#print("Error variable {} is not defined".format(p))
						return
				param_dict[params_[i]] = params[i]
				
			tree = self.func_body[name][0]
			tree.param_values = param_dict
			value = str(tree.computeTree(tree.head))
			_,dt = var_scope[var_y]
			var_scope[var_y] = [value,dt]
			return True
			
	def process_Func(self,line,scope='global',scope_name='') :
			#y = pow(x)
			#where pow is a multiline function
			line = line.split()
			
			
			if len(line) == 1 :
				#pow(x,r)
				if self.is_function(line[0]) :
					name,_,_ = self.get_func_param(line[0])
					if name in self.functions.keys() :
						func = self.functions[name]
						if scope_name :
							func.outer_scope = scope_name
						return func.executeTree(line[0])
				return
			
			# y = 2*pow(x)
			if len(line) != 3 :
				return
				
			if not self.get_func_param(line[-1]) :
				return
			
			func_name = line[-1]
			name,param,_ = self.get_func_param(func_name)
			func = None
			if name in self.functions.keys() :
				func = self.functions[name]
				val = None
			else :
				return

			if len(condition_split(line[-1],'any')) > 1 :

					val = str(self.compute_index(line[-1],scope=scope,scope_name=scope_name,type='float'))
					if self.get_arr_index(line[0]) :
						self.process_array(line,scope=scope,scope_name=scope_name)
						return
					self.assign_value(line[0],val,scope=scope,scope_name=scope_name)
					return
					
			func.outer_scope = scope_name
			val = func.executeTree(line)
			var_y = line[0]
			
			if self.get_arr_index(var_y) :
					#arr[index] = func(y)
				name,index,_ = self.get_arr_index(var_y)
				if len(index.split(',')) == 2 :
					#this means var_y is an 2-d array
					row,col = self.compute_coords(index.split(','),scope=scope,scope_name=scope_name)
					self.assign_2darray(name,val,x=row,y=col,scope=scope,scope_name=scope_name)
					return
				if len(condition_split(index,'any')) > 1 :
					index = self.compute_index(index,scope=scope,scope_name=scope_name)
				elif self.check_variable_name(index) :
					index = self.fetch_var_value(index,scope=scope,scope_name=scope_name)
					index = int(index)
					self.assign_array(name,val,index=index,scope=scope,scope_name=scope_name)
					return
				
					
			self.assign_value(var_y,val,scope=scope,scope_name=scope_name)
			return
			"""
			if scope == 'global' :
				if var_y in self.Variables['global'].keys() :
					_,dt = self.Variables['global'][var_y]
					val = self.format_literals(dt,str(val))
					self.Variables['global'][var_y] = [val,dt]
					return
				
			if scope == 'local' :
				if scope_name :
					if var_y in self.Variables['local']['local_scope'][scope_name].keys() :
						self.assign_value(var_y,val,scope=scope,scope_name=scope_name)
						return	
			
			
			if var_y in self.Variables['local']['local_scope'][name].keys() :
				_,dt = self.Variables['local']['local_scope'][name][var_y]
				val  = self.format_literals(dt,str(val))
				self.Variables['local']['local_scope'][name][var_y] = [val,dt]
				return
			if var_y in self.Variables['global'].keys() :
				_,dt = self.Variables['global'][var_y]
				val  = self.format_literals(dt,str(val))
				self.Variables['global'][var_y] = [val,dt]
				return
			else :
				return
			"""
			
	def clean_line_from_op(self,line) :
		clean_line = ''
		for l in line :
			if l in self.arithmetic_op :
				clean_line += " "
				continue
			clean_line += l
		return clean_line
	
	def get_arr_index(self,arr) :
		if self.is_a_number(arr) :
			return False
		if len(arr) == 0 :
			return False
			
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
	
	def is_char(self,value) :
		if len(value) < 2 :
			return False
		if value[0] == "'" and value[-1] == "'" :
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
	
	def is_variable_in_scope(self,var,scope='global',scope_name='') :
		if scope == 'local' :
			if var in self.Variables[scope]['local_scope'][scope_name].keys() :
				return True
			return False
		if var in self.Variables['global'].keys() :
			return True
		return False
	
	def fetch_variable(self,var,scope='global',scope_name='') :
		if scope == 'global' :
			return self.Variables[scope][var]
		if var in self.Variables['local']['local_scope'][scope_name].keys() :
			data,dt = self.Variables['local']['local_scope'][scope_name][var]
			if data != None :
				return data,dt
		return self.fetch_variable(var,scope='global')
		
	def assign_array(self,name,value,index=None,scope='global',scope_name="") :
		if index != None :
			if scope == 'local' :
				if name in self.Variables['local']['local_scope'][scope_name].keys() :
					elements,dt = self.Variables['local']['local_scope'][scope_name][name]
					elements[index] = self.format_literals(dt[:3],value)
					self.Variables['local']['local_scope'][scope_name][name] = [elements,dt]
					return
			if name in self.Variables['global'].keys() :
				elements,dt = self.fetch_variable(name,scope='global')
				elements[index] = self.format_literals(dt[:3],value)
				self.Variables['global'][name] = [elements,dt]
				return
		if name in self.Variables['global'].keys() :
			elements,dt = self.fetch_variable(name,scope='global')
			elements[index] = self.format_literals(dt[:3],value)
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
			if type(val) == type('a') :
				val = self.format_literals(dt,val)
			self.Variables[scope][var] = [val,dt]
			return
		if var in self.Variables[scope]['local_scope'][scope_name].keys() :
			_,dt  = self.Variables[scope]['local_scope'][scope_name][var]
			if type(val) == type('a') :
				val = self.format_literals(dt,val)
			self.Variables[scope]['local_scope'][scope_name][var] = [val,dt]
			return
		return self.assign_value(var,val,scope='global')
		
	def compute_index(self,index,scope='global',scope_name='',type='int') :
		if index :
			if self.is_number(index) :
				return int(index)
			has_op = False
			val = condition_split(index,'any')
			if len(val) > 1 :
				has_op = True
			del val
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
			if type == 'let' :
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
		
		
	def is_2darray(self,name) :
		count_brackets = 0
		index = ''
		found_bracket = False
		
		for char in name :
			if char == '[' :
				found_bracket = True
				continue
			if char == ']' :
				break
			if found_bracket :
				index += char
		if len(index.split(',')) == 2 :
			return True
		return False
		
	def get_2darray(self,line) :
		#arr[i+1][j-1]
		row = ""
		column = ""
		name = ""
		count_b = 0
		
		for char in line :
			have_found_b = False
			if char == '[' :
				have_found_b = True
				count = count + 1
				continue
			if char == ']' :
				have_found_b = False
				continue
			if have_found_b :
				if count == 1 :
					row += char
				else :
					column += char
			name += char
		
		return name,row,column
	
			
	def fetch_2darray_element(self,value,data_type) :
		row_elements = []
		column_elements = []
		N = len(value)
		count_b = 0
		for i,v in enumerate(value) :
			if v == '(' :
				column_elements  = []
				count_b = 1
				continue
			if v == ')' :
				if i+1 >= N :
					break
				row_elements.append(column_elements)
				count_b = 0
				continue
			if count_b :
				if v == ',' :
					continue
				v =self.format_literals(data_type[:3],v)
				column_elements.append(v)
				
		return row_elements
		
	def compute_coords(self,coords : list,scope='global',scope_name='',another_scope='') :
		if coords == [] :
			return
		row,column = coords
		compute_row = compute_col = False
		
		if len(condition_split(row,'any')) > 1 :
			row = self.compute_index(row,scope=scope,scope_name=scope_name)
			compute_row = True
		if len(condition_split(column,'any')) > 1 :
			column = self.compute_index(column,scope=scope,scope_name=scope_name)
			compute_col  = True
		
		if not compute_row :
			if self.is_number(row) :
				row = int(float(row))
			elif self.check_variable_name(row) :
				row = self.fetch_var_value(row,scope=scope,scope_name=scope_name)
				row = int(float(row))
		
		if not compute_col :
			if self.is_number(column) :
				column = int(float(column))
			elif self.check_variable_name(column) :
				column = self.fetch_var_value(column,scope=scope,scope_name=scope_name)
				column = int(float(column))
		
		return row,column
		
	def assign_2darray(self,name,val,x=None,y=None,scope='global',scope_name='') :
		
		elements,dt = self.fetch_variable(name,scope=scope,scope_name=scope_name)
		elements[x][y] = self.format_literals(dt[:3],val)
		
		if scope == 'local' :
			if name in self.Variables['local']['local_scope'][scope_name].keys() :
				self.Variables['local']['local_scope'][scope_name][name] = [elements,dt]
				return
			if name in self.Variables['global'].keys() :
				self.Variables['global'][name] = [elements,dt]
				return
		
		if name in self.Variables['global'].keys() :
			self.Variables['global'][name] = [elements,dt]
		return
			
	
	def fetch_2darray(self,name,scope='global',scope_name='') :
		if scope == 'global' :
			if name in self.Variables['global'].keys() :
				return self.Variables['global'][name]
		if name in self.Variables['local']['local_scope'][scope_name].keys() :
			return self.Variables['local']['local_scope'][scope_name][name]
		return self.fetch_2darray(name,scope='global')
		
	def process_array(self,line,scope='global',scope_name='',class_obj=None,another_scope='') :
		if type(line) == type('a') :
			line = line.split()
		#int_arr arr[] = (1,2,3,4,5,6)
		#arr[6] = 7
		#arr = (1,2,3,4,5)
		#int2d_arr array[][] = ((1,2,3,4,5),(6,7,8,9,10))
		
		if '∈' in line :
			return
		
		if len(line) == 1 :
			#arr[i]
			# i E W
			
			if self.is_2darray(line[0]) :
				#2d array
				#arr[i,j]
				if not self.get_arr_index(line[0]) :
					return
				name,coords,_ = self.get_arr_index(line[0])
				row,column = coords.split(',')
				row,column  = self.compute_coords((row,column),scope=scope,scope_name=scope_name,another_scope=another_scope)
				elements,dt = self.fetch_2darray(name,scope=scope,scope_name=scope_name)
				m,n = len(elements),len(self.to_int(elements[0]))
				
				if row > m or column > n:
					print('IndexOutofBoundError [{},{}]'.format(m,n))
					return
				
				return elements[row][column],dt
						
			
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
			#int_arr arr[5+1] = (1,2,3,4,5)
			#int row = arr[1]

			if line[0] in self.DataTypes :
				value = None
				new_line = None
				if len(condition_split(line[3],'any')) > 1 :
					try :
						value = self.compute_index(line[3],scope=scope,scope_name=scope_name,type='float')
						new_line = line[0] + ' ' + line[1] + ' ' + line[2]+ ' '+str(value)
						self.process_variable(new_line,scope=scope,scope_name=scope_name)
					except :
						pass
						
				elif self.get_arr_index(line[3]) :
					value,_ = self.process_array(line[3],scope=scope,scope_name=scope_name)
					new_line = line[0] +'  '+ line[1] +'  '+ line[2]+'  ' + str(value)
					self.process_variable(new_line,scope=scope,scope_name=scope_name)
				return
			
			if line[0] in self.ArrayDataTypes :
				data_type = line[0]
				name = line[1]
				
				if self.is_2darray(name) :
					#int_arr arr[2,7]  = ((1,2,3,4,5,6,7),(8,9,10,11,12,13,14))
					name,coords,_ = self.get_arr_index(name)
					coords = coords.split(',')
					self.check_variable_name(name)
					value = line[3]
					elements = None
					if self.check_variable_name(value) :
						elements = self.fetch_var_value(value,scope=scope,scope_name=scope_name)
					else :
						elements = self.fetch_2darray_element(value,data_type)
					m,n = len(elements),len(elements[0])
					row,column = self.compute_coords(coords,scope=scope,scope_name=scope_name)
					
					if row > m or column > n :
						print('error the index entered at the time of initialising the array is wrong')
						return
					
					self.define_variable(name,elements,data_type,scope=scope,scope_name=scope_name)
					if class_obj :
						class_obj.head.body[name] = elements
					return True
				
				is_arr= self.get_arr_index(name)
				if not is_arr :
					return
				name,index,_ = self.get_arr_index(name)
				index = self.compute_index(index,scope=scope,scope_name=scope_name)
				temp_elements = ''
				count = 0
				if self.check_variable_name(line[-1]) :
					line[-1] = self.fetch_var_value(line[-1],scope=scope,scope_name=scope_name)
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
					print("Syntax error from process_array {}".format(line))
					return
				if index :
					if index != len(elements_delta) :
						print("index {} does not match the number of elements in the array {}".format(index,elements_delta))
						return
				if scope == 'local' :
					self.Variables['local']['local_scope'][scope_name][name] = [elements_delta,data_type]
					if class_obj :
						class_obj.head.body[name] = elements_delta
					return True
				self.Variables['global'][name] = [elements_delta,data_type]
				return True
		
		if len(line) == 3 :
			# y = arr[i]
			#arr[i] = y
			# t = arr[]
			#res = 2+arr[i]
			#y = arr[i,j]
			#arr[i] = f(x)
			y = line[0]
			arr = line[2]
			clean_line = condition_split(arr,'any')
			have_arr = False
			
			for element in clean_line+[y] :
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
				#var = var*arr[i-k]
				is_2d = False
				row  = column = None
				tree = ExpressionTree(Variables=self.Variables,scope=scope,scope_name=scope_name,obj=self)
				tree.buildTree(arr)
				val  = str(tree.computeTree(tree.head))
				#if y is an array then this will be executed
				if self.get_arr_index(y) :
					
					name,index_y,_ = self.get_arr_index(y)

					if len(index_y.split(',')) > 1 :
						is_2d = True
						row,column = index_y.split(',')
						row,column = self.compute_coords((row,column),scope=scope,scope_name=scope_name)
						#arr[i,j] = arr[k+1,h+1]
						self.assign_2darray(name,val,x=row,y=column,scope=scope,scope_name=scope_name)
						return
					
					else :	
						return_value = condition_split(index_y,'any')
					
					if len(return_value) > 1 :
						index_y = self.compute_index(index_y,scope=scope,scope_name=scope_name)
					
					elif self.is_number(str(index_y)) :
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
				
				value_found = False
				name,index,_ = self.get_arr_index(y)
				val = None
				is_2d = False
				if self.is_2darray(y) :
					is_2d = True
				row=column = None
				
				if self.get_arr_index(arr) :
					#arr[i,j] = arr[j,k]
					#arr[i,j] = arr[k]
					val,_ = self.process_array(arr,scope=scope,scope_name=scope_name)
					
				if self.is_2darray(y) :
					index = index.split(',')
					row,column = self.compute_coords(index,scope=scope,scope_name=scope_name)

				else :
					index = self.compute_index(index,scope=scope,scope_name=scope_name)
					
				elements,dt  = self.fetch_variable(name,scope=scope,scope_name=scope_name)

				if self.is_number(arr) :
					if is_2d :
						self.assign_2darray(name,arr,x=row,y=column,scope=scope,scope_name=scope_name)
						return True
					self.assign_array(name,arr,index=index,scope=scope,scope_name=scope_name)
					return True
				
				if self.check_variable_name(arr) :
					arr,_ = self.fetch_variable(arr,scope=scope,scope_name=scope_name)
					value_found = True
					val = arr
				
				if is_2d :
					if value_found :
						self.assign_2darray(name,arr,x=row,y=column,scope=scope,scope_name=scope_name)

				elif self.is_function(arr) :
					name_,params,_ = self.get_func_param(arr)
					val = None
					if name_ in self.func_body.keys() :
						val = self.process_functions(arr,scope=scope,scope_name=scope_name,exe=True)
					elif name_ in self.functions.keys() :
						func = self.functions[name]
						func.outer_scope = scope_name
						val = func.executeTree(arr)
					
					if is_2d :
						self.assign_2darray(name,val,scope=scope,x=row,y=column,scope_name=scope_name)
						return True
					self.assign_array(name,val,index=index,scope=scope,scope_name=scope_name)
					return True
					
				elif self.get_arr_index(arr) :
					
					#arr[i] = arr[j]
					#arr[i,j] = arr[k,l]
					#arr[i,k] = arr[j]
					#arr[k] = arr[k,l]
					name_j,j_index,_= self.get_arr_index(arr)
					row = column = None
					
					if len(j_index.split(',')) > 1 :
						value = self.process_array(arr,scope=scope,scope_name=scope_name)
						#in case if y is a 2 dimensional array
						if self.is_2darray(y) :
							row,column = self.compute_coords(index.split(','),scope=scope,scope_name=scope_name)
							self.assign_2darray(name,value,x=row,y=column,scope=scope,scope_name=scope_name)
							return
						self.assign_array(name,value,index=index,scope=scope,scope_name=scope_name)
						return
							
					else :
						j_index = self.compute_index(j_index,scope=scope,scope_name=scope_name)
						j_arr = self.get_arr_element(name_j,j_index,scope=scope,scope_name=scope_name)
						
						if self.is_2darray(y) :
							row,column = self.compute_coords(index.split(','),scope=scope,scope_name=scope_name)
							self.assign_2darray(name,j_arr,x=row,y=column,scope=scope,scope_name=scope_name)
							return
						
						elements[index] = j_arr
						
					if scope == 'local' :
						self.Variables[scope]['local_scope'][scope_name][name] = [elements,dt]
					else :
						self.Variables[scope][name] = [elements,dt]
					#self.assign_array(name,j_arr,index=index,scope=scope,scope_name=scope_name)
					return
					

				if not value_found :
					return
				
				if self.is_2darray(y) :
					if type(index) == type('a') :
						index = index.split(',')
					row,column = self.compute_coords(index,scope=scope,scope_name=scope_name)
					self.assign_2darray(name,arr,x=row,y=column,scope=scope,scope_name=scope_name)
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
		
	def is_a_number(self,n) :
		try :
			float(n)
			return True
		except :
			return False
		
	def is_function(self,line) :
		if self.is_a_number(line) :
			return False
			
		
		if not '=' in line :
			name,_,_ = extract_name_param(line)
			if name in self.functions.keys() :
				return True
			if name in self.func_body.keys() :
				return True
			return False
			
			if len(line) == 2 :
				return True
			return False
		if type(line) == type('a') :
			line = line.split('=')
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
				return False
		return True
		
	def check_char_literals(self,var,value) :
		if value[0] != "'" or value[-1] != "'"  :
			return
		for v in value :
			if v in self.symbols :
				continue
			if not v.lower() in self.char_literals + self.int_literals :
				return False
		return True
		
	def format_char_literals(self,chars) :
		if chars == '' :
			return chars
		line = ''
		for i,char in enumerate(chars) :
			if i + 1 == len(chars) :
				line += char
				break
			line += char
			line += ' '
		return line
		
	def has_negative_sign(self,num) :
		if self.is_a_number(num) :
			num  = str(num)
		if num[0] == '-' :
			for op in ['*','/','+','^'] :
				if op in num :
					return False
			return True
		return False
	
	def format_negative_number(self,num) :
		if self.is_a_number(num) :
			num = str(num)
		if num[0] == '-' :
			return num[1:]
		return num
		
	def minus_minus_plus(self,num) :
		if len(num) >= 3 :
			if num[0] == '-' and num[1] == '-' :
				return num[2:]
		return num
	
	def print_scope_body(self,scope='local',scope_name='') :
		if scope == 'global' :
			print(self.Variables['global'])
			return
		if scope_name == '' :
			return
		print(self.Variables[scope]['local_scope'][scope_name])
	
	def format_literals(self,data_type,num) :
		if data_type == 'int' :
			
			if type(num) == type([1]) :
				for i,row in enumerate(num) :
					if type(row) == type([1]) :
						for j,col in enumerate(row) :
							if '.' in col :
								col = str(col)
								num[i][j] = col.split('.')[0]
					else :
						if '.' in row :
							num[i] = row.split('.')[0]
				return num
			num = str(num)
			if '.' in num :
				return num.split('.')[0]
			return num
		
		if data_type in ['float','let'] :
			if type(num) == type([1]) :
				for i,row in enumerate(num) :
					if type(row) == type([1]) :
						for j ,col in enumerate(row) :
							col = str(col)
							if not '.' in col :
								num[i][j] = col+'.0'
					else :
						if not '.' in row :
							num[i] = row +'.0'
				return num
			num = str(num)		
			if not '.' in num :
				num = num + '.0'
			return num
		return num
		
		
		
	def process_variable(self,line,scope='global',scope_name='',class_obj=None) :
		if self.is_array(line.split('=')) :
			return
		if self.is_function(line) :
			return
		if '∈' in line :
			return
		save = line
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
					
			if data_type in ['int','float','let'] :
				has_operator = False
				is_negative = False
				
				val = condition_split(value,'any')
				if len(val) > 1 :
					has_operator = True
				del val
				
				if has_operator :
					value = str(self.compute_index(value,scope=scope,scope_name=scope_name,type='float'))
				#DataType Variable_a = variable_b
				#int a = b  
				#int a = f(x)
				#int element = arr[1]
				
				elif self.is_function(value) :
					name_,params,_ = self.get_func_param(value)
					
					if name_ in self.func_body.keys() :
						value = self.process_functions(value,scope=scope,scope_name=scope_name,exe=True)
					elif name_ in self.Variables['local']['local_scope'].keys() :
						func = self.functions[name_]
						func.outer_scope = scope_name
						value = func.executeTree(value)
				
				elif self.get_arr_index(value) :
					value,_ = self.process_array(value,scope=scope,scope_name=scope_name)
					value = str(value)
				else :
					is_negative = False
					
					if self.has_negative_sign(value) :
						value = self.format_negative_number(value)
						is_negative = True
						
					if self.check_variable_name(value) :
						value = self.fetch_var_value(value,scope=scope,scope_name=scope_name)
	
					if value in self.mathematical_constants.keys() :
						value = str(self.mathematical_constants[value])
						
					if is_negative :
						value = '-' + value
						value = self.minus_minus_plus(value)
						
				
				value = self.format_literals(data_type,value)
				self.define_variable(name,value,data_type,scope=scope,scope_name=scope_name)
				if class_obj :
					class_obj.head.body[name] = value
				return True
				
			if data_type == 'chars' :
				value = self.format_char_literals(line[3:])
				if not self.check_char_literals(name,value) :
					return
				self.define_variable(name,value,data_type,scope=scope,scope_name=scope_name)
				if class_obj :
					class_obj.head.body[name] = value
				return True
				
		if N == 3 :
			# a = 3
			if len(line) >= 4 :
				if line[0] in self.ArrayDataTypes or line[0] in self.DataTypes :
					return
			
			if scope == 'local' :
				if scope_name == '' :
					 print("Error from process_variable unit please provide the name of the scope ")
					 return
			
				
				name = line[0]
				value = line[2]
				
				if value in self.mathematical_constants.keys() :
					value = str(self.mathematical_constants[value])
					
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
				   
				   if data_type in self.DataTypes :
				   	has_operator = False
				   	val = condition_split(value,'any')
				   	if len(val) > 1 :
				   		has_operator = True

				   	if has_operator :
				   	    value = str(self.compute_index(value,scope=scope,scope_name=scope_name,type='float'))
				   	    
				   	
				   	if self.is_function(value) :
				   		name_,params,_ = self.get_func_param(value)
				   		if name_ in self.func_body.keys() :
				   			value = self.process_functions(value,scope=scope,scope_name=scope_name,exe=True)
				   			value = str(value)
				   	
				   	if not self.check_number_literals(name,value) :
				   		return
				   	value = self.format_literals(data_type,value)
				   	self.assign_value(name,value,scope=scope,scope_name=scope_name)
				   	return True
				   if data_type == 'chars' :
				       value = self.format_char_literals(line[2:])
				       if not self.check_char_literals(name,value) :
				       	return
				       self.assign_value(name,value,scope=scope,scope_name=scope_name)
				       return True
				else :
					 #line = self.format_char_literals(line)
					# return self.process_variable(line,scope='global'))
					 #res = res*i
					 if name in self.Variables['global'].keys() :
					 	_,data_type = self.Variables['global'][name]
					 	
					 	if data_type in ['int','float','let'] :
					 		has_op = False
					 		val = condition_split(value,'any')
					 		
					 		if len(val) > 1 :
					 			has_op = True
					 				
					 		if has_op :
					 			value = str(self.compute_index(value,scope=scope,scope_name=scope_name,type='float'))
					 			
					 		if self.is_function(value) :
					 			name_,params,_ = self.get_func_param(value)
					 			if name_ in self.func_body.keys() :
					 				value = self.process_functions(value,scope=scope,scope_name=scope_name,exe=True)
					 				value = str(value)
					 				
					 		if not self.check_number_literals(name,value) :
					 			return
					 		value = self.format_literals(data_type,value)
					 		self.assign_value(name,value,scope=scope,scope_name=scope_name)
					 		return True
					 	if data_type == 'chars' :
					 		value = self.format_char_literals(line[2:])
					 		if not self.check_char_literals(name,value) :
					 			return
					 		self.assign_value(name,value,scope=scope,scope_name=scope_name)
					 		return True	
					 print("Error from process_variable unit assigning value before defining a variable {}".format(line))
					 return
			if scope == 'global' :
				if line[0] in self.ArrayDataTypes :
					return
				if self.is_function(save) :
					return

				name = line[0]
				value = line[2]
				
				if value in self.mathematical_constants.keys() :
					value = str(self.mathematical_constants[value])
					
				
				if line[1] != '=' :
					print("Syntax  Error from process_variable {}".format(line))
					return	
				if name in self.Variables[scope].keys() :
					_,data_type = self.Variables[scope][name]
					if data_type in self.DataTypes :
						has_operator = False
						val = condition_split(value,'any')
						if len(val) > 1 :
							has_operator = True
						del val
						if has_operator :
							value = str(self.compute_index(value,scope='global',type='float'))
						
						if self.is_function(value) :
							name_ ,params,_ = self.get_func_param(value)
							
							if name_ in self.func_body.keys() :
								value = self.process_functions(value,scope=scope,scope_name=scope_name,exe=True)
								value = str(value)

						if not self.check_number_literals(name,value) :
							return
						value = self.format_literals(data_type,value)		
						self.assign_value(name,value,scope=scope,scope_name=scope_name)
						return True
					if data_type == 'chars' :
						value = self.format_char_literals(line[2:])
						if not self.check_char_literals(name,value) :
							return
						self.assign_value(name,value,scope=scope,scope_name=scope_name)
						return True
				else :
				 	print("Error from process_variable unit variable is not defined {}".format(line))
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
	
		
	def has_comment(self,line) :
		if self.comment_syntax in line.split()[0] :
			return True
		return False
		
	def length_syntax(self,line) :
		#|array|
		array = line.split()[-1]
		if array[0] == '|' and array[-1] == '|' :
			return True
		return False
	
	#def is_char(self,var) :
		#if var[0] == "'" and var[-1] == "'" :
			#return True
	
	def execute_Functions(self,function,scope='global',scope_name='') :
		name,params,_ = extract_name_param(function)
		
		if name in self.functions.keys() :
			func = self.functions[name]
			func.outer_scope = scope_name
			return func.executeTree(function)
		
		if name in self.func_body.keys() :
			return self.process_functions(function,scope=scope,scope_name=scope_name,exe=True)
			
			
	def to_int(self,n) :
		if type(n) == type('a') :
			return int(n)
		res = []
		for i in n :
			res.append(int(float(i)))
		return res
		
	def numberise_array(self,arr,dim=1) :
		if dim == 1 :
			for i,v in enumerate(arr) :
				try :
					arr[i] = float(v)
				except :
					arr = self.numberise_array(arr,dim=2)
			return arr
		if dim == 2 :
			for i,row in enumerate(arr) :
				for j,col in enumerate(row) :
					arr[i][j] = float(col)
			return arr
			
	def function_to_execute(self,line,scope,scope_name,name) :
		if name == 'condition_split' :
			return condition_split(line,'any')
	
	def length_of_array(self,line,scope='global',scope_name="",get_n=False) :
		#let n = |array|
		#n = |n|
		#arr[i-1] = |n|
		pos = 0
		if get_n :
			variable = ""
			N = len(line)
			
			for i in range(1,N-1) :
				variable += line[i]
				
			elements,_ = self.fetch_variable(variable,scope=scope,scope_name=scope_name)
			elements = self.numberise_array(elements)
			col = None
			
			try :
				col = len(elements[0])
			except :
				pass
			
			if col :
				return len(elements),col
			
			return len(elements)
		
		line = line.split()
		
		
		if len(line) == 4 :
			data_type = line[0]
			pos = 1
			

		variable = line[pos]
		name_bar = line[2+pos]
		name = ''
		
		N = len(name_bar)
		
		for i in range(1,N-1) :
			name += name_bar[i]
		
		elements,_ = self.fetch_variable(name,scope=scope,scope_name=scope_name)
		elements = self.numberise_array(elements)
		n = len(elements)
		col=None
		
		try :
			col = len(elements[0])
		except :
				pass
				

		if pos :
			#print(line)
			if col :
				self.define_variable(variable,[n,col],'int_arr',scope=scope,scope_name=scope_name)
				return
			self.define_variable(variable,n,data_type,scope=scope,scope_name=scope_name)
			return
		if col :
			_,dt = self.fetch_variable(variable,scope=scope,scope_name=scope_name)
			if not dt in ['int_arr','float_arr'] :
				if dt == 'let' :
					dt = 'float_arr'
				else :
					dt = dt+'_arr'
					
			self.define_variable(variable,[n,col],dt,scope=scope,scope_name=scope_name)
			return
			
		self.assign_value(variable,n,scope=scope,scope_name=scope_name)
		
	def initialize_array(self,line,scope='global',scope_name='') :
		
		if type(line) == type('a') :
			line = line.split()
		
		if not self.element in line :
			return False
		if not line[0] in self.ArrayDataTypes :
			return False
			
		def get_non_zero_element(arr) :
			for i in arr :
				if i != 0 :
					return i
			return arr
		
		def zero() :
			return  0
			
		def randint() :
			return random.randint(1,1000)
		
		#int_arr A ∈ R[m,n]
		data_type = line[0]
		variable = line[1]
		self.check_variable_name(variable)
		Set = line[3][0]
		dimension = 1
		size = ''
		dim = line[3][1:]
		N = len(dim)
		m = n = 0
		function = zero
		
		if Set == 'R' :
			function = random.random
		elif Set == 'N' :
			function = randint
		
		for i in range(1,N-1) :
			size += dim[i]
			
		if len(size.split(',')) > 1 :
			dimension = 2
			m,n = size.split(',')
		
		if dimension == 1 :
			m = size
		
		vars = [m,n]

		# m  and will be either number or a variable
		for i,var in enumerate(vars) :
			if var == 0 :
				dimension = 1
				continue
			if self.is_number(var) :
				vars[i] = int(float(var))
			elif self.check_variable_name(var) :
				var = self.fetch_var_value(var,scope=scope,scope_name=scope_name)
				vars[i] = int(float(var))
		
		if dimension == 1 :
			M = None
			if len(vars) == 1 :
				M = vars[0]
			else :
				M = max(vars[0],vars[1])
			arr = [function() for i in range(M)]
		else :
			m,n = vars
			arr = [ [function() for j in range(n)] for i in range(m)]
		
		self.define_variable(variable,arr,data_type,scope=scope,scope_name=scope_name)
		return True
		
	def line_to_execute(self,line,scope,scope_name,to_exe) :
		if to_exe == 'accessing_attributes' :
			return accessing_attributes(None,line,scope=scope,scope_name=scope_name,compiler=self)
	
	def add_to_container(self,c,v) :
		if type(c) == type('a') :
			c += v
		elif type(c) == type([1]) :
			c.append(v)
		return c
	
	def split_space(self,line,to_use='list') :
		new_line = None
		if to_use == 'str' :
			new_line = ''
		else :
			new_line = []
		
		N = len(line)
		found_eq = False
		chars = ''
		for i,l in enumerate(line) :
			if l == '=' :
				found_eq = True
				continue
			if found_eq :
				new_line = self.add_to_container(new_line,'=')
				v = self.split_space(line[i:],to_use='str')
				new_line = self.add_to_container(new_line,v)
				break
			if l != ' ' :
				chars += l
				if i+1 == N :
					v = self.add_to_container(new_line,chars)
					new_line = v
					break
				continue
			new_line = self.add_to_container(new_line,chars)
			chars = ''
		
		return new_line
	
	def ProcessLine(self,line,scope='',scope_name='',class_obj=None,Class=None) :
		if line.split() == [] :
			return
		if self.has_comment(line) :
			return
		elif line.split()[0] == self.break_statement :
			return self.break_statement
		elif line.split()[0] == self.continue_statement :
			return self.continue_statement
		elif self.length_syntax(line) :
			return self.length_of_array(line,scope=scope,scope_name=scope_name)
		elif self.initialize_array(line,scope=scope,scope_name=scope_name) :
			return
		elif accessing_attributes(Class,line,scope=scope,scope_name=scope_name,compiler=self) :
			return
		self.process_variable(line,scope=scope,scope_name=scope_name,class_obj=class_obj)
		self.process_Func(line,scope=scope,scope_name=scope_name)
		self.process_functions(line,scope=scope,scope_name=scope_name)
		self.iostream.ans(line,scope=scope,scope_name=scope_name)
		self.iostream.ask(line,scope=scope,scope_name=scope_name)
		#process_functions(self,line,scope=scope,scope_name=scope_name)
		self.process_array(line,scope=scope,scope_name=scope_name,class_obj=class_obj)	
		process_logic_element(compiler,line,scope=scope,scope_name=scope_name)
		#accessing_attributes(Class,line,scope=scope,scope_name=scope_name,compiler=self)
	
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
			if line.split()[0] == 'class' :
				name = line.split()[1]
				self.Variables['local']['local_scope'][name] = {}
				clspu = CLSPU(scope='local',scope_name=name,indent=self.indent,compiler=self)
				pos = clspu.build_class(lines[i:])
				i = i + pos
				continue
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
				loop = LoopProcessingUnit(self.Variables,scope='local',scope_name='for'+str(loop_count),indent=self.indent,process_variable=self.process_variable,output_func=self.output_func,obj=self)
				pos = loop.buildTree(lines[i:])
				loop.executeTree(node=loop.loop_node)
				loop_count = loop_count + 1
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
		
	def compile(self,file_name,op="android") :
		self.Variables['local']['local_scope'].clear()
		self.Variables['global'].clear()
		self.functions.clear()
		self.func_body.clear()
		root = ""
		if op == "android" :
			root = '/storage/emulated/0/'
		file = open(root+file_name+'.bhask')
		lines = file.read()
		self.ProcessLines(lines)
		
		
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
            print('i==8')
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
        r = 0-r
        res = pow(x,r)
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
val = pow(3,-2)
ans(val)
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
res = pow(2,5)
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
ans(fac)
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
    ans(arr[i-1])
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
int n = 10
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

for i = 1 to n :
    for k = 1 to n :
        print(i)
        if i == 6 :
            print('here')
            over
print('finish')

Func pow(x,r) :
    if r == 0 :
        return 1
    if r == 1 :
        return x
    if r > 0 :
        float res = x-0
        r  = r-1
        for i = 1 to r :
            res  = res*x
        return res
    if r < 0 :
        float res = 0.0
        int a = r+r
        r = r-a
        res = pow(x,r)
        return 1/res

func f(x) = 2*x
float res  = 0.0
res = pow(2,4)+pow(2,3)
print(res)
res = f(2)+3*f(3)+pow(2,4)
print(res)
res = pow(3,-2)
print(res)
"""
L11 = """
Func mean(arr,n) :
    float res = 0.0
    for i  = 1 to n :
        res = res+arr[i-1]
    return res/n
    
Func std(arr) :
    float res = 0.0
    res = mean(arr)
    if res |= 0 :
        return res/2
    return 0

int_arr  nums[] = (1,2,3,6,7)
float res = 1*mean(nums,5)
ans(res)
nums[3] = 77
res = mean(nums,5)
ans(nums)
ans(res)
res = std(nums)
ans(res)
float_arr array[] = (9.9,4.5)
ans(array)
int i = 0
array[i+1] = std(nums)
print(array)
for index = 1 to 2 :
    array[index-1] = nums[index*2]
ans(array)
int age = 0
ask(age,"what_is_your_age_:-")
ans(age)
for i = 1 to 2 :
    ans(array[i-1])

"""
L12 = """
let a = 3
if a ≤ 3 :
    ans(a)
else :
    ans('else')
ans('here')
let ∆ = 3
"""
L7 = """
int x = 2

Func poww(float x,int r) :
    int res = x-0
    int r = r-1
    for i = 1 to r :
        res = res*x
    print(res)
    return res

Func pow(float x,int r) :
    if r == 0 :
        print('hereso')
        return 1
    int res = x-0
    int val = 0
    if r < 0 :
        ans(r)
        r = 0-r
        ans('r',r)
        ans('x',x)
        res = pow(x,r)
        return 1/res
    if r == 1 :
        print('here')
        return x
    if r == 0 :
        print('hereo')
        return 1
    r = r-1
    ans('here',r,x)
    for i = 1 to r :
        res = res*x
    return res        

float val = 0
let r = -2
int x = 2
val = pow(x,-2)
ans(val)
for i = 1 to 10 :
    print(i)
int i = 2
if i |= 1 :
    print('yes')
"""
L22 = """
func f(x,y) = x+y*-3
let x = 3
let y = 2
let res = 0.0
ans('here')
res = f(3,2)
ans('res:-',res)

Func fun(float x,float y) :
    int r = 1.0
    for i = x to y :
        r = r+i
        ans(r)
        skip
        ans('r')
    let a = 0
    return r
    
res = fun(3,5)
ans('r:-',res)
res = 1+2
ans(res)
let r = 1
for i = 3 to 5 :
    r = r+i
ans(r)
r = -6-+6*8
ans(r) 
let a = 3+2*-3
ans('a:-',a)
let t = fun(3,4)+fun(3,5)/fun(3,4)
ans('t:-',t)
"""
L33  = """
Func fact(int x) :
    if x == 0 :
        return 1
    int a = x
    int res = 0
    x = x-1
    res = a*fact(x)
    return res
    
Func pow(float x,int r) :
    if r == 1 :
        return x
    if r == 0 :
        return 1
    if r < 0 :
        let res = 0
        r = 0-r
        res = pow(x,r)
        return 1/res
    float res = x
    r = r-1
    float index = 1
    for i = 1 to r :
        res = res*x
        index = index*i
    ans('index:-',index)
    return res
    
int a = 6
int res = 0
res = fact(6)
ans(res)
res = -6--6*8+8
ans(res)
int a = 3
int b = -2
int c = a-1
ask(c,'enter_value_of_x')
res = pow(c,b)
ans('res_here')
ans(res)
let b = 0
ans(a)
b =  a-1
ans('b',b)
ans('after')
"""
L13  = """
Func pow(float x,int r) :
    let res = x+1
    return res
int a = 6
let b = a+3+1+3
ans(b)
let c = 0
c =  pow(-3,-4)
ans(c)
let res = 3
let a = 3
for i = 1 to 2 :
    res = res*i
ans(res)
int a = 6
let b = a
res = 3*3+b
ans(res)
ans('after')
let big = 6
for i = 1 to 6 :
    big = big*i
    let flag = 0
    for k = 1 to 7 :
        big = big*k
        if big >= 1000 :
            flag = 1
            over
    if flag == 1 :
        over

ans('here_',big)
let res = 9
big = res*big
ans('big',big)
let a = big-res
ans(a)
"""
L44 = """
%func j(res) = 2*res+3*res

Func f(int x) :
    return x-2

Func mean(float_arr arr,int n) :
    int sum = 1
    let r = 0
    for i = 1 to n :
        sum = sum+arr[i-1]
    ans(sum)
    r = f(sum)*f(sum)
    ans('ans:-',r)
    return sum/n

int_arr arr[] = (1,5,88,54)
int_arr arr1[] = (1,6,3,4)
ans(arr1)
let a = 0
for i = 1 to 4 :
    ans(arr[i-1])
    arr1[i-1] = arr[i-1]
    a = a+i
ans(arr1)
ans('a:-',a)
ele3 ∈ arr
ans('ele:-',ele)
let r = 3
 let area = 2*π*r
ans('area',area)
r = π
ans(r)
if 5 ∈ arr :
    ans('is_a_element')
else :
    ans('not_an_element')
%let res = j(3)
%res = j(3)
%ans(res)
let i = 0
a0 ∈ arr
ans('a:-',a)

Func powa(int r) :
    return r-1

%let r =  0
let rr = powa(5)+powa(6)
%rr = powa(5)
ans('rr:-',rr)
let r = powa(5)
ans('r:-',r)

Func _examp_a(int r) :
    return r+1

let _a = _examp_a(5)
ans(_a)

let hh = mean(arr,4)
ans('mean:-',hh)
func g(x) = 3*x
let a = 0
a = g(3)
ans('ans:-',a)
""" 
L45 = """
func g(x) = 3*x

Func foo(float x) :
    if x ≤ 0 :
        return 1
    x = x-1
    x = foo(x)
    ans('x',x)
    if x == 1 :
        return g(x)
    return x
let a = foo(7)
ans(a)
"""

L46 = """
Func f(float x) :
    return x-1
func g(x) = 2*x
let a = 2
let x = -a
let var = f(x)/g(x)
ans(var)
for i = 1 to 5 :
    let a = 0
    if a == 0 :
        ans('a')
        ans(i)
        over
float_arr k[] = (1.2,3.4,4.4)
int j = 2
for i = 1 to 3 :
    a[i-1] ∈ k
    ans(a)
%the length of the array [arr]
int_arr arr[] = (1,2,4)
let n = 0
n = |arr|
ans(n)

"""
L47 = """
func f(x) = 33*x
int_arr arr[2,3] = ((1,2,3),(4,5,6))
int_arr fun[] = (99,100)
ans(arr)
fun[0] = f(5)
ans(fun)
let length = |arr|
ans('length:-',length)
int row = length[1]
%row = length[0]
ans('row:-',row)
arr[1,1] = fun[0]*arr[1,1]+arr[1,1]
arr[1,0] = fun[0]
ans(arr[1,0])
for i = 1 to 2 :
    for j = 1 to 3 :
        ans(arr[i-1,j-1])
        %arr[i-1,j-1] = fun[0]
ans(arr)
arr[0,0] = 999
% every thing is working fine :)
ans(arr) 
let m = 2
let n = m
%initialising array
int_arr a ∈ 0[m,n]
ans(a)
a[0,0] = 9
ans(a)
"""

L48 = """

class Node :
    let a = 0
    int_arr arr[] = (0,0,0,0)
    
    Func get_element(int pos) :
        let a = arr[pos]
        return a
    
Func hello(chars name) :
    ans('hello_',name)
    return name

Func get_n(int n) :
    return n-1

Node node
node.a = 5
int i = 2
node.arr[i] = 55
let a = 0
a = node.a
ans('a:-',a)
let b = 0
b = node.arr[i]
node.arr[0] = b
ans('b:-',b)
let c = 0
c = node.get_element(i)
ans('c:-',c)
node.a = 5
ans('node:-',node.a)
ans(node.arr[0])
Node node1
node1.a = 6454
ans(node1.a)
"""

L49 = """
class Node :
    int a = 0
    int_arr arr[] = (4,2)
Node node
node.a = 5

Func f(int x) :
    return x-1
float_arr arr[2,2] = ((1,2),(2,2))
ans(arr)
%int i = 0
int j = 1
for i = 1 to 2 :
    ans(f(node.arr[0]))
    arr[i-1,i-1] = f(node.arr[i-1])*-3
%arr[0,0] = f(arr[i+1,j])
ans(arr)
let a = 2^2*6
ans(a)
"""
lin = """
int a = 0
for i = 1 to 5 :
    for j = 1 to 5 :
        if i == 4 :
            if j == 4 :
                over
        ans(i)
        a = a+1
ans(a)
"""
#compiler.ProcessLines(lin)
#compiler.ProcessLines(L49)
compiler.compile("C:\Python\DiagnolCheck",op="windows")
#print(compiler.Variables['local']['local_scope']['pow'])
#compiler.compile('POW')
#compiler.compile('sample_program')
#compiler.compile('BubbleSort')
#compiler.compile('Calculator')
#compiler.compile('MatrixMul')
#compiler.compile('Classes')
#compiler.compile('simple_neuron')
#compiler.compile('nested_functions')
#print(compiler.Variables['local']['local_scope'])
#print(compiler.Variables['global'])