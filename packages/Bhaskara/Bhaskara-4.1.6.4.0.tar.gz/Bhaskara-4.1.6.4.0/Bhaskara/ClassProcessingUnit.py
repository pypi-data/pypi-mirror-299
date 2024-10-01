from StringAlgorithm.ExtractFuncNameParams import extract_name_param
from LoopProcessingUnit2 import LoopProcessingUnit as LPU
from FunctionalProcessingUnit import FunctionProcessingUnit as FPU
from ConditonalProcessingUnit import ConditionalProcessingUnit as CPU
from ExpressionTree1 import ExpressionTree
from  StringAlgorithm.ConditionSplit import condition_split

class class_node :
	
	def __init__(self,) :
		self.class_name = ''
		self.body = {}
		


class ClassProcessingUnit :
	
	def __init__(self,scope='local',scope_name='',indent=None,compiler=None) :
		self.scope = scope
		self.scope_name = scope_name
		self.indent = indent
		self.compiler = compiler
		self.ERROR_CODE = -9999
		
	
	def check_syntax(self,line) :
		line = line.split()
		#class Name :
		class_name = line[1]
		if line[2] != ':' :
			print('Invalid Syntax {}'.format(line))
			return self.ERROR_CODE
		if not self.compiler.check_variable_name(class_name) :
			print("Invalid name {}".format(line))
			return self.ERROR_CODE
		
		
		
	def check_indent(self,line) :
		count = 0
		for i in range(len(line)) :
			if line[i] != ' ' :
				break
			count += 1
		if count == self.indent :
			return True
		return False
		
	def build_class(self,lines) :
		if type(lines) == type('a') :
			lines = lines.split('\n')
		node = class_node()
		self.head = node
		i = 0
		N = len(lines)
		line = lines[i]
		self.check_syntax(line)
		node.class_name = line.split()[1]
		i = 1
		while i < N :
			line = lines[i]
			if line.split() == [] :
				i = i + 1
				continue
			if not self.check_indent(line) :
				break
			if line.split()[0] == 'Func' :
				func = FPU(scope=self.scope,scope_name=self.scope_name,compiler=self.compiler)
				name,_,_ = self.compiler.get_func_param(line)
				name = 'class_'+name.split()[1]
				self.compiler.functions[name] = func
				_,pos = func.buildTree(lines[i:],indent=2*self.indent)
				node.body[name] = func
				self.compiler.Variables['local']['local_scope'][self.scope_name][name] = func
				i = i + pos
				continue
			self.compiler.ProcessLine(line,scope=self.scope,scope_name=self.scope_name,class_obj=self,Class=self)
			i = i + 1
		
		self.compiler.Variables['local']['local_scope'][self.scope_name]['class_name'] = self
		
		return i
		
	def attribute_not_found(self,name) :
		print("Error attribute of name {} is not defined".format(name))
		return
		
def accessing_attributes(self,line,scope='',scope_name='',compiler=None) :
	
	#Object.attributes = Variable
	#Variable = Object.attribute
	#Object.attributes
	#Node node
	if len(compiler.split_space(line)) >= 4 :
		return
	
	if len(line.split()) == 2 :
		if line.split()[0] == 'return' :
			return
		
		if self == None :
			class_name,object = line.split()
			self = compiler.Variables['local']['local_scope'][class_name]['class_name']
		
		line = line.split()
		class_name,obj = line
		
		
		if obj in compiler.Variables['local']['local_scope'].keys() :
			print("Variable {} of type {} has already defined".format(obj,class_name))
			return True
			
		if class_name != self.head.class_name :
			return
		compiler.Variables['local']['local_scope'][obj] = compiler.Variables['local']['local_scope'][class_name].copy()
		compiler.Variables['local']['local_scope'][obj]['class_name'] = self
		#print(compiler.Variables['local']['local_scope']['d1'])
		return True
	
		
	if '=' in line :
		
		line = line.split('=')
		left_side,right_side = line
		object = variable = None
		value = None
		#node.value 
		if '.' in left_side :
			
			object,variable = left_side.split()[0].split('.')
			object = object.split()[0]
			variable = variable.split()[0]

			if not self :
				self = compiler.Variables['local']['local_scope'][object]['class_name']
			if not object in compiler.Variables['local']['local_scope'].keys() :
				print("Object is not defined {}".format(line[0]))
				return False

			right_side = right_side.split()[0]
			
				
			#check if the right_side is a variable ,length or a function
			if right_side[0] == "'" and right_side[-1] == "'" :
				value = right_side
			if compiler.is_a_number(right_side) :
				value = right_side
			elif len(condition_split(right_side,'any')) > 1 :
				tree = ExpressionTree(Variables=self.compiler.Variables,scope=scope,scope_name=scope_name,obj=compiler)
				tree.buildTree(right_side)
				value = tree.computeTree(tree.head)
			elif compiler.check_variable_name(right_side) :
				value = self.compiler.fetch_var_value(right_side,scope=scope,scope_name=scope_name)
			elif compiler.is_function(right_side) :
				value = compiler.execute_Functions(right_side,scope=scope,scope_name=scope_name)
			elif compiler.get_arr_index(right_side) :
				value,_ = compiler.process_array(right_side,scope=scope,scope_name=scope_name)
			elif compiler.length_syntax(right_side) :
				value = compiler.length_of_array(right_side,scope=scope,scope_name=scope_name)

			if compiler.get_arr_index(variable) :
				#variable is an array
				name,index,_ = compiler.get_arr_index(variable)
				row = col = None
				if len(index.split(',')) > 1 :
					row,col = compiler.compute_coords(index.split(','),scope=scope,scope_name=scope_name)
					compiler.assign_2darray(name,value,x=row,y=col,scope='local',scope_name=object)
					return True
				if len(condition_split(index,'any')) > 1 :
					index = compiler.compute_index(index,scope=scope,scope_name=scope_name)
					index = int(index)
					compiler.assign_array(name,value,index=index,scope='local',scope_name=object)
					return True
				if compiler.is_a_number(index) :
					pass
				elif compiler.check_variable_name(index) :
					index = compiler.fetch_var_value(index,scope=scope,scope_name=scope_name)
				index = int(index)
				compiler.assign_array(name,value,index=index,scope='local',scope_name=object)
				return True

			if variable in compiler.Variables['local']['local_scope'][object].keys() :
				compiler.assign_value(variable,value,scope='local',scope_name=object)
				return True
			print("Error class {} has no such attribute {}".format(self.head.class_name,variable))
			return False
		
		if '.' in right_side and not compiler.is_a_number(right_side) :
			#n = node.data
			right_side = right_side.split()[0]
			
			if len(right_side.split('.')) != 2 :
				return False
			
			obj,variable = right_side.split()[0].split('.')
			
			y = left_side.split()[0]
			value = None
			
			if not self :
				self = compiler.Variables['local']['local_scope'][obj]['class_name']
			#if variable is an array
			#a = arr[i] or arr[i,j]
			if not obj in compiler.Variables['local']['local_scope'].keys() :
				print('Error object of name {} has not defined'.format(obj))
				return False
			
			if self.compiler.get_arr_index(variable) :
				name,index,_ =self.compiler.get_arr_index(variable)
				if not name in self.compiler.Variables['local']['local_scope'][self.head.class_name].keys() :
					self.attribute_not_found(name)
					return False
				
				if len(index.split(',')) == 2 :
					row,col = compiler.compute_coords(index.split(','),scope=scope,scope_name=scope_name)
					elements = compiler.fetch_var_value(name,scope='local',scope_name=obj)
					value = elements[row][col]
				elif len(condition_split(index,'any')) > 1 :
					index = compiler.compute_index(index,scope=scope,scope_name=scope_name)
					elements = compiler.fetch_var_value(name,scope='local',scope_name=obj)
					value = elements[index]
				elif compiler.is_a_number(index) :
					elements = compiler.fetch_var_value(name,scope='local',scope_name=scope_name)
					value = elements[int(index)] 
				elif compiler.check_variable_name(index) :
					index = int(compiler.fetch_var_value(index,scope=scope,scope_name=scope_name))
					elements = compiler.fetch_var_value(name,scope='local',scope_name=obj)
					value = elements[index]
			
			
			elif compiler.check_variable_name(variable) :
				if not variable in compiler.Variables['local']['local_scope'][obj].keys() :
					self.attribute_not_found(variable)
					return False
				value = compiler.fetch_var_value(variable,scope='local',scope_name=obj)
			
			
			elif compiler.is_function('class_'+variable) :
				name,params,_ = compiler.get_func_param('class_'+variable)
				if name in compiler.Variables['local']['local_scope'][obj].keys() :
					func = compiler.Variables['local']['local_scope'][obj][name]
					func.outer_scope = scope_name
					value = func.executeTree('class_'+variable)
				
				elif name in compiler.Variables['local']['local_scope'][obj].keys() :
					value = compiler.process_functions('class_'+variable,scope='local',scope_name=obj,exe=True)
				
				
			if compiler.get_arr_index(y) :
				name,index,_ = compiler.get_arr_index(y)
				line = left_side + ' ' + '=' + ' ' + value
				compiler.process_array(y,scope=scope,scope_name=scope_name)
			
			if compiler.check_variable_name(y) :
				compiler.assign_value(y,value,scope=scope,scope_name=scope_name)
			return True
	if type(line) == type('a') :
		line = line.split()[0]
		
	if '.' in line and not compiler.is_a_number(line) :
		obj,var = line.split('.')
		
		if not obj in compiler.Variables['local']['local_scope'].keys() :
			return
			
		if compiler.get_arr_index(var) :
			name,index,_ = compiler.get_arr_index(var)
			if len(index.split(',')) == 2 :
				row = col =  None
				try :
					row,col = compiler.compute_coords(index.split(','),scope=scope,scope_name=scope_name)
				except :
					return
				
				elements,_ = compiler.fetch_variable(name,scope='local',scope_name=obj)
				return elements[row][col]
			try :
				index = compiler.compute_index(index,scope=scope,scope_name=scope_name)
			except :
				return
			elements = compiler.fetch_var_value(name,scope='local',scope_name=obj)
			return elements[index]
			
			#return compiler.process_array(var,scope='local',scope_name=obj)[0]
			
		if var in compiler.Variables['local']['local_scope'][obj].keys() :
			val =  compiler.Variables['local']['local_scope'][obj][var]
			return val[0]
		if compiler.is_function(var) :
			name,_,_ = compiler.get_func_param(var)
			name = 'class_'+name
			func = self.Variables['local']['local_scope'][obj][name]
			func.outer_scope = scope_name
			return func.executeTree(var)
	return False