
def condition_split(line,op='+') :
	#1+arr[j]*arr[j+1]
	element = ''
	open_brackets = ['[','{','(']
	closing_brackets = [']','}',')']
	operators = ['+','-','*','/','^']
	elements = []
	N = len(line)
	found_bracket = False
	open_bracket = 0
	closing_bracket = 0
	for i in range(N) :
		
		if line[i] in open_brackets :
			element += line[i]
			found_bracket = True
			open_bracket += 1
			continue
		if line[i] in closing_brackets :
			element += line[i]
			closing_bracket += 1
			if closing_bracket == open_bracket :
				found_bracket = False
				closing_bracket = 0
				open_bracket = 0
			if i+1 == N :
				elements.append(element)
			continue
		if found_bracket :
			element += line[i]
			continue
		if op == 'any' :
			pos = -1
			if line[i] in operators :
				if i-1 == -1 :
					element += line[i]
					pos = i
				elif line[i-1] in operators :
					element += line[i]
					pos = i
			if  not line[i] in operators :
				element += line[i]
				pos = 0
				if i+1 == N :
					elements.append(element)
			else :
				if pos != -1 :
					continue
				elements.append(element)
				element = ''
		else :
			pos = -1
			if line[i] in operators :
				if i-1 == -1 :
					element += line[i]
					pos = 0
				#$elif line[i]
				elif line[i-1] in operators :
					if line[i] == '-' and line[i-1] == '-' :
						# - - = +
						pos = 0
						#element += '+'
					else :
						element += line[i]
						pos = 1
			if  line[i] != op :
				if pos == 0 and i-1 == -1 :
					continue
					
				element += line[i]
				if i+1 == N :
					elements.append(element)
				continue
			else :
				if pos != -1 :
					continue
				elements.append(element)
				element = ""
	return elements
	
"""
line = 'arr[i*1]*2*arr[j*2*2]*7'
line1 = '((1+2)+2)+5+6'
print(condition_split(line,op='*'))
print(condition_split(line1,op='+'))
print(condition_split('arr[i+1]',op='+'))
print(condition_split('2+3','+'))
print(condition_split('arr[i*1]+arr[k+1]/2+3','any'))
print(condition_split('pow(2+3,4*8)*pow(23,4+4)+f(2/3)','any'))
line = '-res+234*-544+-343'
print(condition_split(line,'any'))
print(condition_split('-2*2-3+4','+'))
print(condition_split('4-3+-2/4','-'))
print(condition_split('-3-2*2','any'))
print(condition_split('2+2','any'))
"""
#print(condition_split('-6-+6*8','-'))