class LoopNode :
	
	def __init__(self,) :
		self.syntax = []
		self.loop_body = []
	

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

def BuildTree(lines,indent,prev_node=None) :
	syntax = lines[0]
	node = LoopNode()
	node.syntax.append(syntax)
	if prev_node :
		prev_node.loop_body.append(node)
	i = 1
	N = len(lines)
	while i < N :
		line = lines[i]
		if line.split() == [] :
			i = i + 1
			continue
		if not HasIndent(line,indent) :
			print("indentation error :- {} ".format(indent),line)
			break
		if line.split()[0] == 'for' or line.split()[0] == 'while' :
			pos,_ = BuildTree(lines[i:],indent+4,prev_node=node)
			i = i + pos
			continue
		node.loop_body.append(line)
		i = i + 1
	return i,node
	
def PrintTree(node) :
	syntax = node.syntax[0].split()
	a = int(syntax[3])
	b = int(syntax[5])
	for i in range(a,b+1) :
		for line in node.loop_body :
			if type(line) == type(node) :
				PrintTree(line)
				continue
			print(line)
	return

Loop = ['for i = 1 to 10 :','    h = h + 1','    for j = 1 to 10 :','        pass','        loop','    a = a + 1','    h = h + 1']
L1 = ['for i = 2 to 7',"    for j = 1 to 3","        for k = 1 to 3","            pass","    pass"]
L2 = ['for i = 1 to 3','    for j = 1 to 3','        nes_loop','        for k = 1 to 2','            nes_nes_loop','    pass']
_,node = BuildTree(Loop,4)
PrintTree(node)
print(node.loop_body)
_,node1 = BuildTree(L2,4)
PrintTree(node1)
print(node1.loop_body)