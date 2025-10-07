from cli import getcliargs
from lexer import tokenize
from parser import parse
from runtime import evaluate

USERCODE = getcliargs()

src = []
for raw_line in USERCODE.splitlines():
    code = raw_line.split(";", 1)[0]
    if code.strip():
        src.append(code)

tokens = tokenize("\n".join(src))

ast = []
while tokens:
    ast.append(parse(tokens))

for action in ast:
    evaluate(action)