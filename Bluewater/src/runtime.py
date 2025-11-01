import math

# Global environment (stores variables)
env = {}

def evaluate(ast):
    global env
    KW = [
        "*", "/", "-", "+", "let", "print", "scan", "if", "while",
        "list", "append", "index", ">", "<", ">=", "<=", "==", "!=",
        "true", "false", "&", "|", "sqrt", "pow", "mod", "abs",
        "len", "reverse", "concat", "strlen", "substr", "nativecode", "fn"
    ]
    #print(ast,"!")
    # ---- Base case: AST is a list ----
    if isinstance(ast, list):
        # Return literal list if it's not a keyword expression
        if not ast or not (isinstance(ast[0], str) and ast[0] in KW):
            return [evaluate(x) for x in ast]

        # Evaluate each operation
        for idx, token in enumerate(ast):
            if token not in KW:
                try:
                    if token in env:
                        print(token,"is a function")
                    else:
                        continue
                except Exception:
                    continue
                    
            # --- Math Operations ---
            if token == "*":
                return evaluate(ast[idx + 1]) * evaluate(ast[idx + 2])
            if token == "/":
                return evaluate(ast[idx + 1]) / evaluate(ast[idx + 2])
            if token == "-":
                return evaluate(ast[idx + 1]) - evaluate(ast[idx + 2])
            if token == "+":
                return evaluate(ast[idx + 1]) + evaluate(ast[idx + 2])
            if token == "mod":
                return evaluate(ast[idx + 1]) % evaluate(ast[idx + 2])
            if token == "pow":
                return math.pow(evaluate(ast[idx + 1]), evaluate(ast[idx + 2]))
            if token == "sqrt":
                return math.sqrt(evaluate(ast[idx + 1]))
            if token == "abs":
                return abs(evaluate(ast[idx + 1]))

            # --- Comparison ---
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

            # --- Logic ---
            if token == "&":
                return bool(evaluate(ast[idx + 1]) and evaluate(ast[idx + 2]))
            if token == "|":
                return bool(evaluate(ast[idx + 1]) or evaluate(ast[idx + 2]))

            # --- Variables ---
            if token == "let":
                name = ast[idx + 1]
                value = evaluate(ast[idx + 2])
                env[name] = value
                return (name, value)

            # --- Lists ---
            if token == "list":
                return [evaluate(x) for x in ast[idx + 1:]]
            if token == "append":
                name = ast[idx + 1]
                value = evaluate(ast[idx + 2])
                env[name].append(value)
                return env[name]
            if token == "index":
                name = ast[idx + 1]
                index = evaluate(ast[idx + 2])
                action = ast[idx + 3]

                if action == "delete":
                    val = env[name][index]
                    del env[name][index]
                    return val
                elif action == "get":
                    return env[name][index]
                else:
                    val = evaluate(action)
                    env[name][index] = val
                    return (name, index, val)
            if token == "len":
                name = ast[idx + 1]
                return len(env[name])
            if token == "reverse":
                name = ast[idx + 1]
                env[name].reverse()
                return env[name]

            # --- String operations ---
            if token == "concat":
                s1 = evaluate(ast[idx + 1])
                s2 = evaluate(ast[idx + 2])
                return str(s1) + str(s2)
            if token == "strlen":
                s = evaluate(ast[idx + 1])
                return len(str(s))
            if token == "substr":
                s = str(evaluate(ast[idx + 1]))
                start = int(evaluate(ast[idx + 2]))
                end = int(evaluate(ast[idx + 3]))
                return s[start:end]

            # --- I/O ---
            if token == "print":
                value = evaluate(ast[idx + 1])
                print(value)
                return value
            if token == "scan":
                prompt = evaluate(ast[idx + 1])
                return input(prompt)

            # --- Control Flow ---
            if token == "if":
                condition = evaluate(ast[idx + 1])
                if condition:
                    result = None
                    for act in ast[idx + 2:]:
                        result = evaluate(act)
                    return result
                return False

            if token == "while":
                condition = ast[idx + 1]
                body = ast[idx + 2:]
                while evaluate(condition):
                    for line in body:
                        evaluate(line)
                return None

            # --- functions ---

            if token == "fn": #fn define
                fnname = ast[idx + 1]
                fnvars = ast[idx + 2].split("|")# the format wil be like fn sayhi x|y|z code
                fnbody = ast[idx + 3:]

                env[fnname] = [fnvars, fnbody]

    # ---- Base case: literals ----
    elif isinstance(ast, (int, float)):
        return ast

    elif isinstance(ast, str):
        # --- Numeric ---
        if ast.isnumeric():
            return int(ast)

        # --- String literal ---
        if (ast.startswith("'") and ast.endswith("'")) or (ast.startswith('"') and ast.endswith('"')):
            return ast[1:-1]

        # --- Variables & booleans ---
        if ast in env:
            return env[ast]
        if ast == "true":
            return True
        if ast == "false":
            return False

        # --- Float ---
        try:
            return float(ast)
        except:
            print(f"Runtime error: invalid token '{ast}'")
            return None

    else:
        print(f"Unknown AST type: {type(ast)}")
        return None
