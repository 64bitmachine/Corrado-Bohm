#!/usr/bin/python3

import sys
import ply.lex as lex
import ply.yacc as yacc
import util

# counts for static,pointer and assignemnt statements
count_static=0
count_pointer=0
count_assign=0

ifelsecounter=0

node_list = []
nest_node_list = []
cond_list = []
cond_list2 = []

check_ = 1
count_bb=1

tokens = (
		'NAME',
		# 'MAIN',
		'NUMBER',
		'RETURN',
		'FLOAT',
		'INT',
		# 'NEWLINE',
		'VOID',
		'COMMA',
		'PLUS',
		'MINUS',
		'DIVIDE',
		'SEMICOLON',
		'PERCENTAGE',
		'LPAREN',
		'RPAREN',
		'EQUALS',
		'LTHAN',
		'GTHAN',
		'LBRACE',
		'RBRACE',
		# 'UMINUS',
		'EXCLAIM',
		'ORLINE',
		'IF',
		# 'IFX',
		'ELSE',
		'WHILE',
		# 'LBRACKET',
		# 'RBRACKET',
		'ASTERISK',
		'AMPERSAND',
)

# allotted_words = {
# 	'name' : 'NAME',
# 	'number' : 'NUMBER',
# 	'int' : 'INT',
# 	'void' : 'VOID'
# }

t_ASTERISK = r'\*'
t_NUMBER = r'[0-9]+'
t_AMPERSAND = r'&'
t_LTHAN = r'<'
t_EXCLAIM = r'!'
t_GTHAN = r'>'
# t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_COMMA = r','
t_ORLINE = r'\|'
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_PERCENTAGE = r'%'
# t_LBRACKET = r'\['
# t_RBRACKET = r'\]'

lineno = 1


def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if (t.value == 'if'):
		t.type = 'IF'
	if (t.value == 'else'):
		t.type = 'ELSE'
	if (t.value == 'while'):
		t.type = 'WHILE'
	# if (t.value == 'main'):
	# 	t.type = 'MAIN'
	if (t.value == 'void'):
		t.type = 'VOID'
	if (t.value == 'int'):
		t.type = 'INT'
	if (t.value == 'float'):
		t.type = 'FLOAT'
	return t

# def t_IF(t):
# 	r'if | IF'
# 	t.value = 'if'
# 	return t

# def t_ELSE(t):
# 	r'else | ELSE'
# 	t.value = 'else'
# 	return t

# def t_WHILE(t):
# 	r'while | WHILE'
# 	t.value = 'while'
# 	return t

def t_NEWLINE(t):
	r'\n'
	global lineno
	lineno+=1
#    return t

t_ignore = " \t"

# def t_MAIN(t):
# 	r'MAIN | main'
# 	t.value = 'main'
# 	return t

# def t_VOID(t):
# 	r'VOID | void'
# 	t.value = 'void'
# 	return t

# def t_INT(t):
# 	r'INT | int'
# 	t.value = 'int'
# 	return t

def t_error(t):
	print("Line %d." % (t.lineno,) + "")
	if t.value[0] == '"':
		print("Unterminated string literal.")
		if t.value.count('\n') > 0:
			t.skip(t.value.index('\n'))
	elif t.value[0:2] == '/*':
		print("Unterminated comment.")
	else:
		print("Illegal character '%s'" % t.value[0])
		t.skip(1)

precedence = (
		('left','PLUS','MINUS'),
		('left','ASTERISK','DIVIDE'),
		('right', 'UMINUS'),
		('nonassoc','IFX'),
		('nonassoc','ELSE'),   
)

def p_cprog(p):
	'''
	cprog : sprog
	'''
	global nest_node_list
	# print nest_node_list
	for node in list(reversed(nest_node_list)):
		node.printTree(0)
		print ("")

def p_sprog(p):
	'''
	sprog : type NAME arguments main_body
			| type NAME arguments main_body sprog
	'''
	# global node_list, nest_node_list
	# global count_bb
	# temp=0
	# print p[2]
	# print p[4]
	rev_node_list = list(reversed(p[4]))
	Node = util.Node()
	Node.value = p[2]
	for child in rev_node_list:
		Node.addChild(child)
	nest_node_list.append(Node)
	# print "jennie is in sprog"
	# for node in rev_node_list:
		# node.printTree(0)
		# count_bb = util.retriveexpr(node,count_bb)
		# print ""
	# print 'value of count bb ',count_bb
	# global check_
	# print "check value is ",check_
	
	# endval = util.CFGPrint(util.printCFG(util.CFGTree(rev_node_list)))

	# print '<bb '+str(endval)+'>'
	# print 'End'

def p_arguments(p):
	'''
	arguments : LPAREN params RPAREN
			  | LPAREN RPAREN
	'''
	# print "jennie is in arguments"

def p_params(p):
	'''
	params : type var COMMA params
			| type var1 COMMA params
			| type var
			| type var1
	'''
	# print "jennie is in params"


def p_main_body(p):
	'''
	main_body : LBRACE stmt_list RBRACE
	'''
	global node_list
	p[0] = node_list
	# print node_list
	node_list=[]
	# print "jennie is in main_body"

def p_stmt_list(p):
	'''
	stmt_list : stmt stmt_list
			  | stmt
	'''
	global check_
	global node_list
	global cond_list
	if (check_ != 1 and p[1]):
		# print check_,len(cond_list)
		cond_list[check_-2][0].append(p[1])
		p[0]=p[1]
	elif (p[1]):
		node_list.append(p[1])
		p[0]=p[1]
	# if(p[1]):
	# 	p[1].printTree(0)
	# print "jennie is in stmt_list",p[1],check_

def p_decl_stmt(p):
	'''
	stmt : type varlist SEMICOLON
	'''
	# print "jennie in decl_stmt"

# assignlist -> assign comma assignlist semicolon | assign semicolon
# assign -> starname equals number | starname equals starname | name equals name | name equals andname

def p_stmt(p):
	'''
	stmt : assignlist SEMICOLON
	'''
	p[0]=p[1]
	# print "jennie is in stmt",p[1]

def p_select_stmt(p):
	'''
	stmt : selection_stmt
	'''
	# global node_list
	# global cond_list
	# global check_
	# if (len(cond_list) <= check_-2):
	# 	cond_list.append(([p[1]],0))
	# else:
	# 	print len(cond_list), check_
	# 	cond_list[check_-2][0].append(p[1])
	p[0]=p[1]
	# print "jennie is in select_stmt"

def p_iterate_stmt(p):
	''' 
	stmt : iteration_stmt 
	'''
	# global node_list
	# global cond_list
	# global check_
	# if (len(cond_list) <= check_-2):
	# 	cond_list.append(([p[1]],0))
	# elif (check_ != 1):
	# 	print len(cond_list), check_
	# 	cond_list[check_-2][0].append(p[1])
	p[0]=p[1]
	# print "jennie is in iteration_stmt"
	
def p_assignlist(p):
	'''
	assignlist : assignstmt COMMA assignlist 
				| assignstmt
	'''
	p[0]=p[1]
	# print "jennie is in assignlist"

def p_assignstmt(p):
	'''
	assignstmt : rec_starname EQUALS expression
				| name EQUALS expression
	'''
	# print "jennie is in assignstmt"
	node = util.Node()
	node.value = "ASGN"
	node.addChild(p[1])
	node.addChild(p[3])
	global count_assign
	count_assign+=1
	# global node_list
	# global cond_list
	# global check_
	# if (check_ == 1):
	# 	node_list.append(node)
	# elif (len(cond_list) <= check_-2):
	# 	cond_list.append(([node],0))
	# else:
	# 	print len(cond_list), check_
	# 	cond_list[check_-2][0].append(node)
	p[0]=node

def p_rec_starname(p):
	'''
	rec_starname : ASTERISK rec_starname
	'''
	# print "jennie is in rec_starname"
	node = util.Node()
	node.value = "DEREF"
	node.addChild(p[2])
	p[0]=node

def p_rec_starname1(p):
	'''
	rec_starname : starname
	'''
	# print "jennie is in p_rec_starname1"
	p[0]=p[1]

def p_expression(p):
	'''
	expression : expression PLUS expression
				| expression MINUS expression
				| expression DIVIDE expression
				| expression ASTERISK expression
				| expression PERCENTAGE expression
	'''
	# print "jennie is in expression"
	node = util.Node()
	if p[2] == '*':
		node.value = "MUL"
		node.addChild(p[1])
		node.addChild(p[3])
	if p[2] == '+':
		node.value = "PLUS"
		node.addChild(p[1])
		node.addChild(p[3])
	if p[2] == '/':
		node.value = "DIV"
		node.addChild(p[1])
		node.addChild(p[3])
	if p[2] == '-':
		node.value = "MINUS"
		node.addChild(p[1])
		node.addChild(p[3])
	p[0]=node


def p_term_expression(p):
	'''
	expression : starname
				| andname
				| name
				| number
	'''
	# print "jennie is in p_term_expression"
	p[0]=p[1]

def p_paren_expression(p):
	'''
	expression : LPAREN expression RPAREN
	'''
	# print "jennie is in p_paren_expression"
	p[0]=p[2]

def p_type(p):
	'''
	type : INT
		  | VOID
		  | FLOAT
	'''
	# print "jennie is in p_type"

def p_starname(p):
	'''
	starname : ASTERISK name
	'''
	# print "jennie is in starname"
	node = util.Node()
	node.value = "DEREF"
	node.addChild(p[2])
	p[0] = node

def p_andname(p):
	'''
	andname : AMPERSAND name
	'''
	# print "jennie is in andname"
	node = util.Node()
	node.value = "ADDR"
	node.addChild(p[2])
	p[0] = node

def p_num(p):
	'''
	number : NUMBER
	'''
	# print "jennie is in num"
	node = util.Node()
	node.value = "CONST("+str(p[1])+")"
	p[0]=node
 
def p_name(p):
	'''
	name : NAME
	'''
	# print "jennie is in name"
	node = util.Node()
	node.value = "VAR("+p[1]+")"
	p[0]=node

# varlist-> var COMMA varlist | var
# var -> name | starname

def p_var(p):
	'''
	var : NAME
	'''
	# print "jennie is in p_var"
	global count_static
	count_static+=1

def p_var1(p):
	'''
	var1 : starname
	'''
	# print "jennie is in var1"
	global count_pointer
	count_pointer+=1

def p_var2(p):
	'''
	var1 : ASTERISK var1
	'''
	# print "jennie is in p_var2"

def p_varlist(p):
	'''
	varlist : var COMMA varlist
			| var1 COMMA varlist
			| var
			| var1
	'''
	# print "jennie is in varlist"

def p_uminus(p):
	'''
	expression : MINUS expression %prec UMINUS
	'''
	# print "jennie is in uminus"
	node = util.Node()
	node.value = "UMINUS"
	node.addChild(p[2])
	p[0] = node

# selection-stmt -> if lparen cond_expr rparen stmt ;
# cond_expr -> logical-or-expr
# logical-or-expr -> logical-and-expr | logical-or || logical-and
# logical-and-expr -> inclusive-or | logical-and && inclusive-or


def p_iteration_stmt1(p):
	'''
	iteration_stmt : WHILE LPAREN condition_expression RPAREN brace_stmt
	'''
	# print "jennie is in iteration_stmt1"
	node = util.Node()
	node.value = "WHILE"
	node.addChild(p[3])
	# node.addChild(p[5])
	global cond_list
	global check_
	for x in list(reversed(cond_list[check_-2][0])):
		node.addChild(x)
	del cond_list[check_-2]
	check_ = check_ - 1
	# if (check_ == 1):
	# 	node_list.append(node)
	p[0]=node

def p_brace_stmt(p):
	'''
	brace_stmt : stmt
	'''
	global check_, ifelsecounter
	global cond_list
	if (check_ != 1):
		# if(not ifelsecounter):
		# 	ifelsecounter+=1
		cond_list[check_-2][0].append(p[1])
	cond_list[check_-2][1].append(len(cond_list[check_-2][0]))
	# print "jennie is in brace_stmt", "check_->",check_
	p[0]=p[1]

def p_brace_stmt1(p):
	'''
	brace_stmt : LBRACE stmt_list RBRACE
	'''
	global cond_list, ifelsecounter, check_
	# print "jennie is in p_brace_stmt1",p[2], "check_->",check_
	if (not ifelsecounter):
		ifelsecounter =  len(cond_list[check_-2][0])
	# print cond_list[check_-2][1]
	# MI = list(cond_list[check_-2])
	# MI[1]=len(cond_list[check_-2][0])
	cond_list[check_-2][1].append(len(cond_list[check_-2][0]))
	# print "testing ",ifelsecounter
	p[0]=p[2]

def p_selection_stmt(p):
	'''
	selection_stmt : IF LPAREN condition_expression RPAREN brace_stmt %prec IFX
	'''
	node = util.Node()
	node.value = "IF"
	node.addChild(p[3])
	global cond_list,ifelsecounter
	ifelsecounter = 0
	global check_
	for x in list(reversed(cond_list[check_-2][0])):
		node.addChild(x)
	del cond_list[check_-2]
	check_ = check_ - 1
	# if (check_ == 1):
	# 	node_list.append(node)
	p[0]=node
	# print "jennie is in selection_stmt",p[3]

def p_selection_stmt1(p):
	'''
	selection_stmt : IF LPAREN condition_expression RPAREN brace_stmt ELSE brace_stmt
	'''
	node = util.Node()
	node.value = "IF"
	node.addChild(p[3])
	# node.addChild(p[5])
	# node.addChild(p[7])
	# global cond_list
	global cond_list
	global check_, ifelsecounter
	# print "length ",len(cond_list[check_-2][0])
	# print cond_list[check_-2][1]
	if (len(cond_list[check_-2][1])):
		node.elsepart = cond_list[check_-2][1][0]+1
	else:
		node.elsepart = 1
	# print "elsepart ", cond_list[check_-2][1]
	# print 
	ifpart = cond_list[check_-2][0][0:node.elsepart-1]
	# print "ifpartlist ",ifpart
	elsepart = cond_list[check_-2][0][node.elsepart-1:len(cond_list[check_-2][0])]
	# print "elsepartlist ",elsepart
	ifelsecounter = 0

	for x in reversed(ifpart):
		node.addChild(x)
	for x in reversed(elsepart):
		node.addChild(x)
	del cond_list[check_-2]
	# node.addChild(p[7])
	check_ = check_ - 1
	# for x in cond_list[check_-2][0]:
	# 	node.addChild(x)
	# del cond_list[check_-2]
	# if (check_ == 1):
	# 	node_list.append(node)
	p[0]=node
	# node.printTree(0)
	# print "jennie is in selection_stmt1","check_->",check_

def p_condition_expression(p):
	'''
	condition_expression : assign_expr
	'''
	global check_
	global cond_list
	cond_list.append(([],[]))
	check_ = check_ + 1
	# print "jennie is in condition_expression"
	p[0]=p[1]

def p_assign_expr(p):
	'''
	assign_expr : log_and_expr
	'''
	# print "jennie is in assign_expr"
	p[0]=p[1]

# def p_cond_expr(p):
# 	'''
# 	cond_expr : log_or_expr
# 	'''
# 	# print "jennie is in cond_expr"
# 	p[0]=p[1]

# def p_log_or_expr(p):
# 	'''
# 	log_or_expr : log_and_expr
# 	'''
# 	# print "jennie is in log_or_expr"
# 	p[0]=p[1]

def p_log_and_expr(p):
	'''
	log_and_expr : log_and_expr AMPERSAND AMPERSAND eq_expr
				 | log_and_expr ORLINE ORLINE eq_expr
	'''
	# print "jennie is in logical-and-expr"
	node = util.Node()
	if (p[2] == '&'):
		node.value = 'AND'
	else:
		node.value = 'OR'
	node.addChild(p[1])
	node.addChild(p[4])
	p[0]=node

def p_log_and_expr1(p):
	'''
	log_and_expr : eq_expr
	'''
	# print "jennie is in p_log_and_expr1"
	p[0]=p[1]

# def p_incl_or_expr(p):
# 	'''
# 	incl_or_expr : excl_or_expr
# 	'''
# 	# print "jennie is in incl_or_expr"
# 	p[0] = p[1]

# def p_excl_or_expr(p):
# 	'''
# 	excl_or_expr : and_expr
# 	'''
# 	# print "jennie is in excl_or_expr"
# 	p[0] = p[1]

# def p_and_expr(p):
# 	'''
# 	and_expr : eq_expr
# 	'''
# 	# print "jennie is in and_expr"
# 	p[0]=p[1]

def p_eq_expr(p):
	'''
	eq_expr : rel_expr
	'''
	# print "jennie is in eq_expr"
	p[0]=p[1]

def p_rel_expr(p):
	'''
	rel_expr : rel_expr EXCLAIM EQUALS shift_expr
			 | rel_expr EQUALS EQUALS shift_expr
			 | rel_expr LTHAN EQUALS shift_expr
			 | rel_expr GTHAN EQUALS shift_expr
	'''
	# print "jennie is in rel_expr",p[2]
	node = util.Node()
	if (p[2] == '<'):
		node.value="LE"
	if (p[2] == '!'):
		node.value="NE"
	if (p[2] == '>'):
		node.value="GE"
	if (p[2] == '='):
		node.value="EQ"
	node.addChild(p[1])
	node.addChild(p[4])
	p[0]=node

def p_rel_expr1(p):
	'''
	rel_expr : shift_expr
	'''
	# print "jennie is in p_rel_expr1"
	p[0]=p[1]

def p_rel_expr2(p):
	'''
	rel_expr : rel_expr LTHAN shift_expr
			 | rel_expr GTHAN shift_expr
	'''
	# print "jennie is in p_rel_expr2"
	node = util.Node()
	if (p[2] == '<'):
		node.value = "LT"
	if (p[2] == '>'):
		node.value = "GT"
	node.addChild(p[1])
	node.addChild(p[3])
	# node_list.append(node)
	p[0]=node

def p_shift_expr(p):
	'''
	shift_expr : expression
	'''
	# print "jennie is in shift_expr"
	p[0]=p[1]

# def p_additive_expr(p):
# 	'''
# 	additive_expr : additive_expr PLUS multiplicative_expr
# 				  | additive_expr MINUS multiplicative_expr
# 	'''
# 	# print "jennie is in additive_expr"
# 	node = util.Node()
# 	if (p[2]=='+'):
# 		node.value = "PLUS"
# 	if (p[2]=='-'):
# 		node.value = "MINUS"
# 	node.addChild(p[1])
# 	node.addChild(p[3])
# 	# node_list.append(node)
# 	p[0]=node

# def p_additive_expr1(p):
# 	'''
# 	additive_expr : multiplicative_expr
# 	'''
# 	# print "jennie is in p_additive_expr1"
# 	p[0]=p[1]

# def p_multiplicative_expr(p):
# 	'''
# 	multiplicative_expr : cast_expr
# 	'''
# 	# print "jennie is in multiplicative_expr"
# 	p[0]=p[1]

# def p_cast_expr(p):
# 	'''
# 	cast_expr : expression
# 	'''
# 	# print "jennie is in cast_expr"
# 	p[0]=p[1]

# http://www.lysator.liu.se/c/ANSI-C-grammar-y.html

def p_error(t):
	# print "You've got a syntax error somewhere in your code."
	# print "It could be around line %d." % t.lineno
	# print "Good luck finding it."
	# raise ParseError()
	if t:
		print("syntax error at lineno {1} at {0}".format(t.value,lineno))
	else:
		print("syntax error at EOF")

def call_lex():
	file = open(sys.argv[1])
	lines = file.readlines()
	file.close()
	strings = ""
	for i in lines:
		strings += i
	lex.input(strings)
	# while 1:
	#     token = lex.token()       # Get a token
	#     if not token: break        # No more tokens
	#     print "(%s,'%s',%d, %d)" % (token.type, token.value, token.lineno, token.lexpos)
	yacc.yacc()
	yacc.parse(strings)
	global count_assign
	global count_pointer
	global count_static
#    print count_static
#    print count_pointer
#    print count_assign


lex.lex()

if __name__ == '__main__':
	call_lex()