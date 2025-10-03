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
        KW = ["*", "/", "-",  "+", "set", "print", "scan", "if", "while", ">", "<", ">=", "<=" ,"==", "!="]
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
                    if token == "set":
                        name = ast[idx + 1]
                        value = evaluate(ast[idx + 2])
                        env[name] = value
                        return (name,value)
                    if token == "print":
                        value = evaluate(ast[idx + 1])
                        print(value)
                        return (value)
                    if token == "scan":
                        value = evaluate(ast[idx + 1])
                        return evaluate(input(value))
                    if token == "if":
                        cond = evaluate(ast[idx + 1])
                        if cond:
                            c1 = evaluate(ast[idx + 2])
                            return c1
                        else:
                            c2 = evaluate(ast[idx + 3])
                            return c2
                    if token == "while":
                        block = ast[idx+2:len(ast)]
                        while evaluate(ast[idx + 1]):
                            for line in block:
                                evaluate(line)
        elif type(ast) == int or type(ast) == float:
            return ast
        else:
            if ast.isnumeric():
                return int(ast)

            elif ast.startswith("'") and ast.endswith("'") or ast.startswith('"') and ast.endswith('"'):
                return ast[1:-1]
            else:
                if ast.isalpha():
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

