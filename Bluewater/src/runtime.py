from errors import Sytaxerror, Extensionerror, Miscerror, terminate

ast = []
env = {}
def  evaluate(ast: list):
        KW = ["*", "/", "-",  "+", "set", "print", "scan", "if", "while", "list", "append", "index", ">", "<", ">=", "<=" ,"==", "!=", "true", "false", "&", "|"]
        if isinstance(ast, list):
            if not ast or not (isinstance(ast[0], str) and ast[0] in KW):
                return ast
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
                            res = None
                            for act in ast[idx + 2:]:
                                res = evaluate(act)
                            return res
                        else:
                            return False
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