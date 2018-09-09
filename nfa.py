from graphviz import Digraph

class Automata():
    def __init__(self,expr):
        expression = ''.join(expr)
        self.start = 0
        self.final = 1
        self.new = 2
        self.nfa = {0:{expression:1}}
    
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
                print(transicao,trans)
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
                    print(r1,'----',r2)
                    afn.concat(r1,r2)
                    print(afn.nfa)
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
