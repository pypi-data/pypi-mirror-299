
open_brackets = ['[','{','(']
closing_brackets = [']','}',')']

def trim_space(line) :
	new_line = ''
	space = ' '
	for char in line :
		if char == space :
			continue
		new_line += char
	return new_line
	
def get_num(line,op,k,N) :
	b = ''
	M = len(line)
	for i in range(0,M) :
		if not line[i] in op :
			b += line[i]
			continue
		k = k+i+1
		break
	return b,k

def condition_split_v1(expr,oper='any') :
	elements = []
	element = ''
	operators = ['-','+','/','*','^']
	global open_brackets
	global closing_brackets
	op = operators
	if op != 'any' :
		op = oper
	i = 0
	found_bracket = False
	N = len(expr)
	count_ob = 0
	seperate = False
	k = 0
	count_cb = 0
	for i in range(N) :
		
		if i+k >= N :
			break
			
		if expr[i+k] in open_brackets :
			element += expr[i+k]
			count_ob += 1
			found_bracket = True
			continue
		if expr[i+k] in closing_brackets :
			element += expr[i+k]
			count_cb += 1
			if count_cb == count_ob :
				found_bracket = False
				elements.append(element)
				element = ""
			continue
		if found_bracket :
			element += expr[i+k]
			continue
		
		if expr[i+k] == '-' and expr[i+k+1] == '-' :
			#  -  -  = +
			# a - - b = a + b
			# a - - b*3 = a + b * 3+1
			a = element
			b,k = get_num(expr[i+k+2:],operators,i+k+2,N)
			element = a + '+' + b
			
			if oper == '+' :
				elements.append(a)
				elements.append(b)
				seperate = True
				continue
			
			if oper == 'any' :
				elements.append(a)
				elements.append(b)
				seperate = True
				continue
			if i+k+ 1 >= N :
				elements.append(element)
			continue

		if expr[i+k] == '-' and expr[i+k+1] == '+' or expr[i+k] == '+' and expr[i+k+1] == '-' :
			# - + = -
			# + - = -
			# -a - + b  = -a  - b
			# a + - b = a - b
			a = element
			b,k = get_num(expr[i+k+2:],operators,i+k+2,N)
			element = a + '-' + b
			
			if oper == '-' :
				elements.append(a)
				elements.append(b)
				seperate = True
				continue
			
			if oper == 'any' :
				elements.append(a)
				elements.append(b)
				seperate = True
				continue
			
			if i+k+1 >= N :
				elements.append(element)
			continue
		
		if expr[i+k] == '-' :
			# *-
			# /-
			
			if i+k-1 == -1 :
				element += '-'
				continue
			elif expr[i+k-1] in ['*','/','^'] :
				if oper == 'any' :
					elements.append(element)
					element = '-'
					continue
				element += '-'
				continue
		
		if not expr[i+k] in op :
			element += expr[i+k]
			if i+k + 1 == N :
				elements.append(element)
				break
			continue
		else :
			if seperate :
				element = ""
				seperate = False
				continue
			elements.append(element)
			element = ""
	return elements

"""
line = '-2*-3*-4+7--7'
line1 = '-7+-7'
print(condition_split_v1(line,'any'))
print(condition_split_v1(line1,'-'))
print(condition_split_v1('-2+3','+'))
print(condition_split_v1('8*3--3','-'))
print(condition_split_v1('2^-2','-'))
"""