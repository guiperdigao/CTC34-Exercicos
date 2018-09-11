from graphviz import Digraph

class Automata():
    def __init__(self,expr):
        expression = ''.join(expr)
        self.start = 0
        self.final = 1
        self.new = 2
        self.nfa = {0:{expression:1}}
        self.graph = Digraph(comment='E-AFN')
    
    def union(self,r1,r2):
        trans1 = ''.join(r1)
        trans2 = ''.join(r2)
        orig = trans1+'+'+trans2
        orig2 = '('+orig+')'
        for origem, c in self.nfa.items():
            for transicao,destino in self.nfa[origem].items():
                if transicao == orig or transicao == orig2:
                    aux_o = origem
                    aux_d = destino
                    aux_t = transicao
        del self.nfa[aux_o][aux_t]
        self.nfa[aux_o][trans1] = aux_d
        self.nfa[aux_o][trans2] = aux_d
                    
    
    def concat(self,r1,r2):
        trans1 = ''.join(r1)
        trans2 = ''.join(r2)
        n = len(trans2)
        orig1 = trans1+trans2
        if '+' in trans2 and n<=6:
            trans2 = '('+trans2+')'
        orig = trans1+trans2
        for origem,c  in self.nfa.items():
            for transicao,destino in self.nfa[origem].items():
                if transicao == orig or transicao == orig1:
                    aux_o = origem
                    aux_d = destino
                    aux_t = transicao
        del self.nfa[aux_o][aux_t]
        self.nfa[aux_o][trans1] = self.new
        if self.new not in self.nfa.keys():
            self.nfa[self.new] = {trans2:aux_d}
        else: self.nfa[self.new][trans2] = aux_d
        self.new = self.new+1
    
    def kleene(self,r1):
        trans = ''.join(r1)
        alt = '('+trans+')*'
        alt2 = '('+alt+')'
        for origem,c  in self.nfa.items():
            for transicao,destino in self.nfa[origem].items():
                if transicao == trans or transicao == alt or transicao == alt2:
                    aux_o = origem
                    aux_d = destino
                    aux_t = transicao
        n = len(aux_t)
        del self.nfa[aux_o][aux_t]
        if n == 2:
            aux_t = aux_t[0:1]
        else: aux_t = aux_t[1:n-2] 
        if '&' in self.nfa[aux_o].keys():
            self.nfa[aux_o]['e'] = self.new
        else:
            self.nfa[aux_o]['&'] = self.new
        if self.new not in self.nfa.keys():
            self.nfa[self.new] = {'&':aux_d}
        else: self.nfa[self.new]['&'] = aux_d
        self.nfa[self.new][aux_t] = self.new
        self.new = self.new+1
    
    def generateFormat(self):
        for origem, caminho in self.nfa.items():
            self.graph.node(str(origem),str(origem), shape='circle')
        self.graph.node('1','1', shape='doublecircle')
        for origem, caminho in self.nfa.items():
            for transicao,destino in self.nfa[origem].items():
                if transicao == 'e':
                    self.graph.edge(str(origem),str(destino), label = '&')
                else: self.graph.edge(str(origem),str(destino), label = transicao)

def recursao(expr):
    r1 = []
    r2 = []
    previous = '&'
    testa = 1
    n = len(expr)
    if n <= 2:
        if n == 2:
            afn.kleene(expr)
        return 0
    count = 0
    for i in range(0,n-1):
        if expr[i] == '(':
            count = count + 1
        elif expr[i] == ')':
            count = count - 1
        elif expr[i] == '+' and count == 0:
            r1 = expr[0:i]
            r2 = expr[i+1:n]
            testa = 0
            afn.union(r1,r2)
            recursao(r1)
            recursao(r2)
    count = 0
    for i in range(0,n):
        if expr[i] == '*':
            count = count +1
    if expr[0] == '(' and expr[n-1] == '*' and expr[n-2] == ')'and count == 1:
        #fecho de kleene
        r1 = expr[1:n-2]
        testa = 0
        afn.kleene(r1)
        recursao(r1)
    count = 0
    for i in range(0,n-1):
        if testa == 1:
            if expr[i].isalpha():
                if (previous == '*' or previous.isalpha()) and count == 0:
                    r1 = expr[0:i]
                    r2 = expr[i:n]
                    afn.concat(r1,r2)
                    recursao(r1)
                    recursao(r2)
                    testa = 0
            elif expr[i] == '(':
                if previous != '&':
                    r1 = expr[0:i]
                    if expr[n-1] == '*':
                        r2 = expr[i:n]
                    elif expr[n-1] == ')':
                        r2 = expr[i+1:n-1]
                    afn.concat(r1,r2)
                    recursao(r1)
                    recursao(r2)
                    testa = 0
                count = count + 1
            elif expr[i] == ')':
                count = count - 1
                if count == 0:
                    if expr[i+1] == '*':
                        """ fecho de kleene"""
                        r1 = expr[0:i+2]
                        if i != n-2:
                            r2 = expr[i+2:n]
                        if i != n-2:
                            afn.concat(r1,r2)
                            recursao(r1)
                            recursao(r2)
                        else:
                            recursao(r1)
                        testa = 0
                    else:
                        r1 = expr[1:i]
                        recursao(r1)
                        testa = 0
            elif expr[i] == '*':
                if count == 0:
                    r1 = expr[0:i+1]
                    r2 = expr[i+1:n]
                    afn.concat(r1,r2)
                    recursao(r1)
                    recursao(r2)
                    testa = 0
            previous = expr[i]
                
regex = input("Digite expressao regular:")
count = 0
L = []
for i in regex:
    L.append(i)

afn = Automata(L)
recursao(L)    
print(afn.nfa)
afn.generateFormat()
print(afn.graph.source)

## Questao 3:
def encontraSubs(entrada,cadeia):
    #if type(entrada) == str:
    #    L = []
    #    regex = entrada
    #    for i in regex:
    #        L.append(i)
    #    recursao(L)
    #else: afn.nfa = entrada
    CAD = []
    for i in cadeia:
        CAD.append(i) 
    n = len(CAD)
    ## Colocar nfa:
    familia1 = (afn.nfa,'(a+b)*bb(b+a)*')
    familia2 = (afn.nfa,'(a(b+c))*')
    familia3 = (afn.nfa,'a*b+b*a')
    familia4 = (afn.nfa,'a*b*c*')
    dfa1 = {0:{'a':0,'b':2},2:{'b':1,'a':0},1:{'a':1,'b':1}}
    dfa1_final = (1)
    dfa2 = {0:{'a':2,'b':-1,'c':-1},2:{'b':0,'c':0,'a':-1},-1:{'a':-1,'b':-1,'c':-1}}
    dfa2_final = (0)
    dfa3 = {0:{'a':14,'b':15},14:{'b':1,'a':24},24:{'a':24,'b':1},15:{'a':1,'b':35},35:{'a':1,'b':35},1:{'a':-1,'b':-1},-1:{'a':-1,'b':-1}}
    dfa3_final = (1,14,15)
    dfa4 = {0:{'a':0,'b':1,'c':2},1:{'a':-1,'b':1,'c':2},2:{'a':-1,'b':-1,'c':2},-1:{'a':-1,'b':-1,'c':-1}}
    dfa4_final = (0,1,2)
    if entrada in familia1:
        dfa = dfa1
        finals = dfa1_final
    elif entrada in familia2:
        dfa = dfa2
        finals = dfa2_final
    elif entrada in familia3:
        dfa = dfa3
        finals = dfa3_final
    elif entrada in familia4:
        dfa = dfa4
        finals = dfa4_final
    lista = []
    subcad = ''
    prev_state = 0
    for i in range(0,n):
        subcad = ''
        prev_state = 0
        for j in range(i,n):
            if dfa[prev_state][CAD[j]] == -1:
                lista.append(subcad)
                subcad = ''
            elif type(finals) == tuple: 
                if dfa[prev_state][CAD[j]] in finals:
                    subcad = subcad + CAD[j]
                    lista.append(subcad)
                    prev_state = dfa[prev_state][CAD[j]]
                else: 
                    subcad = subcad + CAD[j]
                    prev_state = dfa[prev_state][CAD[j]]
            elif type(finals) == int: 
                if dfa[prev_state][CAD[j]] == finals:
                    subcad = subcad + CAD[j]
                    lista.append(subcad)
                    prev_state = dfa[prev_state][CAD[j]]
                else: 
                    subcad = subcad + CAD[j]
                    prev_state = dfa[prev_state][CAD[j]]
    lista = list(set(lista))
    print(lista)


entrada = input("Entrada:")
cadeia = input("Cadeia principal:")
encontraSubs(entrada,cadeia)
