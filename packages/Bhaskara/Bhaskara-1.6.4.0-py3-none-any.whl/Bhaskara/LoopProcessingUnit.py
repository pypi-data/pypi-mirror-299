def HasIndent(line,indent) :
	count = 0
	for l in line :
		if l == ' ' :
			count += 1
			continue
		break
	if count == indent :
		return True
	return False

def LoopBody(lines,indent) :
	if type(lines) == type('a') :
		lines = lines.split('\n')
	loop_body = []
	loops = ['for','while']
	i = 0
	N = len(lines)
	while i < N :
		line = lines[i]
		nested_loop = []
		if line.split() == [] :
			i = i + 1
			continue
		if HasIndent(line,indent) :
			if line.split()[0] in loops :
				nested_loops,pos = LoopBody(lines[i+1:],indent+4)
				loop_body.append(line)
				loop_body.append(nested_loops)
				pos = pos + 1
				i = i + pos
				continue
			loop_body.append(line)
			i = i + 1
			continue
		break
	return loop_body,i

def ProcessLoop(lines,indent) :
	if type(lines) == type('a') :
		lines = lines.split('\n')
	loop_bodies = {}
	Loops = ['for','while']
	count = 0
	loop_body = []
	i = 0
	N = len(lines)
	while i < N :
		line = lines[i]
		if line.split() == [] :
			i = i + 1
			continue
		if line.split()[0] in Loops :
			loop_body,pos = LoopBody(lines[i+1:],indent)
			loop_body.insert(0,line)
			loop_bodies[str(count)] = loop_body
			count = count + 1
			pos = pos + 1
			i = i + pos
			continue
		i = i + 1
	return loop_bodies
L = """
for i = 1 to N :
    h = h + 1
    while a < 1 :
        j = j + 1
        for j = 1 to H :
            pass
            pass
            pass
    return True
for i = 1 to N :
    for j = 1 to M :
        for k = 1 to O :
            a  = arr[i,j,k]
    a = 1
h = h + 1
a  = a + 1
"""

l = ProcessLoop(L,4)
print(l)