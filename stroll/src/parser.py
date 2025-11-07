from errors import Syntaxerror, Extensionerror, Miscerror, terminate

def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return str(token)

def parse(tokens, inquote=False, quotetype=None):
    print(tokens)
    token = tokens.pop(0)

    if token == "'" or token == '"' or token == "\'" or token == '\"':
        if inquote:
            if token == quotetype:
                inquote = False
                quotetype=None
        else:
            inquote = True
            quotetype == quotetype

    if token == '(' and inquote==False:
        L = []

        while tokens[0] != ')':
            L.append(parse(tokens, inquote, quotetype))
        tokens.pop(0)
        return L
    else:
        return atom(token)