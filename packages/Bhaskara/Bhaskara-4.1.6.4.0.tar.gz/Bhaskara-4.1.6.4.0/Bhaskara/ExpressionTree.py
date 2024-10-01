class Node :
	
	def __init__(self,op) :
		self.op = op
		self.child_nodes = []
		self.vars = []


class ExpressionTree() :
	
	def __init__(self,) :
		self.head = None
		self.ops = ['-','+','/','*']
		self.nums = '0123456789'
	
	def Compute_Scalers(self,symb,a,b) :
		if symb == '+' :
			return a + b
		if symb == '-' :
			return a  - b
		if symb == '/' :
			return a / b 
		if symb == '*' :
			return  a * b
	
	def Compute_List(self,symb,num_list) :
		if len(num_list) == 1 :
			return num_list[0]
		if symb == '+' :
			res = 0
			for n in num_list :
				res = res + n
			return res
		if symb == '-' :
			res = num_list[0]
			for i in range(1,len(num_list)) :
				res = res - num_list[i]
			return res
		if symb == '*' :
			res = 1
			for n in num_list :
				res = res * n
			return res
		if symb == '/' :
			res = num_list[0]
			for n in range(1,len(num_list)) :
				res = res / num_list[n]
			return res
	
	def strip_white_space(self,expr) :
		stripped_expr = ''
		for exp in expr :
			if exp == ' ' :
				continue
			stripped_expr += exp
		return stripped_expr
	
	def buildTree(self,expr,prev_node=None) :
		for op in self.ops :
			if op in expr :
				expr = expr.split(op)
				node = Node(op)
				if prev_node :
					prev_node.child_nodes.append(node)
				else :
					self.head = node
				for exp in expr :
					exp = self.strip_white_space(exp)
					if exp in self.nums :
						node.vars.append(exp)
					else :
						self.buildTree(exp,prev_node=node)
		return
	
	def ComputeExpression(self,node=None) :
		if node :
			if node.child_nodes :
				res = []
				var_res = None
				for child in node.child_nodes :
					temp = self.ComputeExpression(node=child)
					res.append(temp)
				res_total = self.Compute_List(node.op,res)
				if node.vars :
					casted_vars = []
					for v in node.vars :
						casted_vars.append(float(v))
					var_res = self.Compute_List(node.op,casted_vars)
					if not res_total :
						return var_res
				if not var_res :
					return res_total
				return self.Compute_Scalers(node.op,res_total,var_res)
			if node.vars :
				casted_vars = []
				for v in node.vars :
					casted_vars.append(float(v))
				var_res = self.Compute_List(node.op,casted_vars)
				return var_res
	
	def printTree(self,node=None) :
		if node :
			if node.child_nodes :
				for child in range(len(node.child_nodes)) :
					self.printTree(node=node.child_nodes[child])
					if child+1 == len(node.child_nodes) :
						continue
					print(node.op,' ',end='')
			if node.vars :
				for v in range(len(node.vars)) :
					print(node.op,node.vars[v],' ',end='')
		return			
							

tree = ExpressionTree()
expr = "2*8 + 7 - 6 * 4/5"
tree.buildTree(expr)
tree.printTree(tree.head)
print('\n')
print(tree.ComputeExpression(tree.head))