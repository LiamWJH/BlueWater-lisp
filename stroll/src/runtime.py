import builtins
import math
from pathlib import Path
from lexer import tokenize
from parser import parse

try:
    MODULE_CACHE: set[str] = set()
except TypeError:
    from typing import Set
    MODULE_CACHE = set()

def _ensure_ext(name: str, default: str = ".sr") -> str:
    p = Path(name)
    return str(p if p.suffix else p.with_suffix(default))

def _resolve_module(kind: str, name: str, here_file: str) -> Path:
    here = Path(here_file).resolve()
    name = _ensure_ext(name)
    if kind == "std":
        return (here.parent / ".." / "lib" / name).resolve()
    else:
        return (here.parent / name).resolve()

def import_module(kind: str, name: str, env: dict, here_file: str) -> str:
    path = _resolve_module(kind, name, here_file)
    if not path.exists():
        raise FileNotFoundError(f"use: cannot find module file: {path}")

    abspath = str(path)
    if abspath in MODULE_CACHE:
        return abspath

    src = path.read_text(encoding="utf-8")
    toks = tokenize(src)

    while toks:
        form = parse(toks)
        evaluate(form, env)

    MODULE_CACHE.add(abspath)
    return abspath

NATIVE_GLOBALS = {
    "__builtins__": {
        "print": builtins.print,
        "input": builtins.input,
        "len": builtins.len,
        "range": builtins.range,
        "abs": builtins.abs,
        "min": builtins.min,
        "max": builtins.max,
        "sum": builtins.sum,
    },
    "math": math,
}

def _is_lang_fn(v):
    return isinstance(v, list) and len(v) == 2 and isinstance(v[0], list)


def evaluate(ast, env=None):
    if env is None:
        env = {}

    KW = [
        "*", "/", "-", "+", "let", "if", "elif", "else", "while",
        "list", "append", "index", ">", "<", ">=", "<=", "==", "!=",
        "true", "false", "&", "|", "sqrt", "pow", "mod", "abs",
        "len", "reverse", "concat", "strlen", "substr",
        "fn", "call", "native", "use", "return"
    ]

    E = lambda x: evaluate(x, env)
    if isinstance(ast, list):
        if not ast or not (isinstance(ast[0], str) and ast[0] in KW):
            return [E(x) for x in ast]

        for idx, token in enumerate(ast):
            if token not in KW:
                continue

            if token == "*":     return E(ast[idx + 1]) * E(ast[idx + 2])
            if token == "/":     return E(ast[idx + 1]) / E(ast[idx + 2])
            if token == "-":     return E(ast[idx + 1]) - E(ast[idx + 2])
            if token == "+":     return E(ast[idx + 1]) + E(ast[idx + 2])
            if token == "mod":   return E(ast[idx + 1]) % E(ast[idx + 2])
            if token == "pow":   return math.pow(E(ast[idx + 1]), E(ast[idx + 2]))
            if token == "sqrt":  return math.sqrt(E(ast[idx + 1]))
            if token == "abs":   return abs(E(ast[idx + 1]))

            if token == ">":     return E(ast[idx + 1]) >  E(ast[idx + 2])
            if token == "<":     return E(ast[idx + 1]) <  E(ast[idx + 2])
            if token == ">=":    return E(ast[idx + 1]) >= E(ast[idx + 2])
            if token == "<=":    return E(ast[idx + 1]) <= E(ast[idx + 2])
            if token == "==":    return E(ast[idx + 1]) == E(ast[idx + 2])
            if token == "!=":    return E(ast[idx + 1]) != E(ast[idx + 2])

            if token == "&":     return bool(E(ast[idx + 1]) and E(ast[idx + 2]))
            if token == "|":     return bool(E(ast[idx + 1]) or  E(ast[idx + 2]))

            if token == "return": return E(ast[idx + 1])

            # --- Variables ---
            if token == "let":
                name = ast[idx + 1]
                value = E(ast[idx + 2])
                env[name] = value
                return (name, value)

            # --- Lists ---
            if token == "list":
                return [E(x) for x in ast[idx + 1:]]

            if token == "append":
                name = ast[idx + 1]
                value = E(ast[idx + 2])
                if name not in env or not isinstance(env[name], list):
                    raise TypeError(f"append: '{name}' is not a list")
                env[name].append(value)
                return env[name]

            if token == "index":
                name   = ast[idx + 1]
                index  = E(ast[idx + 2])
                action = ast[idx + 3] if len(ast) > idx + 3 else "get"
                if name not in env or not isinstance(env[name], list):
                    raise TypeError(f"index: '{name}' is not a list")
                if action == "delete":
                    val = env[name][index]
                    del env[name][index]
                    return val
                elif action == "get":
                    return env[name][index]
                else:
                    val = E(action)
                    env[name][index] = val
                    return (name, index, val)

            if token == "len":
                return len(E(ast[idx + 1]))

            if token == "reverse":
                name = ast[idx + 1]
                if name not in env or not isinstance(env[name], list):
                    raise TypeError(f"reverse: '{name}' is not a list")
                env[name].reverse()
                return env[name]

            # --- String ops ---
            if token == "concat":
                return str(E(ast[idx + 1])) + str(E(ast[idx + 2]))
            if token == "strlen":
                return len(str(E(ast[idx + 1])))
            if token == "substr":
                s = str(E(ast[idx + 1]))
                start = int(E(ast[idx + 2]))
                end   = int(E(ast[idx + 3]))
                return s[start:end]

            # --- I/O ---
            """
            if token == "print":
                value = E(ast[idx + 1])
                print(value)
                return value

            if token == "scan":
                prompt = E(ast[idx + 1])
                return input(prompt)
            """

            # --- Control Flow ---
            if token == "if":
                cond = E(ast[idx + 1])
                then_body = []
                elifs = []
                else_body = None

                i = idx + 2
                while i < len(ast):
                    part = ast[i]
                    if isinstance(part, list) and part:
                        head = part[0]
                        if head == "elif":
                            elifs.append((part[1], part[2:]))
                            i += 1
                            continue
                        if head == "else":
                            else_body = part[1:]
                            i += 1
                            continue
                    then_body.append(part)
                    i += 1

                if cond:
                    result = None
                    for stmt in then_body:
                        result = E(stmt)
                    return result

                for ec, body in elifs:
                    if E(ec):
                        result = None
                        for line in body:
                            result = E(line)
                        return result

                if else_body is not None:
                    result = None
                    for stmt in else_body:
                        result = E(stmt)
                    return result

                return False

            if token == "while":
                condition = ast[idx + 1]
                body = ast[idx + 2:]
                while E(condition):
                    for line in body:
                        E(line)
                return None

            # --- Imports ---
            if token == "use":
                kind = E(ast[idx + 1])   # "std" or "local"
                mod  = E(ast[idx + 2])   # filename (".sr" optional)
                if not isinstance(kind, str):
                    raise TypeError("use: expected string for kind ('std' or 'local')")
                if not isinstance(mod, str):
                    raise TypeError("use: expected string for module filename")
                imported_path = import_module(kind, mod, env, __file__)
                return imported_path

            # --- Functions ---
            if token == "fn":
                fnname = ast[idx + 1]
                raw    = ast[idx + 2]
                if isinstance(raw, list):
                    params = raw
                elif isinstance(raw, str):
                    params = raw.split("|") if "|" in raw else [raw]
                else:
                    raise TypeError("fn params must be list or 'x|y|z' string")
                fnbody = ast[idx + 3:]
                env[fnname] = [params, fnbody]
                return fnname

            if token == "call":
                fnname = ast[idx + 1]
                passedinargs = ast[idx + 2:]
                if fnname not in env:
                    raise NameError(f"call: unknown function '{fnname}'")
                params, body = env[fnname]
                args = [E(a) for a in passedinargs]
                # Create a shallow local scope with params bound
                localenv = env | dict(zip(params, args))
                result = None
                for expr in body:
                    result = evaluate(expr, localenv)
                return result

            # --- Native (Python) ---
            if token == "native":
                code = E(ast[idx + 1])
                if not isinstance(code, str):
                    return code

                # Locals: env without language functions (avoid shadowing Python names)
                native_locals = {k: v for k, v in env.items() if not _is_lang_fn(v)}

                try:
                    return eval(code, NATIVE_GLOBALS, native_locals)
                except SyntaxError:
                    exec(code, NATIVE_GLOBALS, native_locals)
                    env.update(native_locals)
                    return None

    # ---- Literals / atoms -------------------------------------------
    elif isinstance(ast, (int, float)):
        return ast

    elif isinstance(ast, str):
        # booleans
        if ast == "true":  return True
        if ast == "false": return False

        # integer
        if ast.isnumeric():
            return int(ast)

        # quoted string
        if (ast.startswith("'") and ast.endswith("'")) or (ast.startswith('"') and ast.endswith('"')):
            return ast[1:-1]

        # float fallback
        try:
            return float(ast)
        except Exception:
            # variable lookup last
            if ast in env:
                return env[ast]
            print(f"Runtime error: invalid token '{ast}'")
            return None

    # ---- Unknown -----------------------------------------------------
    else:
        print(f"Unknown AST type: {type(ast)}")
        return None
