test_code = """
(+ 1 2)           ; 3
(* 2 (+ 1 3))     ; 8
(define x 42)     ; binds x = 42
(if (> x 40) (print "big") "small") ; returns "big"
(print "hello")
(print x)
"""
#Goal write a program that can do that 
#after that bind it to a vm
#for now no consideration on string

def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return str(token)


def parse(tokens):
    
    token = tokens.pop(0)
    if token == '(':         # start new list
        L = []
        while tokens[0] != ')':
            L.append(parse(tokens))
        tokens.pop(0)        # discard ')'
        return L
    else:
        return atom(token)
ast = []
preenv = {}

def  evaluate(ast: list): # ast must be a single liner
        KW = ["*", "/", "-",  "+", "define", "print", "if", ">", "<", ">=", "<=" ,"==", "!="]
        #print("dbg" + str(ast))
        if type(ast) == list:
            for idx, token in enumerate(ast):
                if token in KW:
                    if token == "*":
                        return evaluate(ast[idx + 1]) * evaluate(ast[idx + 2])
                    if token == "/":
                        return evaluate(ast[idx + 1]) / evaluate(ast[idx + 2])
                    if token == "-":
                        return evaluate(ast[idx + 1]) - evaluate(ast[idx + 2])
                    if token == "+":
                        return evaluate(ast[idx + 1]) + evaluate(ast[idx + 2])
                    if token == ">":
                        return evaluate(ast[idx + 1]) > evaluate(ast[idx + 2])
                    if token == "<":
                        return evaluate(ast[idx + 1]) < evaluate(ast[idx + 2])
                    if token == ">=":
                        return evaluate(ast[idx + 1]) >= evaluate(ast[idx + 2])
                    if token == "<=":
                        return evaluate(ast[idx + 1]) <= evaluate(ast[idx + 2])
                    if token == "==":
                        return evaluate(ast[idx + 1]) == evaluate(ast[idx + 2])
                    if token == "!=":
                        return evaluate(ast[idx + 1]) != evaluate(ast[idx + 2])
                    
                    #Functions
                    if token == "define":
                        preenv[ast[idx + 1]] = evaluate(ast[idx + 2])
                        return ("IDENT",ast[idx + 1],evaluate(ast[idx + 2]))
                    if token == "print":
                        return ("FUNC", "print", evaluate(ast[idx + 1]))
                    if token == "if":
                        if evaluate(ast[idx + 1]):
                            return evaluate(ast[idx + 2])
                        else:
                            return evaluate(ast[idx + 3])

        elif type(ast) == int or type(ast) == float:
            try:
                return int(ast)
            except TypeError:
                try:
                    return float(ast)
                except TypeError:
                    print("sh*t")

        elif ast.startswith("'") and ast.endswith("'") or ast.startswith('"') and ast.endswith('"'):
            return ast[1:-1]
        else:
            if ast.isalpha():
                return preenv[ast]
            else:
                print("sh*t shi*")
                
def run(instruction: list):
    env = {}
    for action in instruction:
        if type(action) == tuple:
            if action[0] != "IDENT":
                funcname = action[1]

                if funcname == "print":
                    print(action[2])
            else:
                try:
                    env[action[1]] = action[2]
                except:
                    print("shit"+str(action))
        else:
            #print("sh*t")
            pass

for line in test_code.splitlines():
    line = line.split(";", 1)[0]
    if not line.strip():
        continue
    ast.append(parse(line.replace('(', ' ( ').replace(')', ' ) ').split()))

finalast = []
for line in ast:
    finalast.append(evaluate(line))

print("Ast final", finalast)

run(finalast)

