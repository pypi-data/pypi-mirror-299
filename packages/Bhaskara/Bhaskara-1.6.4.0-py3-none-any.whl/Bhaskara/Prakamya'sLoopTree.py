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

def BuildTree(lines,prev_node=None,indent=4) :
	syntax = lines[0]
	node = LoopNode()
	node.syntax.append(syntax)
	pos = 0
	rec = 0
	if prev_node :
		prev_node.loop_body.append(node)
	for i in range(1,len(lines)) :
		if pos+i == len(lines) :
			rec = pos + i
			break
		line = lines[i+pos]
		if not HasIndent(line,indent) :
			break
		if line.split()[0] == 'for' or line.split()[0] == 'while' :
			pos,_ = BuildTree(lines[i+pos:],prev_node=node,indent = indent+4)
			pos = pos + 1
			continue
		print(line)
		node.loop_body.append(line)
	return rec,node
	
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

Loop = ['for i = 1 to 10 :','    h = h + 1','    for j = 1 to 10 :','        pass','        loop','    a = a + 1']
_,node = BuildTree(Loop)
PrintTree(node)
print(node.loop_body)