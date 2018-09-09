regex = input("Digite expressao regular:")
print(regex)
count = 0
L = []
abre_par = []
fecha_par = []
for i in regex:
    L.append(i)


def recursao(expr):
    r1 = []
    r2 = []
    previous = '&'
    testa = 1
    n = len(expr)
    if n <= 2:
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
        recursao(r1)
    count = 0
    for i in range(0,n-1):
        if testa == 1:
            if expr[i].isalpha():
                if (previous == '*' or previous.isalpha()) and count == 0:
                    r1 = expr[0:i]
                    r2 = expr[i:n]
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
                        recursao(r1)
                        if i != n-2:
                            r2 = expr[i+2:n]
                            recursao(r2)
                        testa = 0
                    else:
                        r1 = expr[1:i]
                        recursao(r1)
                        testa = 0
            elif expr[i] == '*':
                if count == 0:
                    r1 = expr[0:i+1]
                    r2 = expr[i+1:n]
                    recursao(r1)
                    recursao(r2)
                    testa = 0
            previous = expr[i]
                
            
recursao(L)
regex = input("Digite expressao regular:")     
            
