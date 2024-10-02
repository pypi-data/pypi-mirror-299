
def get_num(line,ops) :
	N = len(line)
	offset = 0
	element = ''
	for i in range(N) :
		if not line[i] in ops :
			element += line[i]
		else :
			offset = i
			break
	return element,offset

def csp(line,op='+') :
	operators = ['+','-','*','/']
	count_ob = 0
	count_cb = 0
	i = 0
	N = len(line)
	elements = []
	flag = False
	element = ''
	while i < N :
		if i+1 >= N :
			break
		if line[i] == '-' :
			if i - 1 == -1 :
				element += line[i]
				i = i + 1
				continue
			#*-
			#/-
			elif line[i-1] in ['*','/'] :
				element += line[i]
				i = i + 1
				continue
				
		if line[i] == '-' and line[i+1] == '-' :
			# - - = +
			#  a - - b = a + b
			a = element
			b,offset = get_num(line[i+2:],operators)
			i = i + offset + 1
			element = a + '+' + b
			
			if op == 'any' :
				elements.append(a)
				elements.append(b)
				continue
			elements.append(element)
			element = ''
			continue
			
		if line[i] == '-' and line[i+1] == '+' and line[i] == '+' or line[i+1] == '-' :
			# - + = -
			# + - = -
			a = element
			b,offset = get_num(line[i+2:],operators)
			i = i + offset + 1
			
			if op == 'any' :
				elements.append(a)
				elements.append(b)
				flag = True
				continue
			if op == '-' :
				elements.append(a)
				elements.append(b)
				flag  = True
				continue
			elements.append(element)
			continue
			
		if not line[i] in op :
			element += line[i]
			if i + 1 == N :
				elements.append(element)
				break
			i = i + 1
			continue
		else :
			if flag :
				flag = False
				element = ""
				i = i + 1
				continue
			if element :
				elements.append(element)
			element = ""
			i = i + 1
	return elements
	
line = '-7--7'
print(csp(line,'-'))