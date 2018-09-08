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
    n = len(expr)
    if n == 1 or (n==2 and expr[n-1]=='*'):
        print('aqui')
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
            print(r1)
            print(r2)
            print('here')
            recursao(r1)
            recursao(r2)
    count = 0
    for i in range(0,n-1):
        if expr[i] == ('a' or 'b' or 'c'):
            if previous == ('*' or ('a' or 'b' or 'c')) and count == 0:
                r1 = expr[0:i-1]
                r2 = expr[i:n-1]
                print(r1)
                print(r2)
                recursao(r1)
                recursao(r2)
            else: r1.append(expr[i])
        elif expr[i] == '(':
            if previous != '&':
                r1 = expr[0:i-1]
                r2 = expr[i:n-1]
                print(r1)
                print(r2)
                recursao(r1)
                recursao(r2)
            else: r1.append(expr[i])
            count = count + 1
        elif expr[i] == '+':
            r1.append(expr[i])
        elif expr[i] == ')':
            count = count - 1
            if count == 0:
                if expr[i+1] == '*':
                  """ fecho de kleene"""
                else:
                    r1 = expr[1:i-1]
                    recursao(r1)
        previous = expr[i]
                
            


recursao(L)
            