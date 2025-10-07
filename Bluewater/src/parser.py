from errors import Sytaxerror, Extensionerror, Miscerror, terminate

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
    if token == '(':
        L = []

        while tokens[0] != ')':
            L.append(parse(tokens))
        tokens.pop(0)
        return L
            
    else:
        return atom(token)