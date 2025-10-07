import os
from colorama import Style, Back, Fore, init
init()
class Sytaxerror:
    def __init__(self, line, msg):
        self.line = line
        self.msg = msg
    def __repr__(self):
        return Fore.RED + f'Syntax error on line{self.line} -> "{self.msg}!"' + Style.RESET_ALL
class Extensionerror:
    def __init__(self, filename, msg):
        self.filename = filename
        self.msg = msg
    def __repr__(self):
        return Fore.RED + f'File extension error for file: {self.filename}, expected extension: ".bwt" -> "{self.msg}!"' + Style.RESET_ALL
class Miscerror:
    def __init__(self, line, msg):
        self.line = line
        self.msg = msg
    def __repr__(self):
        return Fore.RED + f'Misc error on line{self.line} -> "{self.msg}!"' + Style.RESET_ALL
def terminate():
    os._exit(1)