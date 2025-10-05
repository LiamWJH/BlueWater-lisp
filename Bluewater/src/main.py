import math

import argparse
argparser = argparse.ArgumentParser()
argparser.add_argument("FILENAME", help="filename you wish to run")
args = argparser.parse_args()

USERCODE = ""

with open(args.FILENAME, "r") as f:
    USERCODE = f.read()


#Goal write a program that can do that 
#after that bind it to a vm
#for now no consideration on string 
def tokenize(s: str):
    tokens = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue

        if c in '()':
            tokens.append(c)
            i += 1
            continue

        if c == '"':
            i += 1
            buf = []
            while i < n:
                if s[i] == '\\' and i + 1 < n:
                    # keep escapes like \" or \\ intact
                    buf.append(s[i + 1])
                    i += 2
                elif s[i] == '"':
                    i += 1
                    break
                else:
                    buf.append(s[i])
                    i += 1
            tokens.append('"' + ''.join(buf) + '"')
            continue

        # single-quoted strings (optional)
        if c == "'":
            i += 1
            buf = []
            while i < n and s[i] != "'":
                if s[i] == '\\' and i + 1 < n:
                    buf.append(s[i + 1])
                    i += 2
                else:
                    buf.append(s[i]); i += 1
            if i < n and s[i] == "'":
                i += 1
            tokens.append("'" + ''.join(buf) + "'")
            continue

        # symbols / numbers
        j = i
        while j < n and (not s[j].isspace()) and s[j] not in '()':
            j += 1
        tokens.append(s[i:j])
        i = j

    return tokens

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
env = {}
def  evaluate(ast: list): # ast must be a single liner
        KW = ["*", "/", "-",  "+", "set", "print", "scan", "if", "while", "list", "append", "index", ">", "<", ">=", "<=" ,"==", "!=", "true", "false", "&", "|", "mod", "pow", "sqrt", "abs", "concat", "strlen", "substr", "len", "reverse"]
        # Put this at the top of evaluate()
        if isinstance(ast, list):
            if not ast or not (isinstance(ast[0], str) and ast[0] in KW):
                return ast  # treat as DATA list, not code
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
                    if token == "&":
                        if evaluate(ast[idx + 1]) and evaluate(ast[idx + 2]):
                            return True
                        else:
                            return False
                    if token == "|":
                        if evaluate(ast[idx + 1]) or evaluate(ast[idx + 2]):
                            return True
                        else:
                            return False
                    if token == "mod":
                        return evaluate(ast[idx + 1]) % evaluate(ast[idx + 2])
                    if token == "pow":
                        return evaluate(ast[idx + 1]) ** evaluate(ast[idx + 2])
                    if token == "sqrt":
                        return math.sqrt(evaluate(ast[idx + 1]))
                    if token == "abs":
                        return abs(evaluate(ast[idx + 1]))

                    #Functions
                    if token == "set":
                        name = ast[idx + 1]
                        value = evaluate(ast[idx + 2])
                        env[name] = value
                        return (name,value)
                    if token == "list":
                        return [evaluate(x) for x in ast[idx+1:]]
                    if token == "append":
                        name = ast[idx + 1]
                        value = evaluate(ast[idx + 2])
                        env[name].append(value)
                    if token == "index":
                        name = ast[idx + 1]
                        _idx = evaluate(ast[idx + 2])
                        change = ast[idx + 3]
                        if change == "delete":
                            val = env[name][_idx]
                            del env[name][_idx]
                            return val 
                        elif change == "get":
                            val = env[name][_idx]
                            return val
                        else:
                            change = evaluate(change)
                            env[name][_idx] = change
                            return (name, idx, change)
                        
                    if token == "print":
                        value = evaluate(ast[idx + 1])
                        print(value)
                        return (value)
                    if token == "scan":
                        value = evaluate(ast[idx + 1])
                        return input(value)
                    if token == "if":
                        cond = evaluate(ast[idx + 1])
                        if cond:
                            #print("cond satisfied: ")
                            res = None
                            for act in ast[idx + 2:]:
                                res = evaluate(act)
                            return res
                        else:
                            #c2 = evaluate(ast[idx + 3])
                            return False
                    if token == "while":
                        block = ast[idx+2:len(ast)]
                        while evaluate(ast[idx + 1]):
                            for line in block:
                                evaluate(line)
                    if token == "concat":
                        return str(evaluate(ast[idx + 1])) + str(evaluate(ast[idx + 2]))
                    if token == "strlen":
                        return len(str(evaluate(ast[idx + 1])))
                    if token == "substr":
                        string = str(evaluate(ast[idx + 1]))
                        start = evaluate(ast[idx + 2])
                        end = evaluate(ast[idx + 3])
                        return string[start:end]
                    if token == "len":
                        return len(evaluate(ast[idx + 1]))
                    if token == "reverse":
                        lst = evaluate(ast[idx + 1])
                        return lst[::-1]

        elif type(ast) == int or type(ast) == float:
            return ast
        else:
            if ast.isnumeric():
                return int(ast)

            elif ast.startswith("'") and ast.endswith("'") or ast.startswith('"') and ast.endswith('"'):
                return ast[1:-1]
            else:
                if ast.isalpha():
                    if ast == "true":
                        return True
                    elif ast == "false":
                        return False
                    else:
                        return env[ast]
                else:
                    try:
                        return float(ast)
                    except:
                        print("sh*t" + ast)
                

src = []
for raw_line in USERCODE.splitlines():
    code = raw_line.split(";", 1)[0]
    if code.strip():
        src.append(code)

tokens = tokenize("\n".join(src))

ast = []
while tokens:
    ast.append(parse(tokens))

for action in ast:
    evaluate(action)

