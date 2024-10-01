class Compiler :
	
	def __init__(self,indent=4) :
		self.indent = indent
		self.error_code = False
		self.alpha = 'abcdefghijklmnopqrstuvwxyz'
		self.nums = '0123456789'
		self.GlobalVariables = {}
		self.LocalVariables = {}
		self.Variables = {'Global Variables' : self.GlobalVariables,'Local Variables' : self.LocalVariables}
		self.DataTypes = ['chars','int','float']
		self.LoopTypes = ['for','while']
		self.WhileLoopOp = ['<','>','<=','>=']
		self.chars_literals = self.alpha + self.nums
		self.int_literals = self.nums
		self.float_literals = self.nums
		self.Variables_Literals = {'int' : self.int_literals,'float' : self.float_literals,'chars' : self.chars_literals}
		
		
	
	def HasIndent(self,line,bias_indent=0) :
		if type(line) == type('a') :
			if '\n' in line :
				print("Error :- agr to this function HasIndent(str) must be of single line")
				return self.error_code
			count = 0
			for l in line :
				if l == ' ' :
					count = count  + 1
					continue
				break
			if count == self.indent + bias_indent :
				return True
			return False
		print("Error :- argument of incorrect data type provided to this function HasIndent(arg)")
		return
	
	def Is_single_line(self,line) :
		if type(line) == type('a') :
			if '\n' in line :
				return False
			return True
	
	def Split(self,st,char=' ') :
		new_str = []
		str_ = ''
		for s in st :
			if s == char :
				str_ = ''
				new_str.append(str_)
				continue
			str_ += s
		return new_str
		
	def ProcessVariable(self,line,scope='Global Variables') :
		if self.Is_single_line(line) :
			#DataType VarName = Value
			line = line.split()
			N = len(line)
			if N == 0 or N == 1 :
				return
			if '=' in line :
				if line[0] in self.DataTypes :
					N = 4
				else :
					N = 3
			if N == 4 :
				if line[0] in self.DataTypes :
					data_type = line[0]
					var_name = line[1]
					if not line[2] == '=' :
						print("Incorrect Syntax {}".format(line))
						return
					if not self.CheckVariableName(var_name) :
						 return
					var_val = line[3]
					var_lit = self.Variables_Literals[data_type]
					
					if data_type == 'int' :
						#int a = 2
						for v in var_val :
							if not v in var_lit :
								print("Incorrect Value assigned to the variable {}".format(line))
								return
						Var = self.Variables[scope]
						if var_name in Var.keys() :
							print("Error Variable is already defined {}".format(self.Variables[var_name]))
							return
						self.Variables[scope][var_name] = [var_val,data_type]
						return
					if data_type == 'float' :
						#float b = 1.2
						for v in range(len(var_val)) :
							if var_val[v] == '.' :
								continue
							if not var_val[v] in var_lit :
								print("Incorrect Value Assigned to the variable {}".format(line))
								return
						Var = self.Variables[scope]
						if var_name in Var.keys() :
							print("Error Variable is already defined {}".format(Var[var_name]))
							return
						self.Variables[scope][var_name] = [var_val,data_type]
						return
					if data_type == 'chars' :
						#chars name = '123'
						temp_val = ''
						if len(line[3:]) > 1 :
							N = len(line[3:])
							temp_line = line[3:]
							for v in range(N) :
								temp_val += temp_line[v]
								if v+1 == N :
									continue
								temp_val += ' '
							var_val = temp_val.lower()
						del temp_val
						if var_val[0] == "'" and var_val[-1] == "'" :
							for v in range(1,len(var_val)-1) :
								if var_val[v] == ' ' :
									continue
								if not var_val[v] in var_lit :
									print("Incorrect value assigned to the variable {}".format(line))
									return
							print(var_val)
							Var = self.Variables[scope]
							if var_name in Var.keys() :
								print("Error value of this variable is already defined {}".format(Var[var_name]))
								return
							self.Variables[scope][var_name] = [var_val,data_type]
							return
						print("Error string values must be put inside 'val' single quotation {}".format(var_val))
						return
			if N == 3  :
				# a = 1
				var_name = line[0]
				Var = self.Variables[scope]
				if not var_name in Var.keys() :
					print("Error Variable must be define before assigning values to it {}".format(line))
					return
				if line[1] != '=' :
					print("Error incorrect Syntax {}".format(line))
					return
				_,data_type = Var[var_name]
				var_lit = self.Variables_Literals[data_type]
				var_val = line[2]
				if data_type == 'int' :
						#int a = 2
						for v in var_val :
							if not v in var_lit :
								print("Incorrect Value assigned to the variable {}".format(line))
								return
						self.Variables[scope][var_name] = [var_val,data_type]
						return
				if data_type == 'float' :
					#float b = 1.2
						for v in range(len(var_val)) :
							if var_val[v] == '.' :
								continue
							if not var_val[v] in var_lit :
								print("Incorrect Value Assigned to the variable {}".format(line))
								return False
						self.Variables[scope][var_name] = [var_val,data_type]
						return
				if data_type == 'chars' :
						#chars name = 'Connie Talbot'
						#chars name = 'Mackenzie Foy'
						temp_val = ''
						temp_list = line[2:]
						if len(temp_list) > 1 :
							for i in range(len(temp_list)) :
								temp_val += temp_list[i]
								if i+1 == len(temp_list) :
									break
								temp_val += ' '
							var_val = temp_val
							del temp_val
						del temp_list
						if var_val[0] == "'" and var_val[-1] == "'" :
							for v in range(1,len(var_val)-1) :
								if var_val[v] == ' ' :
									continue
								if not var_val[v].lower() in var_lit :
									print("Incorrect value assigned to the variable {}".format(line))
									return
							self.Variables[scope][var_name] = [var_val,data_type]
							return
						print("Error string values must be put inside 'val' single quotation {}".format(var_val))
						return
	
	def ProcessLines(self,lines) :
		if type(lines) == type('a') :
			if '\n' in lines :
				lines = lines.split('\n')
		if lines == [] :
			return
		self.loop_bodies = {}
		i = 0
		loop_count = 0
		N = len(lines)
		while i < N :
			line = lines[i]
			if line.split() == [] :
				i = i + 1
				continue
			"""
			if not self.HasIndent(line,-self.indent) :
				print("Indentation error at line {} {}".format(i,line))
				return
			"""
			if line.split()[0] in self.LoopTypes :
				if not self.LoopSyntax(line) :
					return
				loop_body,pos = self.FetchLoopBody(lines[i+1:])
				if not loop_body:
					i = i + pos + 1
					continue
				self.loop_bodies['for_'+str(loop_count)] = loop_body
				pos = pos + 1
				i = i + 1
				continue
			print(line)
			self.ProcessVariable(line)
			i = i + 1
		
	def LoopSyntax(self,line) :
		line = line.split()
		#for int i = a to b :
		#while int i [<,>,<=,>=] b :
		if len(line) == 8 or len(line) == 7:
			#[for,int, i , =,a,to,  b,  :  ]
			#  0    1   2  3 4  5   6 7
			pos = 0
			if len(line) == 8 :
				pos = 1
			var_i = line[1+pos]
			if line[2+pos] != '=' :
				print("Syntax Error {}".format(line))
				return
			if line[4+pos] != 'to' :
				print("Syntax Error {}".format(line))
				return
			if line[6+pos] != ':' :
				print("Syntax Error {}".format(line))
				return
			a = line[3+pos]
			b = line[5+pos]
			vars = [var_i,a,b]
			for v in vars :
				if not self.CheckVariableName(v) :
					return
			return True	
		if len(line) == 6 or len(line) == 5 :
			#while int a < b :
			pos = 0
			if len(line) == 6 :
				pos = 1
			var_i = line[1+pos]
			if not line[2+pos] in self.WhileLoopOp :
				print("Error Syntax {}".format(line))
				return
			if not line[4+pos] == ':' :
				print("Syntax Error {}".format(line))
				return
			a =line[1+pos]
			b = line[3+pos]
			vars = [var_i,a,b]
			for v in vars :
				if not self.CheckVariableName(v) :
					return
			return True
			
	def FetchLoopBody(self,lines,indent=0) :
		loop_body = []
		i = 0
		N = len(lines)
		while i < N :
			line = lines[i]
			if line.split() == [] :
				i = i + 1
				continue
			if not self.HasIndent(line,indent) :
				break
			if line.split()[0] in self.LoopTypes :
				if self.LoopSyntax(line) :
					nes_loop,pos = self.FetchLoopBody(lines[i+1:],indent+self.indent)
					print("here nes ",nes_loop)
					pos = pos + 1
					loop_body.append(line)
					loop_body.append(nes_loop)
					i = i + pos
					continue
				print("Syntax Error {}".format(line))
				return [],0
			
			print("here ",line)
			loop_body.append(line)
			i = i + 1
			continue
		return loop_body,i
		
	def CheckVariableName(self,var_name) :
		if type(var_name) == type('a') :
			if '\n' in var_name :
				print("Error argument must be of single line while giving it to this function CheckVariableName(line)")
				return
			if var_name[0].lower() in self.alpha :
				for i in range(1,len(var_name)) :
					if not var_name[i].lower() in self.nums+self.alpha :
						print("Incorrect variable name {}".format(var_name))
						return
				if var_name in self.DataTypes :
					print("Incorrect Variable name {}".format(var_name))
				return True
			if var_name[0] in self.nums :
				for i in range(1,len(var_name)) :
					if var_name[i].lower() in self.alpha :
						print("Incorrect variable name {}".format(var_name))
						return
				return True

a = """
int a = 1
chars b = 'a'
float s = 2.0
s = 43.554387483
for int i = 1 to 2 :
     a = a + 1
     break
     for j = 1 to 4 :
     	pass
     	hey
     a = a + 1
chars f = 'fx'
f = 'gx'
chars name = 'Pinku Khare'
name = 'Prakamya Khare'
"""

c = Compiler(5)
c.ProcessLines(a)
print(c.GlobalVariables)
print(c.loop_bodies)	