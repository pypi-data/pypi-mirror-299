import ConditonalProcessingUnit as CPU
from StringAlgorithm.ConditionSplit import condition_split
from ExpressionTree1 import ExpressionTree as EXPT

class LoopNode :
	
	def __init__(self,) :
		self.syntax = ""
		self.loop_body = []

class LoopProcessingUnit() :
	
	def __init__(self,Variables=None,scope='local',scope_name='',indent=4,process_variable=None,output_func=None,obj=None,is_func=False):
		self.loop_node = None
		self.indent = indent
		self.scope = scope
		self.is_func = is_func
		self.cpu = None
		self.process_variable = process_variable
		self.output_func = output_func
		self.scope_name = scope_name
		self.obj = obj
		self.Variables = Variables
		self.loop_types = ['for','while']
		self.vars = Variables['local']['local_scope'][self.scope_name]
		self.alpha = 'abcdefghijklmnopqrstuvwxyz'
	
	def hasIndent(self,line,indent=0) :
		count = 0
		for l in line :
			if l == " " :
				count += 1
				continue
			break
		if count == self.indent+indent :
			return True
		return False
	
	def is_alpha(self,name) :
		for n in name :
			if n in self.alpha :
				return True
		return False
	
	def process_loop_syntax(self,line) :
		if line == "" or line == [] :
			return
		temp = line
		if type(line) == type('a') :
			temp = line.split()
		if temp[0] == 'for' :
			#for i = 1 to 3 :
			if len(temp) != 7 :
				print("Incorrect loop Syntax {}".format(line))
				return
			if temp[2] != '=' :
				print("Incorrect loop Syntax {}".format(line))
				return
			variable_i = temp[1]
			variable_a = temp[3]
			variable_b = temp[5]
			vars = [variable_a,variable_b]
			if not self.is_alpha(variable_i) :
				print("Error this [i] = 1 must be a variable {}".format(variable_i))
				return
			for i,v in enumerate(vars) :
				
				if self.obj.length_syntax(v) :
					vars[i] = self.obj.length_of_array(v,scope=self.scope,scope_name=self.scope_name,get_n=True)
					continue
				
				if self.obj.is_number(v) :
					vars[i] = int(float(v))
					continue
				
				if len(condition_split(v,'any')) > 1 :
					vars[i] = int(self.obj.compute_index(v,scope=self.scope,scope_name=self.scope_name))
					continue
					
				if self.obj.check_variable_name(v) :
					val,_= self.obj.fetch_variable(v,scope='local',scope_name=self.scope_name)
					vars[i] = int(float(val))
					
			self.vars[variable_i] = [variable_a,'int']
		return vars[0],vars[1]
	 
	def buildTree(self,lines,prev_node=None,indent=0) :
		node = LoopNode()
		node.syntax = lines[0]
		i = 1
		N = len(lines)
		
		if prev_node == None :
			self.loop_node = node
		else :
			prev_node.loop_body.append(node)
			
		while i < N :
			line = lines[i]
			if line.split() == [] :
				i = i + 1
				continue
			if not self.hasIndent(line,indent) :
				break
			if line.split()[0] in self.loop_types :
				pos = self.buildTree(lines[i:],prev_node=node,indent=indent+self.obj.indent)
				i = i + pos
				continue
			if line.split()[0] == 'if' :
				cpu = CPU.ConditionalProcessingUnit(scope='local',scope_name=self.scope_name,compiler=self.obj)
				cpu.has_loop = True
				pos = cpu.buildTree(lines[i:],indent=indent+self.indent)
				i = i + pos
				node.loop_body.append(cpu)
				if not self.cpu :
					self.cpu = cpu
				continue
			node.loop_body.append(line)
			i = i + 1
		return i
		
	def executeTree(self,node=None,d=0) :
		if node :
			a,b = self.process_loop_syntax(node.syntax)
			var_a = node.syntax.split()[1]
			for i in range(a,b+1) :
				_,dt = self.vars[var_a]
				self.vars[var_a] = [str(i),dt]
				for line in node.loop_body :
					if type(line) == type(node) :
						return_val = self.executeTree(line,d=d+1)
						if return_val :
							if return_val.split()[0] == self.obj.break_statement :
									return
							if return_val.split()[0] == self.obj.continue_statement :
									break
						continue

					if type(line) == type(self.cpu) :
						return_value = line.executeTree(line.head)
						if return_value :
							arr = return_value.split()
							if arr[0] == 'return' :
								if len(arr) > 1 :
									value = arr[1]
									expr = EXPT()
									expr.buildTree(value)
									return expr.computeTree(expr.head)
								return
						
						if return_value == self.obj.break_statement :
							return
						elif return_value == self.obj.continue_statement :
							break
						continue
					return_val =self.obj.ProcessLine(line,scope='local',scope_name=self.scope_name)
					if return_val == self.obj.break_statement :
						return
					if return_val == self.obj.continue_statement :
						break
			return