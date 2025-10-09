from errors import Syntaxerror, Miscerror, terminate


def check(tokens: list) -> bool:
    print("DBG PRINT", tokens)

    i=0
    n=len(tokens)
    while i < n:
        token = tokens[i]
        
        #Mismatched parentheses shit
        if token == "(":
            errorsource = tokens[i + 1]
            i+=1
            parentheses_depth = 1
            j=i
            token = tokens[j]
            while j<n:
                token = tokens[j]
                
                if parentheses_depth < 0:
                    print("!!!!!!!!!!!!!!!!!")
                    breakpoint()
                    print(Syntaxerror("Unmatched parentheses"))
                    terminate(errorsource)
                
                if token in "()":
                    if token == "(":
                        parentheses_depth += 1
                    else:
                        parentheses_depth -= 1
                print(token,j,parentheses_depth)
                #print(parentheses_depth, token)
                j+=1

        
        #First to tackle: un finshed shit string
        if token.startswith("'") or token.startswith('"'):
            if token.startswith("'"):
                if not token.endswith("'"):
                    print(Syntaxerror("Missing a \" ' \" "))
                    terminate(token)
            if token.startswith('"'):
                if not token.endswith('"'):
                    print(Syntaxerror("Missing a ' \" '"))
                    terminate(token)
        i+=1