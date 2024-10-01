from StringAlgorithm.ConditionSplit import condition_split
from StringAlgorithm.ConditionSplitV3 import condition_split_v2

class Node :
	
	def __init__(self,sym) :
		self.sym = sym
		self.child_nodes = []
		self.expression = []

class ExpressionTree :
	
	def __init__(self,Variables={},scope='',scope_name='',is_func=False,parameters=[],param_values={},obj=None) :
		self.head = None
		self.obj = obj
		self.Variables = Variables
		self.scope = scope
		self.param_values = param_values
		self.is_func = is_func
		self.parameters = parameters
		self.scope_name = scope_name
		self.alpha = 'abcdefghijklmnopqrstuvwxyz'
		self.chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
		self.nums = '0123456789'
		
		
	def is_number(self,num) :
			try :
				a = float(num)
				return True
			except :
				return False
				
	
	def fetchValue(self,n) :
		if self.is_func :
			if n in self.parameters :
				return n
		if self.scope == 'local' :
			if n in self.Variables['local']['local_scope'][self.scope_name].keys() :
				n,_ = self.Variables['local']['local_scope'][self.scope_name][n]
				return n
			else :
				try :
					if n in self.Variables['global'].keys() :
						n,_= self.Variables['global'][n]
						return n
				except :
					print("Keyerror")
		if self.scope == 'global' :
			try :
				n,_= self.Variables['global'][n]
				return n
			except :
				v_ = self.Variables['local']['local_scope'][self.scope_name]
				if n in v_.keys() :
					return v_[n][0]
				print("error {} is not defined ".format(n))
	
	def buildTree(self,line,prev_node=None) :
		
		if len(condition_split_v2(line,'+')) > 1 :
			line = condition_split_v2(line,op='+')
			node = Node('+')
			
			if prev_node :
				prev_node.expression.append(node)
			else :
				self.head = node
			for l in line :
				n = self.buildTree(l,prev_node=node)
				if n :
					if n in self.obj.mathematical_constants.keys() :
						node.expression.append(self.obj.mathematical_constants[n])
						continue
					
					if self.obj.get_arr_index(n) and not '.' in n:
						n,_ = self.obj.process_array(n,scope=self.scope,scope_name=self.scope_name)
						node.expression.append(float(n))
						continue
					
					is_var = False
					
					if self.obj.check_variable_name(n) :
						is_var = True
					
					if is_var :
						n = self.obj.fetch_var_value(n,scope=self.scope,scope_name=self.scope_name)
						node.expression.append(float(n))
						continue
					
					if self.is_number(n) :
						node.expression.append(float(n))
						continue
					
					name,param,is_found = self.obj.get_func_param(n)
					
					if is_found :
						
						if name in self.obj.func_body.keys() :
							n = self.obj.process_functions(n,scope=self.scope,scope_name=self.scope_name,exe=True)
							node.expression.append(float(n))
							continue
							
						if name in self.obj.functions.keys() :
							func = self.obj.functions[name]
							func.outer_scope = self.scope_name
							n = func.executeTree(n)
							
							if self.is_number(n) :
								node.expression.append(float(n))
								continue
							
							if type(n) == type('a') :
								node.expression.append(float(n))
								continue
							
							if type(n) == type(['1']) :
								for ii in n :
									node.expression.append(float(ii))
								continue
					if not self.is_number(n) and '.' in n :
						node.expression.append(float(self.obj.line_to_execute(n,self.scope,self.scope_name,'accessing_attributes')))
						continue
					
					 
					if '-' in n :
						if self.obj.check_variable_name(n[1:]) :
							n = self.obj.fetch_var_value(n[1:],scope=self.scope,scope_name=self.scope_name)
							n = '-' + str(n)
							n = self.minus_minus_plus(n)
							node.expression.append(float(n))
									
			return
		
		if len(condition_split_v2(line,'-')) > 1 :
			line = condition_split_v2(line,op='-')
			node = Node('-')
			if prev_node :
				prev_node.expression.append(node)
			else :
				self.head = node
					
			for l in line :
				n = self.buildTree(l,prev_node=node)
				
				if n :
					if n in self.obj.mathematical_constants.keys() :
						node.expression.append(self.obj.mathematical_constants[n])
						continue
					
					if self.obj.get_arr_index(n) and not '.' in n:
						n,_ = self.obj.process_array(n,scope=self.scope,scope_name=self.scope_name)
						node.expression.append(float(n))
						continue
					
					is_var = False
					
					if self.obj.check_variable_name(n) :
						is_var = True
					
					if is_var :
					    n = self.obj.fetch_var_value(n,scope=self.scope,scope_name=self.scope_name)
					    node.expression.append(float(n))
					    continue
					
					if self.is_number(n) :
						node.expression.append(float(n))
						continue
						
					name,param,is_found = self.obj.get_func_param(n)
					
					if is_found :
					    if name in self.obj.func_body.keys() :
					         n = self.obj.process_functions(n,scope=self.scope,scope_name=self.scope_name,exe=True)
					         node.expression.append(float(n))
					         continue
					    if name in self.obj.functions.keys() :
					        func = self.obj.functions[name]
					        func.outer_scope = self.scope_name
					        n = func.executeTree(n)
					          
					        if self.is_number(n):
					          	node.expression.append(float(n))
					          	continue
					        if type(n) == type('a') :
					            node.expression.append(float(n))
					            continue
					        if type(n) == type(['1']) :
					             for ii in n :
					                 node.expression.append(float(ii))
					             continue
					if not self.is_number(n) and '.' in n :
					    node.expression.append(float(self.obj.line_to_execute(n,self.scope,self.scope_name,'accessing_attributes')))
					    continue   
					 
					if '-' in n :
						if self.obj.check_variable_name(n[1:]) :
							n = self.obj.fetch_var_value(n[1:],scope=self.scope,scope_name=self.scope_name)
							n = '-' + str(n)
							n = self.minus_minus_plus(n)
							node.expression.append(float(n))
					                 
			return
		if  len(condition_split_v2(line,'/')) > 1 :
			line = condition_split_v2(line,'/')
			node = Node('/')

			if prev_node :
				prev_node.expression.append(node)
			else :
				self.head = node
			for l in line :
				n = self.buildTree(l,prev_node=node)
				if n :
					
					if n in self.obj.mathematical_constants.keys() :
						node.expression.append(self.obj.mathematical_constants[n])
						continue
					
					if self.obj.get_arr_index(n) and not '.' in n:
						n,_ = self.obj.process_array(n,scope=self.scope,scope_name=self.scope_name)
						node.expression.append(float(n))
						continue
						
					is_var = False
					
					if self.obj.check_variable_name(n) :
						is_var = True
					
					if is_var :
					    n = self.obj.fetch_var_value(n,scope=self.scope,scope_name=self.scope_name)
					    node.expression.append(float(n))
					    continue
					
					if self.is_number(n) :
					    node.expression.append(float(n))
					    continue
					    	
					name,param,is_found = self.obj.get_func_param(n)
					if is_found :
					    if name in self.obj.func_body.keys() :
					    	n = self.obj.process_functions(n,scope=self.scope,scope_name=self.scope_name,exe=True)
					    	node.expression.append(float(n))
					    	continue
					    if name in self.obj.functions.keys() :
					    	func = self.obj.functions[name]
					    	func.outer_scope = self.scope_name
					    	n = func.executeTree(n)
					    	
					    	if self.is_number(n) :
					    		node.expression.append(float(n))
					    		continue
					    	if type(n) == type('a') :
					    		node.expression.append(float(n))
					    		continue
					    	if type(n) == type(['1']) :
					    		for ii in n :
					    			node.expression.append(float(ii))
					    		continue
					if not self.is_number(n) and '.' in n :
						value = self.obj.line_to_execute(n,self.scope,self.scope_name,'accessing_attributes')
						node.expression.append(float(value))
						continue
					
					 
					if '-' in n :
						if self.obj.check_variable_name(n[1:]) :
							n = self.obj.fetch_var_value(n[1:],scope=self.scope,scope_name=self.scope_name)
							n = '-' + str(n)
							n = self.minus_minus_plus(n)
							node.expression.append(float(n))
			return
		
		if len(condition_split_v2(line,'*')) > 1 :
			line = condition_split_v2(line,op='*')
			node = Node('*')
			
			if prev_node :
				prev_node.expression.append(node)
			else :
				self.head = node
				
			for l in line :
				n = self.buildTree(l,prev_node=node)
				
				if n :
					
					if n in self.obj.mathematical_constants.keys() :
						node.expression.append(self.obj.mathematical_constants[n])
						continue
						
					
					if self.obj.get_arr_index(n) and not '.' in n:
						n,_ = self.obj.process_array(n,scope=self.scope,scope_name=self.scope_name)
						node.expression.append(float(n))
						continue
						
					is_var = False
					if self.obj.check_variable_name(n) :
						is_var = True
						
					if is_var :
					    n = self.obj.fetch_var_value(n,scope=self.scope,scope_name=self.scope_name)
					    if n :
					    	node.expression.append(float(n))
					    continue
					
					if self.is_number(n) :
						node.expression.append(float(n))
						continue
					
					name,param,is_found = self.obj.get_func_param(n)
					if is_found :
					    name ,param,_ = self.obj.get_func_param(n)
					    if name in self.obj.func_body.keys() :
					    	n = self.obj.process_functions(n,scope=self.scope,scope_name=self.scope_name,exe=True)
					    	node.expression.append(float(n))
					    	continue
					    if name in self.obj.functions.keys() :
					    	func = self.obj.functions[name]
					    	func.outer_scope = self.scope_name
					    	n = func.executeTree(n)
					    	if self.is_number(n) :
					    		node.expression.append(float(n))
					    		continue
					    	if type(n) == type('a') :
					    		node.expression.append(float(n))
					    		continue
					    	if type(n) == type(['1']) :
					    		for ii in n :
					    			node.expression.append(float(ii))
					    		continue
					    		
					if not self.is_number(n) and '.' in n :
					    node.expression.append(float(self.obj.line_to_execute(n,self.scope,self.scope_name,'accessing_attributes')))
					    continue
					
					 
					if '-' in n :
						if self.obj.check_variable_name(n[1:]) :
							n = self.obj.fetch_var_value(n[1:],scope=self.scope,scope_name=self.scope_name)
							n = '-' + str(n)
							n = self.minus_minus_plus(n)
							node.expression.append(float(n))
			return
			
		if len(condition_split_v2(line,'^')) > 1 :
			line = condition_split_v2(line,op='^')
			node = Node('^')
			
			if prev_node :
				prev_node.expression.append(node)
			else :
				self.head = node
				
			for l in line :
				n = self.buildTree(l,prev_node=node)
				
				if n :
					
					if n in self.obj.mathematical_constants.keys() :
						node.expression.append(self.obj.mathematical_constants[n])
						continue
						
					
					if self.obj.get_arr_index(n) and not '.' in n:
						n,_ = self.obj.process_array(n,scope=self.scope,scope_name=self.scope_name)
						node.expression.append(float(n))
						continue
						
					is_var = False
					if self.obj.check_variable_name(n) :
						is_var = True
						
					if is_var :
					    n = self.obj.fetch_var_value(n,scope=self.scope,scope_name=self.scope_name)
					    if n :
					    	node.expression.append(float(n))
					    continue
					
					if self.is_number(n) :
						node.expression.append(float(n))
						continue
					
					name,param,is_found = self.obj.get_func_param(n)
					if is_found :
					    name ,param,_ = self.obj.get_func_param(n)
					    if name in self.obj.func_body.keys() :
					    	n = self.obj.process_functions(n,scope=self.scope,scope_name=self.scope_name,exe=True)
					    	node.expression.append(float(n))
					    	continue
					    if name in self.obj.functions.keys() :
					    	func = self.obj.functions[name]
					    	func.outer_scope = self.scope_name
					    	n = func.executeTree(n)
					    	if self.is_number(n) :
					    		node.expression.append(float(n))
					    		continue
					    	if type(n) == type('a') :
					    		node.expression.append(float(n))
					    		continue
					    	if type(n) == type(['1']) :
					    		for ii in n :
					    			node.expression.append(float(ii))
					    		continue
					    		
					if not self.is_number(n) and '.' in n :
					    node.expression.append(float(self.obj.line_to_execute(n,self.scope,self.scope_name,'accessing_attributes')))
					    continue
					    
					if '-' in n :
						if self.obj.check_variable_name(n[1:]) :
							n = self.obj.fetch_var_value(n[1:],scope=self.scope,scope_name=self.scope_name)
							n = '-' + str(n)
							n = self.minus_minus_plus(n)
							node.expression.append(float(n))
			return
			
			
		return line
	
	def minus_minus_plus(self,num) :
		if len(num) >=3 :
			if num[0] == '-' and num[1] == '-' :
				return num[2:]
		return num
	
	def list_cal(self,list_,symb) :
		
		if symb == '+' :
			res = 0
			for l in list_ :
				res = res + l
			return res
		
		if symb == '-' :
			res = list_[0]
			for i in range(1,len(list_)) :
				res = res - list_[i]
			return res
		
		if symb == '*' :
			res  = 1
			for l in list_ :
				res = res * l
			return res
		
		if symb == '/' :
			res = list_[0]
			for i in range(1,len(list_)) :
				try :
					res = res/list_[i]
				except :
					res = 0
			return res
			
		if symb == '^' :
			return list_[0]**list_[1]
		
	def computeTree(self,node) :
		if node :
			res = 0
			ops = []
			if node.expression :
				for child in range(len(node.expression)) :
					if type(node.expression[child]) == type(node) :
						N = self.computeTree(node.expression[child])
						ops.append(N)
						continue
					if node.expression[child] in self.parameters :
						ops.append(float(self.param_values[node.expression[child]]))
						continue
					ops.append(node.expression[child])
				return self.list_cal(ops,node.sym)
				
					
	
	def printTree(self,node) :
		if node :
			if node.expression :
				for child in range(len(node.expression)) :
					if type(node.expression[child]) == type(node) :
						self.printTree(node.expression[child])
						continue
					if node.expression[child] in self.parameters :
						node.expression[child] = float(self.param_values[node.expression[child]])
					print(node.expression[child],node.sym," ",end="")
				return
			return
		return
	"""
	def printTree(self,node) :
		if node :
			if node.child_nodes :
				for child in range(len(node.child_nodes)):
						self.printTree(node.child_nodes[child])
						if child + 1 == len(node.child_nodes) :
							continue
						print(node.sym,end='')
						
				print(node.sym," ",end='')
			if node.expression :
				for ii in range(len(node.expression)) :
					if ii + 1 < len(node.expression) :
						print(node.expression[ii],' ',node.sym,' ',end='')
						continue
					print(node.expression[ii],' ',end=' ')
				return
			return
		return
		"""
		
		
"""
expr_tree = ExpressionTree()
expr = '8*8 + 2 + 3- 7*7 +8-8'
expr_tree.buildTree(expr)
print(expr)
expr_tree.printTree(expr_tree.head)
print('\n')
print(expr_tree.computeTree(expr_tree.head))
"""
"""
a = "2*2 + 3*2"
tree = ExpressionTree()
tree.buildTree(a)
print(tree.computeTree(tree.head))
"""