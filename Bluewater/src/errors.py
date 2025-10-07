class Error_:
    def __init__(self, line, col, char, msg):
        self.line = line
        self.col = col
        self.char = char
        self.msg = msg


class Syntaxerror_(Error_):
    def __init__(self, line, col, char, msg):
        super().__init__(line, col, char, msg)
    def __repr__(self):
        return f"[STDERR]: |Syntax error| on line {self.line} column {self.col} char {self.char}...\n NOTE -> {self.msg}!"
class Nofileerror_(Error_):
    def __init__(self, filename, msg):
        super().__init__(filename)
    def __repr__(self):
        return f"[STDERR]: |No file error| File {self.filename} does not exist...\n NOTE -> {self.msg}!"
class Wrongexterror_(Error_):
    def __init__(self, filename, ext, msg):
        super().__init__(filename, ext, msg)
    def __repr__(self):
        return f"[STDERR]: |Wrong extension error| Wrong file extension for file {self.filename} of ext {self.ext}...\n NOTE -> {self.msg}!"
class Expectancyerror_(Error_):
    def __init__(self, line, expected, got, msg):
        super().__init__(line, expected, got, msg)
    def __repr__(self):
        return f"[STDERR]: |Expectancy error| on line {self.line} expected data type {self.expected} but got {self.got}...\n NOTE -> {self.msg}!"
class Novalerror_(Error_):
    def __init__(self, line, col, char, msg):
        super().__init__(line, col, char, msg)
    def __repr__(self):
        return f"[STDERR]: |No value error| on line {self.line} column {self.col} char {self.char}...\n NOTE -> {self.msg}!"
    