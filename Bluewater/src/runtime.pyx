# cython: language_level=3, boundscheck=False, wraparound=False, nonecheck=False, infer_types=True
cimport cython

# Global env (Python dict)
cdef dict env = {}

# Keywords as a set for O(1) membership
cdef set KW = {
    "*", "/", "-", "+",
    "set", "print", "scan", "if", "while",
    "list", "append", "index",
    ">", "<", ">=", "<=", "==", "!=",
    "true", "false", "&", "|"
}

@cython.cfunc
@cython.inline
def _truthy(object obj):
    return bool(obj)

@cython.cfunc
@cython.inline
def _num(object obj):
    cdef str s
    if isinstance(obj, (int, float)):
        return obj
    if isinstance(obj, str):
        s = obj
        if s.isnumeric():
            try:
                return int(s)
            except Exception:
                pass
        try:
            return float(s)
        except Exception:
            pass
    return obj

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef object evaluate(object ast):
    cdef object tok, a, b, name, _idx, change, res, val
    cdef Py_ssize_t i, n
    cdef list block
    cdef str s

    # ---- LIST CASE ----
    if isinstance(ast, list):
        n = len(ast)
        if n == 0:
            return ast

        # Keep original behavior: if first isn't a keyword, return list as-is
        if not (isinstance(ast[0], str) and ast[0] in KW):
            return ast

        # Dispatch by scanning (keeps your original shape)
        for i in range(n):
            tok = ast[i]
            if tok not in KW:
                continue

            # ---- arithmetic ----
            if tok == "*":
                a = evaluate(ast[i+1]); b = evaluate(ast[i+2])
                return _num(a) * _num(b)

            if tok == "/":
                a = evaluate(ast[i+1]); b = evaluate(ast[i+2])
                return _num(a) / _num(b)

            if tok == "-":
                a = evaluate(ast[i+1]); b = evaluate(ast[i+2])
                return _num(a) - _num(b)

            if tok == "+":
                a = evaluate(ast[i+1]); b = evaluate(ast[i+2])
                return _num(a) + _num(b)

            # ---- comparisons ----
            if tok == ">":
                a = evaluate(ast[i+1]); b = evaluate(ast[i+2])
                return _num(a) > _num(b)

            if tok == "<":
                a = evaluate(ast[i+1]); b = evaluate(ast[i+2])
                return _num(a) < _num(b)

            if tok == ">=":
                a = evaluate(ast[i+1]); b = evaluate(ast[i+2])
                return _num(a) >= _num(b)

            if tok == "<=":
                a = evaluate(ast[i+1]); b = evaluate(ast[i+2])
                return _num(a) <= _num(b)

            if tok == "==":
                a = evaluate(ast[i+1]); b = evaluate(ast[i+2])
                return a == b

            if tok == "!=":
                a = evaluate(ast[i+1]); b = evaluate(ast[i+2])
                return a != b

            # ---- logical ----
            if tok == "&":
                a = evaluate(ast[i+1])
                if _truthy(a):
                    b = evaluate(ast[i+2])
                    return _truthy(b)
                return False

            if tok == "|":
                a = evaluate(ast[i+1])
                if _truthy(a):
                    return True
                b = evaluate(ast[i+2])
                return _truthy(b)

            # ---- variables / lists ----
            if tok == "set":
                name = ast[i+1]
                val = evaluate(ast[i+2])
                env[name] = val
                return (name, val)

            if tok == "list":
                return [evaluate(x) for x in ast[i+1:]]

            if tok == "append":
                name = ast[i+1]
                val = evaluate(ast[i+2])
                env[name].append(val)
                return None

            if tok == "index":
                name = ast[i+1]
                _idx = evaluate(ast[i+2])
                change = ast[i+3]

                if change == "delete":
                    val = env[name][_idx]
                    del env[name][_idx]
                    return val
                elif change == "get":
                    return env[name][_idx]
                else:
                    change = evaluate(change)
                    env[name][_idx] = change
                    return (name, _idx, change)

            # ---- IO ----
            if tok == "print":
                val = evaluate(ast[i+1])
                print(val)
                return val

            if tok == "scan":
                val = evaluate(ast[i+1])
                return input(val)

            # ---- control flow ----
            if tok == "if":
                a = evaluate(ast[i+1])
                if _truthy(a):
                    res = None           # initialize before use
                    for b in ast[i+2:]:
                        res = evaluate(b)
                    return res
                return False

            if tok == "while":
                block = ast[i+2:n]       # no negative indices (wraparound=False)
                while _truthy(evaluate(ast[i+1])):
                    for b in block:
                        evaluate(b)
                return None

        # If no keyword matched, return as-is
        return ast

    # ---- NUMBER LITERAL ----
    if isinstance(ast, (int, float)):
        return ast

    # ---- STRING / SYMBOL ----
    if isinstance(ast, str):
        s = ast  # assign before use

        # quoted string literal
        if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
            return s[1:-1]

        if s == "true":
            return True
        if s == "false":
            return False

        if s.isnumeric():
            try:
                return int(s)
            except Exception:
                pass
        else:
            try:
                return float(s)
            except Exception:
                pass

        # symbol lookup
        try:
            return env[s]
        except KeyError:
            print("sh*t" + s)
            return None

    # Fallback
    return ast
