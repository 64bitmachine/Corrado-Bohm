import sys

bb_value=1
tt_value=0

class Node:
	def __init__(self):
		self.list = []
		self.value = ''
		self.elsepart=0 

	def addChild(self,node):
		self.list.append(node)
		
	def printTree(self, x=0):
		s=""
		for i in range(x):
			s+='\t'
		s+=self.value
		print(s)
		if len(self.list)==0:
			return
		s1=""
		for i in range(x):
			s1+='\t'
		s1+='('
		print(s1)
		k=0
		for node in self.list:
			if (k!=0):
				s2=""
				for i in range(x+1):
					s2+='\t'
				s2+=","
				print(s2)
			k+=1
			node.printTree(x+1)
		s3=""
		for i in range(x):
			s3+='\t'
		s3+=')'
		print(s3)
		# log = open("text.txt", "w")
		# print >>log, s

class BasicBlock:
	def __init__(self):
		self.Type="None"
		self.Svalue=0
		self.Evalue1=0
		self.Evalue2=0
		self.child=[]
		self.elchild=[]
		self.condition_node=0

def CFGTree(list_of_ASTnodes):
	# print type(list_of_ASTnodes)
	cfg_nodes=[]
	# print len(list_of_ASTnodes)
	if (len(list_of_ASTnodes)==0):
		return
	i=0
	while True:
		# print list_of_ASTnodes[i].value
		if (list_of_ASTnodes[i].value == 'IF'):
			current = BasicBlock()
			current.Type = "IF"
			# print "elsepart ", list_of_ASTnodes[i].elsepart
			current.condition_node = list_of_ASTnodes[i].list[0]
			if list_of_ASTnodes[i].elsepart == 0:
				# print "hello"
				current.child = CFGTree(list_of_ASTnodes[i].list[1:])
			else:
				# print list_of_ASTnodes[i].list
				current.child = CFGTree(list_of_ASTnodes[i].list[1:list_of_ASTnodes[i].elsepart])
				current.elchild = CFGTree(list_of_ASTnodes[i].list[list_of_ASTnodes[i].elsepart:len(list_of_ASTnodes[i].list)])
				# print list_of_ASTnodes[i].list[1:list_of_ASTnodes[i].elsepart]
				# print list_of_ASTnodes[i].list[list_of_ASTnodes[i].elsepart:len(list_of_ASTnodes[i].list)]
			cfg_nodes.append(current)
			i+=1
		elif (list_of_ASTnodes[i].value == 'WHILE'):
			current = BasicBlock()
			current.Type = "WHILE"
			current.condition_node = list_of_ASTnodes[i].list[0]
			current.child = CFGTree(list_of_ASTnodes[i].list[1:])
			cfg_nodes.append(current)
			i+=1
		else:
			current = BasicBlock()
			current.Type = 'ASGN'
			while list_of_ASTnodes[i].value == 'ASGN':
				current.child.append(list_of_ASTnodes[i])
				i+=1
				if i >= len(list_of_ASTnodes):
					break
			cfg_nodes.append(current)
		
		if i >= len(list_of_ASTnodes):
			break

	return cfg_nodes

def lhs(data):
	if (data.value[0] == 'V'):
		# print len(data.value)
		return data.value[4:len(data.value)-1]
	if data.value == 'DEREF':
		return "*"+lhs(data.list[0])
	if data.value == 'UMINUS':
		return "-"+lhs(data.list[0])

def rhs(data):
	global tt_value
	if data.value == 'DEREF':
		return "*"+rhs(data.list[0])
	elif data.value == 'UMINUS':
		return "-"+rhs(data.list[0])
	elif (data.value[0] == 'V'):
		# print len(data.value)
		return data.value[4:len(data.value)-1]
	elif (data.value[0] == 'C'):
		return data.value[6:len(data.value)-1]
	elif data.value == 'ADDR':
		return "&"+rhs(data.list[0])
	elif data.value == 'PLUS':
		oper1 = rhs(data.list[0])
		oper2 = rhs(data.list[1])
		print("t"+str(tt_value)+" = "+oper1 + " + " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)
	elif data.value == 'MINUS':
		oper1 = rhs(data.list[0])
		oper2 = rhs(data.list[1])
		print("t"+str(tt_value)+" = "+oper1 + " - " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)
	elif data.value == 'MUL':
		oper1 = rhs(data.list[0])
		oper2 = rhs(data.list[1])
		print("t"+str(tt_value)+" = "+oper1 + " * " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)
	elif data.value == 'DIV':
		oper1 = rhs(data.list[0])
		oper2 = rhs(data.list[1])
		print("t"+str(tt_value)+" = "+oper1 + " / " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)

def CFGASGN(data):
	return lhs(data.list[0]) + " = " + rhs(data.list[1])

def CFGCOND(data):
	global tt_value
	if data.value == "LE":
		oper1 = CFGCOND(data.list[0])
		oper2 = CFGCOND(data.list[1])
		print("t"+str(tt_value)+" = " + oper1 + " <= " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)
	elif data.value == "MUL":
		oper1 = CFGCOND(data.list[0])
		oper2 = CFGCOND(data.list[1])
		print("t"+str(tt_value)+" = " + oper1 + " * " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)
	elif data.value == "DIV":
		oper1 = CFGCOND(data.list[0])
		oper2 = CFGCOND(data.list[1])
		print("t"+str(tt_value)+" = " + oper1 + " / " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)
	elif data.value == "PLUS":
		oper1 = CFGCOND(data.list[0])
		oper2 = CFGCOND(data.list[1])
		print("t"+str(tt_value)+" = " + oper1 + " + " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)
	elif data.value == "MINUS":
		oper1 = CFGCOND(data.list[0])
		oper2 = CFGCOND(data.list[1])
		print("t"+str(tt_value)+" = " + oper1 + " - " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)
	elif data.value == "LT":
		oper1 = CFGCOND(data.list[0])
		oper2 = CFGCOND(data.list[1])
		print("t"+str(tt_value)+" = " + oper1 + " < " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)
	elif data.value == "NE":
		oper1 = CFGCOND(data.list[0])
		oper2 = CFGCOND(data.list[1])
		print("t"+str(tt_value)+" = " + oper1 + " != " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)
	elif data.value == "GE":
		oper1 = CFGCOND(data.list[0])
		oper2 = CFGCOND(data.list[1])
		print("t"+str(tt_value)+" = " + oper1 + " >= " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)
	elif data.value == "GT":
		oper1 = CFGCOND(data.list[0])
		oper2 = CFGCOND(data.list[1])
		print("t"+str(tt_value)+" = " + oper1 + " > " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)
	elif data.value == "EQ":
		oper1 = CFGCOND(data.list[0])
		oper2 = CFGCOND(data.list[1])
		# print oper1,oper2
		print("t"+str(tt_value)+" = " + oper1 + " == " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)
		# return CFGCOND(data.list[0]) + " == " + CFGCOND(data.list[1])
	elif data.value == "DEREF":
		return "*"+CFGCOND(data.list[0])
	elif data.value == "UMINUS":
		return "-"+CFGCOND(data.list[0])
	elif data.value == "AND":
		oper1 = CFGCOND(data.list[0])
		oper2 = CFGCOND(data.list[1])
		print("t"+str(tt_value)+" = " + oper1 + " && " + oper2)
		tt_value+=1
		return "t"+str(tt_value-1)
	elif data.value == "OR":
		print("t"+str(tt_value)+" = " + CFGCOND(data.list[0]) + " || " + CFGCOND(data.list[1]))
		tt_value+=1
		return "t"+str(tt_value-1)
	elif data.value[0] == 'C':
		# print "hello"
		return data.value[6:len(data.value)-1]
	elif data.value[0] == 'V':
		return data.value[4:len(data.value)-1]


def changeEvalue(data, value):
	# print len(data)
	# print data.
	if(data[len(data)-1].Type == 'ASGN'):
		data[len(data)-1].Evalue1 = value
	if(data[len(data)-1].Type == 'IF'):
		changeEvalue(data[len(data)-1].child, value)
		changeEvalue(data[len(data)-1].elchild, value)
	if(data[len(data)-1].Type == 'WHILE'):
		data[len(data)-1].Evalue2 = value
	# print data[len(data)-1].Type
	# if (len(data[len(data)-1].elchild)):
	# 	changeEvalue(data[len(data)-1].elchild, value)

	# if (len(data[len(data)-1].child)):
	# 	changeEvalue(data[len(data)-1].child, value)
	# for child in data[len(data)-1].child:
	# 	changeEvalue(child, value)

def printCFG(root):
	global bb_value
	global tt_value
	# for child in root:
	# 	print child.Type
	# return
	for child in root:
		if child.Type == 'ASGN':
			child.Svalue = bb_value
			# print "<bb " + str(bb_value) + ">"
			bb_value+=1
			# for sub_child in child.child:
				# CFGASGN(sub_child)
			# print "goto <bb " + str(bb_value) + ">\n"
			child.Evalue1 = bb_value
		elif child.Type == 'IF':
			# print "length ", len(child.elchild)
			# print "<bb " + str(bb_value) + ">"
			child.Svalue = bb_value
			# print child.condition_node
			# CFGCOND(child.condition_node)
			# print "t"+ str(tt_value)+ " = " + CFGCOND(child.condition_node)
			bb_value+=1
			# print "if"+"(t"+ str(tt_value-1)+") " + "goto <bb " + str(bb_value)+">"
			child.Evalue1 = bb_value
			printCFG(child.child)
			child.Evalue2 = bb_value
			if (len(child.elchild)):
				child.Evalue2 = bb_value
				printCFG(child.elchild)
				endval = bb_value
				changeEvalue(child.child, endval)
			# print "else goto <bb " + str(bb_value)+">"
			# child.Evalue=bb_value
		else:
			# while case
			# print "<bb " + str(bb_value) + ">"
			child.Svalue = bb_value
			# CFGCOND(child.condition_node)
			# print "t"+ str(tt_value)+ " = " + CFGCOND(child.condition_node)
			bb_value+=1
			child.Evalue1 = bb_value
			# tt_value+=1
			# print "if"+"(t"+ str(tt_value)+") " + "goto <bb " + str(bb_value)+">"
			printCFG(child.child)
			changeEvalue(child.child, child.Svalue)
			child.Evalue2 = bb_value
			# print "else goto <bb " + str(bb_value)+">"
			# child.Evalue1=bb_value
	return root

def CFGPrint(root):
	# print "============="
	for child in root:
		if child.Type == 'ASGN':
			print('<bb '+str(child.Svalue)+'>')
			for sub_child in child.child:
				print(CFGASGN(sub_child))
			print('goto <bb '+str(child.Evalue1)+'>\n')
		if child.Type == 'IF':
			print('<bb '+str(child.Svalue)+'>')
			# print(child.condition_node.value)
			CFGCOND(child.condition_node)
			print('if(t'+str(tt_value-1)+') goto <bb ' + str(child.Evalue1) + '>')
			print('else goto <bb '+str(child.Evalue2)+'>\n')
			CFGPrint(child.child)
			CFGPrint(child.elchild)
		if child.Type == 'WHILE':
			print('<bb '+str(child.Svalue)+'>')
			CFGCOND(child.condition_node)
			print('if(t'+str(tt_value-1)+') goto <bb ' + str(child.Evalue1) + '>')
			print('else goto <bb '+str(child.Evalue2)+'>\n')
			CFGPrint(child.child)

	return bb_value
