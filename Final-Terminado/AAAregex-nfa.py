'''
Conversion de Expresion Regular a un NFA
Ricardo Leguizamon - Diego Seo, Compiladores 2022
'''

import json #trabajamos con archivos.json de entrada y salida
import sys #interectuamos con el interprete para leer el archivo de entrada desde la terminal directamente


'''
los no simbolos son los identificadores para armar los patrones en 
la definicion regular 
'''
non_symbols = ['+', '*', '.', '(', ')'] #no pudimos agregar el | 
afn = {} #pila para guardar los estados del AFN

class charType:
    SYMBOL = 1
    CONCAT = 2
    UNION  = 3
    KLEENE = 4

'''
Clase Estado_AFN
Clase donde definimos estado del AFN, 
'''
class Estado_AFN: 
    def __init__(self):
        self.next_state = {}

'''
Convertimos la expresion regular a un arbol de expansion
es necesario hacer este paso 
'''
class ExpressionTree: 

    def __init__(self, charType, value=None):
        self.charType = charType
        self.value = value
        self.left = None
        self.right = None
    
'''
Aca utilizamos la construccion de thompson 
regexp es nuestro regex en postfix, aca construimos el NFA- ϵ #3b5 unicode 
'''
def exp_tree(regexp):
    stack = []
    for c in regexp:
        if c == "+":
            z = ExpressionTree(charType.UNION)
            z.right = stack.pop()
            z.left = stack.pop()
            stack.append(z)
        elif c == ".":
            z = ExpressionTree(charType.CONCAT)
            z.right = stack.pop()
            z.left = stack.pop()
            stack.append(z)
        elif c == "*":
            z = ExpressionTree(charType.KLEENE)
            z.left = stack.pop() 
            stack.append(z)
        elif c == "(" or c == ")":
            continue  
        else:
            #print("probar |")
            stack.append(ExpressionTree(charType.SYMBOL, c))
    return stack[0]


def compPrecedence(a, b):
    p = ["+", ".", "*"]
    return p.index(a) > p.index(b)

'''
en esta funcion compute_regex sacamos nuestro regex teniendo de forma postfija

'''
def compute_regex(exp_t):
    
    if exp_t.charType == charType.CONCAT:
        return do_concat(exp_t)
    elif exp_t.charType == charType.UNION:
        return do_union(exp_t)
    elif exp_t.charType == charType.KLEENE:
        return do_kleene_star(exp_t)
    else:
        return eval_symbol(exp_t)

'''
def starNFA(NFA):
    s = ['Q0']
    for i in range(len(NFA['estados'])):
        effective_state = 'Q'+str(i+1)
        s.append(effective_state)
    
    index = 1+len(NFA['estados'])
    only_final_state = 'Q'+str(index)
    s.append(only_final_state)

    l = [ letter for letter in NFA['simbolos'] ]
    ss = ['Q0']
    fs = [only_final_state]

    tm = []
    for arc in NFA['matriz_transicion']:
        [os, il, ns] = arc
        n_os = 'Q'+ str(1+int(os[1:]))
        n_ns = 'Q'+ str(1+int(ns[1:]))
        tm.append([n_os, il, n_ns ])
    
    for st_state in NFA['estado_inicial']:
        tm.append(['Q0','$','Q'+ str(1+int(st_state[1:]))])
    tm.append(['Q0','$',only_final_state])

    for fn_state in NFA['estado_final']:
        tm.append(['Q'+ str(1+int(fn_state[1:])),'$',only_final_state])
        for st_state in NFA['estado_inicial']:
            tm.append(['Q'+ str(1+int(fn_state[1:])),'$','Q'+ str(1+int(st_state[1:]))])
    
    return objectNFA(s, l, tm, ss, fs) #simbols, letters, start, final

'''
def eval_symbol(exp_t):
    start = Estado_AFN()
    end = Estado_AFN()
    
    start.next_state[exp_t.value] = [end]
    return start, end


def do_concat(exp_t):
    left_nfa  = compute_regex(exp_t.left)
    right_nfa = compute_regex(exp_t.right)

    left_nfa[1].next_state['$'] = [right_nfa[0]]
    return left_nfa[0], right_nfa[1]


def do_union(exp_t):
    start = Estado_AFN()
    end = Estado_AFN()

    first_nfa = compute_regex(exp_t.left)
    second_nfa = compute_regex(exp_t.right)

    start.next_state['$'] = [first_nfa[0], second_nfa[0]]
    first_nfa[1].next_state['$'] = [end]
    second_nfa[1].next_state['$'] = [end]

    return start, end


def do_kleene_star(exp_t):
    start = Estado_AFN()
    end = Estado_AFN()

    starred_nfa = compute_regex(exp_t.left)

    start.next_state['$'] = [starred_nfa[0], end]
    starred_nfa[1].next_state['$'] = [starred_nfa[0], end]

    return start, end


def transiciones_m(state, states_done, symbol_table):
    global afn

    if state in states_done:
        return

    states_done.append(state)

    for symbol in list(state.next_state):
        if symbol not in afn['simbolos']:
            afn['simbolos'].append(symbol)
        for ns in state.next_state[symbol]:
            if ns not in symbol_table:
                symbol_table[ns] = sorted(symbol_table.values())[-1] + 1
                q_actual = "Q" + str(symbol_table[ns])
                afn['estados'].append(q_actual)
            afn['transiciones'].append(["Q" + str(symbol_table[state]), symbol, "Q" + str(symbol_table[ns])])

        for ns in state.next_state[symbol]:
            transiciones_m(ns, states_done, symbol_table)

def a_num(str):
    return int(str[1:])


def final_st_dfs():
    global afn
    for st in afn["estados"]:
        count = 0
        for val in afn['transiciones']:
            if val[0] == st and val[2] != st:
                count += 1
        if count == 0 and st not in afn["estado_final"]:
            afn["estado_final"].append(st)


def arrange_nfa(fa):
    global afn
    afn['estados'] = []
    afn['simbolos'] = []
    afn['transiciones'] = []
    afn['estado_inicial'] = []
    afn['estado_final'] = []
    q_1 = "Q" + str(1)
    afn['estados'].append(q_1)
    transiciones_m(fa[0], [], {fa[0] : 1})
    
    st_num = [a_num(i) for i in afn['estados']]

    afn["estado_inicial"].append("Q1")

    final_st_dfs()


def add_concat(regex):
    global non_symbols
    l = len(regex)
    res = []
    for i in range(l - 1):
        res.append(regex[i])
        if regex[i] not in non_symbols:
            if regex[i + 1] not in non_symbols or regex[i + 1] == '(':
                res += '.'
        if regex[i] == ')' and regex[i + 1] == '(':
            res += '.'
        if regex[i] == '*' and regex[i + 1] == '(':
            res += '.'
        if regex[i] == '*' and regex[i + 1] not in non_symbols:
            res += '.'
        if regex[i] == ')' and regex[i + 1] not in non_symbols:
            res += '.'

    res += regex[l - 1]
    return res

'''
infijo a posfijo
stk es una pila que almacena de forma infija 
orden que se toma:  . () * . +
'''
def inf_pos(regexp):
    stk = []
    res = ""

    for c in regexp:
        if c not in non_symbols or c == "*":
            res += c
        elif c == ")":
            while len(stk) > 0 and stk[-1] != "(":
                res += stk.pop()
            stk.pop()
        elif c == "(":
            stk.append(c)
        elif len(stk) == 0 or stk[-1] == "(" or compPrecedence(c, stk[-1]):
            stk.append(c)
        else:
            while len(stk) > 0 and stk[-1] != "(" and not compPrecedence(c, stk[-1]):
                res += stk.pop()
            stk.append(c)

    while len(stk) > 0:
        res += stk.pop()

    return res
'''
polish_regex
retornamos de forma infija el regex 
'''
def polish_regex(regex):
    reg = add_concat(regex)
    regg = inf_pos(reg)
    #print(regg)
    return regg

'''
estas dos definiciones son para el input y output 
del json 
'''
def load_regex():
    with open(sys.argv[1], 'r') as inpjson:
        regex = json.loads(inpjson.read())
    return regex

def output_nfa():
    global afn
    with open(sys.argv[2], 'w') as outjson: 
        outjson.write(json.dumps(afn, indent = 4))

if __name__ == "__main__":
    r = load_regex()
    reg = r['regex']
    pr = polish_regex(reg)
    et = exp_tree(pr)
    fa = compute_regex(et)
    arrange_nfa(fa)
    output_nfa()
