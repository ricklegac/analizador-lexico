'''
Conversion de NFA a un DFA
Ricardo Leguizamon - Diego Seo, Compiladores 2022
'''
import json
import sys

dfa = {}
nfa = {}
nfa_states = []
dfa_states = []

def cerradura_ps(nfa_st):
    stack_ps = [[]]
    for i in nfa_st:
        for sub in stack_ps:
            stack_ps = stack_ps + [list(sub) + [i]]
    return stack_ps

def load_nfa():
    global nfa
    with open(sys.argv[1], 'r') as inpjson:
        nfa = json.loads(inpjson.read())

def out_dfa():
    global dfa
    with open(sys.argv[2], 'w') as outjson:
        outjson.write(json.dumps(dfa, indent = 4))

if __name__ == "__main__":
    load_nfa()
    #estado inicial del dfa antes de convertir
    dfa['estados'] = []
    dfa['simbolos'] = nfa['simbolos']
    dfa['transiciones'] = []
    
    for state in nfa['estados']:
        nfa_states.append(state)
    #power set, 
    dfa_states = cerradura_ps(nfa_states)


    dfa['estados'] = []
    for estados in dfa_states:
        temp = []
        for state in estados:
            temp.append(state)
        dfa['estados'].append(temp)

    for estados in dfa_states:
        for letter in nfa['simbolos']:
            q_to = []
            for state in estados:
                for val in nfa['transiciones']:
                    start = val[0]
                    inp = val[1]
                    end = val[2]
                    if state == start and letter == inp:
                        if end not in q_to:
                            q_to.append(end)
            q_states = []
            for i in estados:
                q_states.append(i)
            dfa['transiciones'].append([q_states, letter, q_to])

    dfa['estado_inicial'] = []
    for state in nfa['estado_inicial']:
        dfa['estado_inicial'].append([state])
    dfa['estado_final'] = []
    for estados in dfa['estados']:
        for state in estados:
            if state in nfa['estado_final'] and estados not in dfa['estado_final']:
                dfa['estado_final'].append(estados)
    
    out_dfa()


