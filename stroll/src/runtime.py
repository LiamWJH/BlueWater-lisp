import builtins
import math
from pathlib import Path
from lexer import tokenize
from parser import parse

class _Return(Exception): # custom return class
    def __init__(self, value):
        self.value = value

LOADED_MODULE: set[str] = set() # set is a cool thing :D

def _formatimport(name: str, default: str = ".sr") -> str: # yeah literally so the stupid guy can write elborate stuff ofc
    p = Path(name)
    return str(p if p.suffix else p.with_suffix(default))

def _getmodulepath(kind: str, name: str, here_file: str) -> Path: # wdym u dont understand look at the name
    here = Path(here_file).resolve()
    name = _formatimport(name)
    if kind == "std":
        return (here.parent / ".." / "lib" / name).resolve()
    else:
        return (here.parent / name).resolve()

def import_module(kind: str, name: str, env: dict, here_file: str) -> str: # self documentation through name
    path = _getmodulepath(kind, name, here_file)
    if not path.exists():
        raise FileNotFoundError(f"use: cannot find module file: {path}")
    abspath = str(path)

    # This is because if its already have it we dont have to add the fn to env again thats a WASTE if you import much
    if abspath in LOADED_MODULE:
        return abspath
    
    src = path.read_text(encoding="utf-8")
    toks = tokenize(src)
    while toks:
        line = parse(toks)
        evaluate(line, env)
    LOADED_MODULE.add(abspath)
    return abspath

NATIVE_GLOBALS = {
    "__builtins__": builtins,
    "math": math,
} # we need it for the exec and eval for native code(Safe sand box) we will be changing and adding stuff here as we use more native code

def _is_fn(v): # checks if the given v is a function
    return isinstance(v, list) and len(v) == 2 and isinstance(v[0], list)

def evaluate(ast, env=None):
    if env is None: #given no env we iniiiiiit a empty env
        env = {}

    KW = [
        "*", "/", "-", "+", "let", "if", "elif", "else", "while",
        "list", "append", "index", ">", "<", ">=", "<=", "==", "!=",
        "true", "false", "&", "|", "sqrt", "pow", "mod", "abs",
        "len", "reverse", "concat", "strlen", "substr",
        "fn", "call", "native", "use", "return"
    ] # we are transitioning from putting builtings in the KW to the core and lib folder

    E = lambda x: evaluate(x, env) # lambda func cause it looks cool and does stuff xD

    if isinstance(ast, list): # it means its a list or a form of command
        if not ast: # just in case yk
            return []
        
        head = ast[0] # all lisp keyword/function should be at the index 0

        if isinstance(head, str) and head not in KW and head in env and _is_fn(env[head]): # just checking if its a imported func
            params, body = env[head] # unpacking for the imported function
            args = [E(a) for a in ast[1:]] # Arguments that was given
            localenv = env | dict(zip(params, args)) # just adding it in the local env

            try: # try statement because we use a custom return keyword
                result = None
                for expr in body:
                    result = evaluate(expr, localenv)
                return result
            
            except _Return as r:
                return r.value
            
        if not (isinstance(head, str) and head in KW): # not a keyword and is a list
            return [E(x) for x in ast]
        
        for idx, token in enumerate(ast):
            if token not in KW and token in env and _is_fn(env[token]): # runs an imported function
                fnname = token
                passedinargs = ast[idx + 1:]
                params, body = env[fnname]
                args = [E(a) for a in passedinargs]
                localenv = env | dict(zip(params, args))
                try:
                    result = None
                    for expr in body:
                        result = evaluate(expr, localenv)
                    return result
                except _Return as r:
                    return r.value
            
            # Math stuff
            if token == "*":     return E(ast[idx + 1]) * E(ast[idx + 2])
            if token == "/":     return E(ast[idx + 1]) / E(ast[idx + 2])
            if token == "-":     return E(ast[idx + 1]) - E(ast[idx + 2])
            if token == "+":     return E(ast[idx + 1]) + E(ast[idx + 2])
            if token == "mod":   return E(ast[idx + 1]) % E(ast[idx + 2])
            if token == "pow":   return math.pow(E(ast[idx + 1]), E(ast[idx + 2]))
            if token == "sqrt":  return math.sqrt(E(ast[idx + 1]))
            if token == "abs":   return abs(E(ast[idx + 1]))

            # comapritives
            if token == ">":     return E(ast[idx + 1]) >  E(ast[idx + 2])
            if token == "<":     return E(ast[idx + 1]) <  E(ast[idx + 2])
            if token == ">=":    return E(ast[idx + 1]) >= E(ast[idx + 2])
            if token == "<=":    return E(ast[idx + 1]) <= E(ast[idx + 2])
            if token == "==":    return E(ast[idx + 1]) == E(ast[idx + 2])
            if token == "!=":    return E(ast[idx + 1]) != E(ast[idx + 2])

            # logic
            if token == "&":     return bool(E(ast[idx + 1]) and E(ast[idx + 2]))
            if token == "|":     return bool(E(ast[idx + 1]) or  E(ast[idx + 2]))

            # return as in return
            if token == "return": raise _Return(E(ast[idx + 1]))

            # let for assignment
            if token == "let":
                name = ast[idx + 1]
                value = E(ast[idx + 2])
                env[name] = value
                return (name, value)
            
            # Array stuff
            # list for initiating a dynamic array
            if token == "list":
                return [E(x) for x in ast[idx + 1:]]
            
            # append as in appending a obj in an array
            if token == "append":
                name = ast[idx + 1]
                value = E(ast[idx + 2])
                if name not in env or not isinstance(env[name], list):
                    raise TypeError(f"append: '{name}' is not a list")
                env[name].append(value)
                return env[name]
            
            # index for performing many task on arrays
            if token == "index":
                name   = ast[idx + 1]
                index  = E(ast[idx + 2])
                action = ast[idx + 3] if len(ast) > idx + 3 else "get" # get is just index grabbing

                if name not in env or not isinstance(env[name], list):
                    raise TypeError(f"index: '{name}' is not a list")
                
                if action == "delete": # obviously
                    val = env[name][index]
                    del env[name][index]
                    return val
                elif action == "get": # obviously
                    return env[name][index]
                else: # edge case
                    val = E(action)
                    env[name][index] = val
                    return (name, index, val)
                
            if token == "len": # will be replaced in the core module soon
                return len(E(ast[idx + 1]))
            
            if token == "reverse": # will be replaced in the core module soon
                name = ast[idx + 1]
                if name not in env or not isinstance(env[name], list):
                    raise TypeError(f"reverse: '{name}' is not a list")
                env[name].reverse()
                return env[name]
            
            if token == "concat": # will be replaced in the core module soon
                return str(E(ast[idx + 1])) + str(E(ast[idx + 2]))
            if token == "strlen": # will be replaced in the core module soon
                return len(str(E(ast[idx + 1])))
            if token == "substr": # will be replaced in the core module soon
                s = str(E(ast[idx + 1]))
                start = int(E(ast[idx + 2]))
                end   = int(E(ast[idx + 3]))
                return s[start:end]
            
            #control flow btw
            if token == "if":
                cond = E(ast[idx + 1])
                then_body = [] # then body contains if the condition is already satisfied
                elifs = [] # contains all the elifs
                else_body = None # there can be always 1 else idiot

                i = idx + 2

                while i < len(ast):
                    part = ast[i]

                    if isinstance(part, list) and part:
                        head2 = part[0] # for seeing the elifs and else

                        if head2 == "elif":
                            elifs.append((part[1], part[2:]))
                            i += 1
                            continue
                        if head2 == "else":
                            else_body = part[1:]
                            i += 1
                            continue

                    then_body.append(part) # just append the code to the then if it isnt anything special
                    i += 1

                if cond:
                    result = None
                    for stmt in then_body:
                        result = E(stmt)
                    return result
                
                for ec, body in elifs: # ec means Elif Condition
                    if E(ec):
                        result = None
                        for line in body:
                            result = E(line)
                        return result
                    
                if else_body is not None: # run the else body if exists and matches condtion
                    result = None
                    for stmt in else_body:
                        result = E(stmt)
                    return result
                return False
            
            if token == "while": # while loop obviously
                condition = ast[idx + 1]
                body = ast[idx + 2:]
                while E(condition):
                    for line in body:
                        E(line)
                return None
            
            if token == "use": # import
                kind = E(ast[idx + 1])
                mod  = E(ast[idx + 2])
                if not isinstance(kind, str):
                    raise TypeError("use: expected string for kind ('std' or 'local')")
                if not isinstance(mod, str):
                    raise TypeError("use: expected string for module filename")
                
                imported_path = import_module(kind, mod, env, __file__)
                return imported_path
            
            if token == "fn": # fn definition
                fnname = ast[idx + 1]
                raw = ast[idx + 2]
                if isinstance(raw, list): # if there is no more than 1 given args
                    params = raw
                elif isinstance(raw, str): # more than 1 args
                    params = raw.split("|") if "|" in raw else [raw]
                else:
                    raise TypeError("fn params must be list or 'x|y|z' string")
                
                fnbody = ast[idx + 3:] # grab all the code
                env[fnname] = [params, fnbody]
                return fnname
            
            if token == "call": # useless for now but jic
                fnname = ast[idx + 1]
                passedinargs = ast[idx + 2:]
                if fnname not in env:
                    raise NameError(f"call: unknown function '{fnname}'")
                params, body = env[fnname]
                args = [E(a) for a in passedinargs]
                localenv = env | dict(zip(params, args))
                try:
                    result = None
                    for expr in body:
                        result = evaluate(expr, localenv)
                    return result
                except _Return as r:
                    return r.value
                
            if token == "native": # native code stuff for writeing important stuff
                code = E(ast[idx + 1])
                if not isinstance(code, str):
                    return code
                native_locals = {k: v for k, v in env.items() if not _is_fn(v)}
                try:
                    return eval(code, NATIVE_GLOBALS, native_locals)
                except SyntaxError:
                    exec(code, NATIVE_GLOBALS, native_locals)
                    env.update(native_locals)
                    return None
    
    #finally out of kw hell
    elif isinstance(ast, (int, float)):
        return ast
    elif isinstance(ast, str): 
        # just in case bools sneak in
        if ast == "true":  return True
        if ast == "false": return False

        if ast.isnumeric():
            return int(ast)
        if (ast.startswith("'") and ast.endswith("'")) or (ast.startswith('"') and ast.endswith('"')): # string unwrap
            return ast[1:-1]
        try:
            return float(ast)
        except Exception:
            if ast in env:
                return env[ast]
            return None
    else:
        return None
