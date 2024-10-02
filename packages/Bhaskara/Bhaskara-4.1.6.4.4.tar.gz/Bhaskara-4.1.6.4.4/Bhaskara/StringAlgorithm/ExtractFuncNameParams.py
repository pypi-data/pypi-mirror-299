def extract_name_param(line) :
	name = ''
	param = ''
	is_found = False
	#f(g(x))
	ob_count = 0
	N = len(line)
	for i in range(N-1) :
		if line[i] == '(' :
			if ob_count == 1 :
				param += line[i]
				continue
			ob_count += 1
			is_found = True
			continue
		if not is_found :
			name += line[i]
			continue
		param += line[i]
	
	return name,param,is_found
	
#print(get_func_param('pow(a,a,b)'))