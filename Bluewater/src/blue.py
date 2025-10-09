import time, gc
from cli import getcliargs
from lexer import tokenize
from parser import parse
from runtime import evaluate

# --- prep program once ---
USERCODE = getcliargs()
src = []
for raw_line in USERCODE.splitlines():
    code = raw_line.split(";", 1)[0]
    if code.strip():
        src.append(code)

tokens = tokenize("\n".join(src))
wholetoken = []
while tokens:
    wholetoken.append(parse(tokens))

for action in wholetoken:
    evaluate(action)
