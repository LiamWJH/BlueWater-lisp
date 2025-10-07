from cli import getcliargs
from lexer import tokenize
from parser import parse
from runtime import evaluate
from errors import Syntaxerror, Extensionerror, Miscerror, terminate
from checker import check
USERCODE = getcliargs()

src = []
for raw_line in USERCODE.splitlines():
    code = raw_line.split(";", 1)[0]
    if code.strip():
        src.append(code)

tokens = tokenize("\n".join(src))
check(tokens)

wholetoken = []
while tokens:
    wholetoken.append(parse(tokens))

for action in wholetoken:
    evaluate(action)