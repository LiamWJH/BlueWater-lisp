from errors import Sytaxerror, Extensionerror, Miscerror, terminate

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

        j = i
        while j < n and (not s[j].isspace()) and s[j] not in '()':
            j += 1
        tokens.append(s[i:j])
        i = j

    return tokens