# Brian Schwartz
# Bjs9yv
# CS4710 HW1

import re

roots = {}
learned = {}
rules = {}
facts = []

def parse_expression(expr):
    expression = expr
    variables = sorted(re.split('&|\||!|\(|\)',expr), key=len, reverse=True) # sort decending by len avoids issues
    while '' in variables: variables.remove('')
    for v in variables:
        if v in roots:
            if roots[v][0] == True:
                expression = expression.replace(v,'$') # replace True/False with safe characters avoids issues
            else:
                expression = expression.replace(v,'%')
        elif v in learned:
            if learned[v][0] == True:
                expression = expression.replace(v,'$')
            else:
                expression = expression.replace(v,'%')
        else:
            print('one or more undeclared variables')
            return
    expression = expression.replace('!', ' not ')
    expression = expression.replace('&', ' and ')
    expression = expression.replace('|', ' or ')
    expression = expression.replace('$', 'True')
    expression = expression.replace('%', 'False')
    truth_value = eval(expression) # eval() does all the heavy lifting involving boolean logic
    return truth_value

def Learn():
    for expr in rules:
        truth_value = parse_expression(expr)
        var = rules[expr]
        if truth_value == True and learned[var][2] == False:
            learned[var][2] = expr # store the rule that led to this assignment
            learned[var][0] = truth_value # learn something about this variable
            facts.append(var) # add it to facts
            Learn() # run Learn again in case we can learn something new

def List():
    """ Lists out all of the facts and rules currently known by the system """
    print('Root Variables:')
    for var in roots:
        print('\t%s = "%s"' %(var,roots[var][1]))
    print('\nLearned Variables:')
    for var in learned:
        print('\t%s = "%s"' %(var,learned[var][1]))
    print('\nFacts:')
    for fact in facts:
        print('\t%s' %(fact))
    print('\nRules:')
    for rule in rules:
        print('\t%s -> %s' % (rule,rules[rule]))

def Query(expr): 
    # Syntax: Query <EXP>
    print(parse_expression(expr))


def Why(expr): 
    # Syntax: Why <EXP>
    variables = sorted(re.split('&|\||!|\(|\)',expr), key=len, reverse=True)
    while '' in variables: variables.remove('')
    result = parse_expression(expr)
    print(result)
    for var in variables:
        if var in roots:
            if roots[var][0] == True:
                print('I KNOW THAT %s' %(roots[var][1]))
            else:
                print('I KNOW IT IS NOT TRUE THAT %s' %(roots[var][1]))
        else:
            rule = learned[var][2] # if False then no rule led to the truth this variable has
            if rule == False:
                print('I KNOW IT IS NOT TRUE THAT %s' %(learned[var][1])) 
            else:
                args = sorted(re.split('&|\||!|\(|\)', learned[var][2]), key=len, reverse=True)
                while '' in args: args.remove('')
                for arg in args:
                    if arg in roots:
                        statement2 = learned[var][1]
                        if parse_expression(learned[var][2]) == True:
                            print('BECAUSE %s I KNOW THAT %s' %(roots[arg][1], statement2))
                        else:
                            print('BECAUSE It IS NOT TRUE THAT %s I CANNOT PROVE %s' %(roots[arg][1], statement2))
                    else:
                        if eval(learned[var][2]) == True:
                            print('BECAUSE %s I KNOW THAT %s' %(learned[arg][1], statement2))
                        else: 
                            print('BECAUSE IT IS NOT TRUE THAT %s I CANNOT PROVE %s' %(learned[arg][1], statement2))
    expression = expr
    expr_lookup = [] # avoids replace() issues
    for v in variables:
        if v in roots:
            expression = expression.replace(v,str(len(expr_lookup)))
            expr_lookup.append(roots[v][1])
        else:
            expression = expression.replace(v,str(len(expr_lookup)))
            expr_lookup.append(learned[v][1])
    for e in reversed(range(len(expr_lookup))):
        expression = expression.replace(str(e),expr_lookup[int(e)])
    expression = expression.replace('!',' NOT ')
    expression = expression.replace('&', ' AND ')
    expression = expression.replace('|', ' OR ')
    if result == True: 
        print('THUS I KNOW THAT %s' %(expression))
    else:
        print('THUS I CANNOT PROVE THAT %s' %(expression))

    
def Teach(cmd):
    """ Three ways to use this command """
    # Syntax: Teach <ARG> <VAR> = <STRING> , takes -R and -L
    # variable names cant be used twice
    # varaible names can have letters and _ 
    # A root variable is a direct observation that can only be set to true directly by the user
    # A learned variable cannot be set true directly, but must be inferred via inference rules
    if '-R ' in cmd:
        cmd = cmd.split('-R ')[1]
        var, value = cmd.split(' = ')
        roots[var] = [False,value.replace('"', '').strip(),False] # [Truth value, statement value, learned before]
        roots[var][2] = True # keep track of if root has been set before, if this changes reset all learned vars
    elif '-L ' in cmd:
        cmd = cmd.split('-L ')[1]
        var, value = cmd.split(' = ')
        learned[var] = [False,value.replace('"', '').strip(),False] # [Truth value, statement value, expr/False]
        
   # Syntax: Teach <ROOT VAR> = <BOOL>
   # sets a root variable to be True or False
   # can only be used on root variables
    elif '=' in cmd:
        var, truth_value = cmd.split(' = ')
        if roots.get(var):
            if roots[var][2] == True:
                for v in learned:
                    learned[v][0] = False
                    learned[v][2] = False
                    if v in facts:
                        facts.remove(v)
                if truth_value == 'false':
                    if var in facts:
                        facts.remove(var)
            if truth_value == 'true':
                truth_value = True
            else:
                truth_value = False
            roots[var][0] = truth_value
            if truth_value == True:
                facts.append(var)
        else:
            print("Only root variables can be set directly")
    
    # Syntax: Teach <EXP> -> <VAR>
    # entire expressions are allowed, with parenthesis
    # order of operations: !, &, |
    # if any variable in the expression is not defined ignore entire expression
    # <VAR> must be a root variable
    elif '->' in cmd:
        expr, var = cmd.split(' -> ')
        if var not in learned:
            print("value after -> must be a Learned Variable")
        else:
            if parse_expression(expr) is not None:
                rules[expr] = var

    else:
        print('Syntax error in Teach command')

def read(command):
    if command == 'Learn':
        Learn()
    elif command == 'List':
        List()
    else:
        prefix, cmd = command.split(' ', 1)
        if prefix == 'Query':
            Query(cmd)
        elif prefix == 'Why':
            Why(cmd)
        elif prefix == 'Teach':
            Teach(cmd)
        else:
            print('bad input (1)')

while True:
    command = input('Enter a command: ') 
    read(command)

