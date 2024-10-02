def tokenize_defining_variable(line,self=None) :
	data_type = ""
	name = ""
	value  = ""
	found_eq = False
	for char in line :
		if not data_type in ['int','chars','float'] :
			if char == " " :
				continue
			data_type += char
			continue
		if char == '=' :
			found_eq = True
			continue
		if found_eq :
			value += char
			continue
		if char != ' ' :
			name += char
	return data_type,name,value

"""
line = 'int a=23723 '
print(tokenize_defining_variable(line))
line = 'chars name=  " Prakamya Khare sks " '
print(tokenize_defining_variable(line))
"""