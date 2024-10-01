class LoopProcessingUnit :
	
	def __init__(self,indent="    ") :
		self.indent = indent
		self.for_loop_syntax = ['=','to',':']
		self.error_code = -222
		self.while_loop_syntax = ['<,>,<=,>=',':']
		if len(self.indent) == 0 :
			self.indent = "    "
	
	def check_variable(self,var) :
		if type(var) == type('a') :
			alpha = 'abcdefghijklmnopqrstuvwxyz'
			nums = '0123456789'
			
			if not '\n' in var :
				if var[0] in alpha :
					for i in range(1,len(var)) :
						if not var[i] in alpha and not var[i] in nums :
							print("Incorrect Variable name {}".format(var))
							return False
					return True
				if var[0] in nums :
					for i in range(1,len(var)) :
						if var[i] in alpha :
							print("Incorrect variable name {}".format(var))
							return False
					return True
			print("string given to check_varaible(str)  must be of single line")
			return self.error_code
	
	def Check_Indent(self,line,bias_indent=0) :
		if type(line) == type('a') :
			if '\n' in line :
				print("str given to Check_Indent func must be a single line string")
				return self.error_code
			count_indent = 0
			for char in line :
				if char == ' ' :
					count_indent += 1
				else :
					break
			if count_indent == len(self.indent) + bias_indent :
				return True
			print("incorrect number of indent {} provided at line {}".format(count_indent,line))
			return False
		print("line arg to Check_Indent() func must be a string ")
		return self.error_code
	
	def FetchLoopBody(self,lines,bias_indent=0) :
		if type(lines) == type('a') :
			if '\n' in lines :
				lines = lines.split('\n')
		if lines == [] :
			return
		loop_body = []
		pos = -1
		for i in range(len(lines)) :
			line = lines[i]
			nes_ind = None
			if self.Check_Syntax(line) :
				nes_loop,ind = self.FetchLoopBody(lines[i+1:],bias_indent+8)
			if self.Check_Indent(line,bias_indent) :
				loop_body.append(line)
			else :
				pos = i
		return loop_body,pos
		
	def HasNestedLoop(self,loop_body,bias_indent=4) :
		if loop_body :
			for i in range(len(loop_body)) :
				line = loop_body[i]
				if self.Check_Syntax(line) :
					return i
		return 0
	
	def ProcessLoop(self,lines,bias_indent=0) :
		if type(lines) == type('a') :
			if '\n' in lines :
				lines = lines.split('\n')
		if lines == [] :
			return
		loop_bodies = {}
		count = 0
		i = 0
		while i < len(lines) :
			line = lines[i]
			if self.Check_Syntax(line) :
				loop_body,_ = self.FetchLoopBody(lines[i+1:],bias_indent)
				nes_loop_body = []
				line_n = self.HasNestedLoop(loop_body,8+bias_indent)
				if line_n :
					nes_loop_body = self.ProcessLoop(loop_body[line_n:],bias_indent=8)
				loop_bodies[str(count)] = [loop_body,nes_loop_body]
				i = i + len(loop_body) 
			else :
				i = i + 1
		return loop_bodies
	
	def Check_Syntax(self,line) :
		if type(line) == type('a') :
			line = line.split()
		if len(line) == 7 :
			if line[0] == 'for' :
				#for i = a to b :
				i = line[1]
				equal_notation = line[2]
				a = line[3]
				to = line[4]
				b = line[5]
				indent = line[6]
				vars = [i,a,b]
				has_incorrect_syntax = False
				has_incorrect_var = False
				syntaxs = [equal_notation,to,indent]
				for i in range(len(self.for_loop_syntax)) :
					if not syntaxs[i] == self.for_loop_syntax[i] :
						print('incorrect syntax {}'.format(syntaxs[i]))
						has_incorrect_syntax = True
				if has_incorrect_syntax :
					return self.error_code
				for v in vars :
					if self.check_variable(v) :
						pass
					else :
						has_incorrect_var = True
				
				if has_incorrect_var :
					return self.error_code
				return True
				
			if len(line) == 5 :
				if line[0] == 'while' :
					#while a [<,>,<=,>=] b :
					a = line[1]
					op = line[2]
					b = line[3]
					ind = line[4]
					vars = [a,b]
					syntax = [op,ind]
					has_incorrect_var = False
					has_incorrect_syn = False
					for i in range(len(syntax)) :
						ops = self.while_loop_syntax[i]
						if i == 0 :
							ops = ops.split(',')
							if not syntax[i] in ops :
								print("incorrect syntax {}".format(syntax[i]))
								has_incorrect_syn = True
						
						if syntax[i] != ops :
							print("incorrect syntax {}".format(syntax[i]))
							has_incorrect_syn = True
					if has_incorrect_syn :
						return self.error_code
					for v in vars :
						if not self.check_variable(v) :
							has_incorrect_var = True
					if has_incorrect_var :
						return self.error_code
					return True
				return False

			
LPU = LoopProcessingUnit()
lp = """
for i = 1 to n :
    a = a + 1
    while j < r :
        b = b + r
        for h = 1 to n :
            a = a + 1
    return
return a

"""
print(LPU.ProcessLoop(lp))
			