import os
from colorama import Style, Back, Fore, init
init()
class Syntaxerror:
    def __init__(self, msg):
        self.msg = msg
    def __repr__(self):
        return Fore.RED + f'Syntax error  -> {self.msg}!' + Style.RESET_ALL
class Extensionerror:
    def __init__(self, filename, msg):
        self.filename = filename
        self.msg = msg
    def __repr__(self):
        return Fore.RED + f'File extension error for file: {self.filename}, expected extension: ".bwt" -> {self.msg}!' + Style.RESET_ALL
class Miscerror:
    def __init__(self, msg):
        self.msg = msg
    def __repr__(self):
        return Fore.RED + f'Misc error  -> {self.msg}!' + Style.RESET_ALL
def terminate(token):
    print(Fore.YELLOW + f"On token: [ {token} ]" + Style.RESET_ALL)
    os._exit(1)