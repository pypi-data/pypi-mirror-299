class LoopProcessingUnit:
	
	def __init__(self,indent="    ") :
		self.indent = indent
		if len(self.indent) == 0 :
			self.indent = "    "
		self.allowed_loops = ['for','while']
	
	def has_for_loop_syntax(self,line) :
		if line[2] == '=' :
			if line[4] == 'to' :
				if line[6] == ':' :
					return True
				return "Forget indentation [:]"
			return "Forgot [to]"
		return "Forgot [=]"
	
	def check_variable(self,var) :
		nums = '0123456789'
		alpha = 'abcdefghijklmnopqrstuvwxyz'
		if len(var) > 1 :
			if var[0] in nums :
				for v in range(1,len(var)) :
					if not var[v] in nums :
						print("{} incorrect variable name ".format(var))
						return False
				return True
			if var[0] in alpha :
				for v in range(1,len(var)) :
					if not var[v] in nums and not var[v] in alpha :
						print("{} incorrect variable name".format(var))
						return False
				return True
		if var in alpha :
			return True
		if var in nums :
			return True
		return False 
	
	def has_while_loop_syntax(self,line) :
		#while i [<,>,<=,>=] a :
		comparsion_operator = ['>','<','<=','>=']
		if line[2] in comparsion_operator :
			if line[-1] == ":" :
				return True
			return "Forgot indentation :"
		return "incorrect operator used in while loop"
	
	def check_syntax(self,line) :
		#for i = a to b :
		#while a [<,>,<=,>=] n :
		if type(line) == type([1]) :
			pass
		else :
			line = line.split()
		if line == [] :
			return False
		if len(line) == 7 :
			if line[0] == 'for' :
				val = self.has_for_loop_syntax(line)
				if val == True :
					i = line[1]
					a = line[3]
					b = line[5]
					vars = [i,a,b]
					bool_list = [self.check_variable(var) for var in vars]
					if False in bool_list :
						print("Variables are defined incorrectly in loop header")
						return False
					return True
				print('\n',val)
				return -2
		if len(line) == 5 :
			if line[0] == "while" :
				var = self.has_while_loop_syntax(line)
				if var == True :
					# while a < b :
					a = line[1]
					b = line[3]
					vars = [a,b]
					bool_list = [self.check_variable(var) for var in vars]
					if False in bool_list :
						print("Variables are defined incorrectly in loop header")
						return -2
					return True
				print('\n',var)
				return -2
		return False
		
	def has_valid_indent(self,line,bias_indent=0) :
		count = 0
		for l in line :
			if l != ' ' :
				if count != len(self.indent)+bias_indent :
					return False
				else :
					break
			if l == ' ' :
				if count == len(self.indent)+bias_indent :
					if self.has_valid_indent(line.split('    ')) :
						continue
					return False
				count += 1
		return True
		
	def Fetch_Loop_Body(self,lines,start,bias_indent=0) :
		loop_body = []
		line_num = 0
		print(lines)
		if type(lines) == type('a') :
			lines = lines.split('\n')
		for ii in range(start,len(lines)) :
			if self.has_valid_indent(lines[ii],bias_indent) :
				if lines[ii].split() == [] :
					continue
				loop_body.append(lines[ii].split())
			else :
				line_num = ii
				break
		return loop_body,line_num
	
	def Is_Num(self,st) :
		nums = '0123456789'
		for s in st :
			if not s in nums :
				return False
		return True
	
	def EvaluateLoop(self,loop_body) :
		loop_syntax = loop_body[0]
		if loop_syntax[0] == 'for' :
			#for i = a to b :
			step = 1
			i = loop_syntax[1]
			a = loop_syntax[3]
			b = loop_syntax[5]
			try :
				a = int(a)
				b = int(b)
			except :
				pass
			if a > b :
				step = -1
			for ii in range(a,b+1,step) :
				print(ii)
				#and also evaluating all loop bodies excpression
		if loop_syntax[0] == 'while' :
			#while a < b
			step = 1
			a = int(loop_syntax[1])
			b = int(loop_syntax[3])
			op = loop_syntax[2]
			if op == '<' :
				for i in range(a,b,step) :
					print(i)
				return
			if op == '>' :
				step = -1
				for ii in range(a,b,step) :
					print(ii)
				return
			if op == '>=' :
				step = -1
				for ii in range(a,b-1,step) :
					print(ii)
				return
			if op == '<=' :
				step = 1
				for ii in range(a,b+1,step) :
					print(ii)
				return
		return
	
	def HasNestedLoop(self,data) :
		print(data)
		for d in range(len(data)) :
			if self.check_syntax(data[d]) :
				return d	
		return False
		
	def process_loop(self,data,st=0,nes=0) :
		if type(data) == type([1]) :
			pass
		else :
			data = data.split('\n')
		loop_body = []
		loop_bodies = {}
		nested_loops = []
		N = len(data)
		ii = st
		count = 0
		while ii < N :
			prev_i = ii
			if self.check_syntax(data[ii]) :
				loop_body,ln = self.Fetch_Loop_Body(data[ii+1:],ii+1,nes)
				nes_ln = self.HasNestedLoop(loop_body)
				print(loop_body)
				if nes_ln :
					nested_loops = self.process_loop(loop_body,nes_ln,nes=nes+4)
				loop_body.insert(0,data[ii].split())
				if nested_loops :
					loop_bodies[str(count)+'_nes'] = nested_loops
				loop_bodies[str(count)] = loop_body
				loop_body = []
				nested_loops = []
				ii = ii + ln
				count = count + 1
			if ii > prev_i :
				continue
			ii = ii + 1	
				
		if loop_bodies == {} :
			return
		return loop_bodies
	
	def ProcessLoop(self,data) :
		loop_bodies = self.process_loop(data)
		for key in loop_bodies.keys():
			self.EvaluateLoop(loop_bodies[key])
		return
		
			
LPU = LoopProcessingUnit()
Loop = """
for i = 1 to 10 :
     for j = 1 to 10 :
		h = a + 1
	a = b + 1
while 10 > 1 :
	a = n + 2*n	
"""	
LPU.ProcessLoop(Loop)
print(LPU.process_loop("""for i = 1 to 3 :\n    for j = 1 to 3:\n    """))
print(LPU.check_syntax("for i = 1 to 10 :"))