import math
import itertools
legalOps = ["+", "-", "*", "/", "**"]
#legalOps = ["+", "-", "*", "/"] #we omit exponentiation so the program doesn't crash
replaceT = { #switch characters to python equivalents
    "**": "^"
    }

#note bracketPos takes values from 0 to 3, and is the position of the end bracket
#lens: numbers=4, operations=3, bracketPos=4
#note: doesn't account for all 4 numbers being negative; work out that case seperately.

def prune(numbers, operations, bracketPos): #meant to delete duplicates (ex 1+2+3+4 and 4+3+2+1)
    if((operations[0] == operations[1]) and (operations[1] == operations[2]) and (operations[1] == "+" or operations[1] == "*")):
        if((numbers[0] > numbers[1]) or (numbers[1] > numbers[2]) or (numbers[2] > numbers[3])): #only return false if a<b<c<d
            return True
    for i in range(len(operations)):
        if((operations[i] == "+" or operations[i] == "*") and bracketPos[i] <= i+1 and bracketPos[i+1] == i+1): #addition and multiplication are commutative
            if(numbers[i] > numbers[i+1]):
                return True
    return False

def pvalu(numbers, operations, bracketPos): #Used to print expressions
    expression = ""
    expression += "(" + str(int(numbers[0]))
    currentClose = 0
    for i in range(3):
        if(bracketPos[currentClose] == i):
            expression += ")"
            currentClose += 1
            if(bracketPos[currentClose] == i):
                expression += ")"
                currentClose += 1
                if(bracketPos[currentClose] == i):
                    expression += ")"
                    currentClose += 1
        expression += operations[i] + "(" + str(int(numbers[i+1]))
    for i in range(4-currentClose):
        expression += ")"
    return expression

def evalu(numbers, operations, bracketPos): #Evaluates the value of generated expressions
    expression = ""
    expression += "(" + str(numbers[0])
    currentClose = 0
    for i in range(3):
        if(bracketPos[currentClose] == i):
            expression += ")"
            currentClose += 1
            if(bracketPos[currentClose] == i):
                expression += ")"
                currentClose += 1
                if(bracketPos[currentClose] == i):
                    expression += ")"
                    currentClose += 1
        expression += operations[i] + "(" + str(numbers[i+1])
    for i in range(4-currentClose):
        expression += ")"
    try:
        return eval(expression)
    except ZeroDivisionError:
        return math.nan
    except OverflowError:
        return math.nan

def generate1(numbers, target): #generates all possible operations based on a set of numbers
    out = []
    for i in range(len(legalOps)):
        for j in range(len(legalOps)):
            for k in range(len(legalOps)):
                for a in range(4):
                    b = 1
                    maxb = max(4 * (a<1), a+1)
                    while(b < maxb):
                        c = 2
                        maxc = max(4 * (b<2), b+1)
                        while(c < maxc):
                            d = 3
                            while(d < 4):
                                if(not prune(numbers, [legalOps[i], legalOps[j], legalOps[k]], [a, b, c, d]) and evalu(numbers, [legalOps[i], legalOps[j], legalOps[k]], [a, b, c, d]) == target):
                                    out.append(pvalu(numbers, [legalOps[i], legalOps[j], legalOps[k]], [a, b, c, d]))
                                d += 1
                            c += 1
                        b += 1
    return out

def generate(numbers, target): #generates the answers. Ex. generate([4, 2, 5, 6], 24)
    out = []
    numbers2 = [float(j) for j in numbers]
    numsTry = list(itertools.permutations(numbers2))
    for i in numsTry:
        out += generate1(i, target)
    out = [p.replace(f, replaceT[f]) for f in replaceT for p in out]
    print("\n".join(out)) #remember to change later
