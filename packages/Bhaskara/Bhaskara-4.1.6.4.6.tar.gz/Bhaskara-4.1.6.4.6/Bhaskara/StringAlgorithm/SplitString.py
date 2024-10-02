def split(line,char=',') :
	new_line = []
	found_b = False
	params = ''
	open_b = ['[','(','{',"'"]
	closing_b = [']',')','}',"'"]
	
	for i in range(len(line)) :
		if line[i] in open_b :
			params += line[i]
			found_b = True
			continue
		if line[i] in closing_b :
			params += line[i]
			found_b = False
			if i+1 == len(line) :
				new_line.append(params)
			continue
		if found_b :
			if line[i] == ' ' :
				continue
			params += line[i]
			continue
		if line[i] == char :
			new_line.append(params)
			params = ''
			continue
		params += line[i]
		if i+1 == len(line) :
			new_line.append(params)
	return new_line

"""	
split("arr[i+1,j+1]")
"""