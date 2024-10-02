operators = ['+','-','*','/','^']
open_brackets = ['[','{','(']
closing_brackets = [']',')','}']


def get_number(expr,op) :
	chars = ''
	N = len(expr)
	k = 0
	for i in range(N) :
		if not expr[i] in op :
			chars += expr[i]
		else :
			k = i
			break
	return chars,k
	
def trim_space(line) :
	clean_line = ''
	for i in line :
		if i == ' ' :
			continue
		clean_line += i
	return clean_line

def condition_split_v2(expr,op='any') :
	space = ' '
	if space in expr :
		expr = trim_space(expr)
	global operators
	global open_brackets
	global closing_brackets
	found_bracket = False
	elements = []
	element   = ''
	count_ob = 1
	count_cb = 1
	flag  = False
	N = len(expr)
	k  = 0
	if op == 'any' :
		op = operators

	for i in range(N) :
		
		if i+k == N :
			break
		
		if expr[i+k] in open_brackets :
			found_bracket = True
			element += expr[i+k]
			count_ob = count_ob + 1
			continue
		if expr[i+k] in closing_brackets :
			element += expr[i+k]
			count_cb = count_cb + 1
			if count_cb == count_ob :
				found_bracket = False
			if i+k+1 >= N :
				elements.append(element) 
			continue
			 
		if found_bracket :
			element += expr[i+k]
			continue
		
		
		if expr[i+k] == '-' and expr[i+k+1] == '-' :
			# - - = +
			# a - - b = a + b
			a = element
			b,k = get_number(expr[i+k+2:],operators)
			element = a + '+' + b
			k = k + 2
			M = len(element)
			if op == 'any' :
				elements.append(a)
				elements.append(b)
				flag = True
			
			if op == '+' :
				elements.append(a)
				element = b
				flag  = True
				
			
			if M == N - 1 :
				if not flag :
					elements.append(element)
				else :
					elements.append(b)
				break
		
		if expr[i+k] == '-' and expr[i+k+1] == '+' or expr[i+k] == '+' and expr[i+k+1] == '-' :
			# - + = -
			# + - = -
			# a - + b = a - b
			 a  = element
			 b,k = get_number(expr[i+k+2:],operators)
			 element = a + '-' + b
			 k = k + 2
			 M = len(element)
			 
			 if op == 'any' :
			 	elements.append(a)
			 	elements.append(b)
			 	flag = True
			 	
			 
			 if op == '-' :
			 	elements.append(a)
			 	element = b
			 	flag = True
			 
			 if M == N - 1 :
			 	if not flag :
			 		elements.append(element)
			 	else :
			 		elements.append(b)
			 	break
			 
		if expr[i+k] == '-' :
			if i+k-1 == -1 :
				element += '-'
				continue
			
			#*-
			#*/
			if expr[i+k-1] in ['*','/','^'] :
				element += '-'
				continue
		
		if not expr[i+k] in op :
			element += expr[i+k]
			if i+k+1 == N :
				 elements.append(element)
				 break
			continue
		else :
			if flag :
				elements.append(element)
				element = ''
				flag = False
				continue
			elements.append(element)
			element = ''
	return elements

"""
line = '-7--7'
line2 = '-3*-2--3+4'
print(condition_split_v2(line,'+'))
print(condition_split_v2(line2,'any'))
v1= condition_split_v2('-6-+6*8','-')
print(v1)
print(condition_split_v2(v1[0],'-'))
print(condition_split_v2('-3--4*3-9','+'))
print(condition_split_v2('-arr[I+1]--a','+'))
line = '-6--6*8'
print(condition_split_v2(line,'+'))
print(condition_split_v2(' a*fact(x)','*'))
print(condition_split_v2('a*fact(x)','*'))
print(condition_split_v2('2--2','+'))
print(condition_split_v2('6*2+2','+'))
res = condition_split_v2('6*6+3','+')
print(res)
print(condition_split_v2(res[0],'*'))
print(condition_split_v2('2^-2','-'))
"""