from errors import Syntaxerror, Extensionerror, Miscerror, terminate

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
    #a = tokens.copy()
    if token == '(':
        L = []
        try:
            while tokens[0] != ')':
                L.append(parse(tokens))
                if len(tokens) == 0:
                    break
            try:
                tokens.pop(0)
            finally:
                return L
        except Exception as e:
            print(e)
    else:
        return atom(token)