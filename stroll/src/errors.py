import os
from colorama import Style, Fore, init
init(autoreset=True)


# Legacy error classes (old system)
# Kept so old code does not break.


class Syntaxerror:
    def __init__(self, msg):
        self.msg = msg
    def __repr__(self):
        return Fore.RED + f'Syntax error -> {self.msg}!' + Style.RESET_ALL

class Extensionerror:
    def __init__(self, filename, msg):
        self.filename = filename
        self.msg = msg
    def __repr__(self):
        return (
            Fore.RED +
            f'File extension error for: {self.filename}, expected .bwt -> {self.msg}!'
            + Style.RESET_ALL
        )

class Miscerror:
    def __init__(self, msg):
        self.msg = msg
    def __repr__(self):
        return Fore.RED + f'Misc error -> {self.msg}!' + Style.RESET_ALL



# New improved error system
# Real Python exceptions with
# optional line/column/token info.


class StrollError(Exception):
    def __init__(self, message, *, line=None, column=None, filename=None, token=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.filename = filename
        self.token = token

    def __str__(self):
        text = Fore.RED + f"{self.__class__.__name__}: {self.message}"
        # Show position info if available
        if self.line is not None:
            text += f" (line {self.line}"
            if self.column is not None:
                text += f", col {self.column}"
            text += ")"
        # Show token if available
        if self.token:
            text += f" [token: {self.token}]"
        return text + Style.RESET_ALL

    __repr__ = __str__


# Simple subclasses so we can distinguish types of errors
class SyntaxErrorStroll(StrollError): pass
class ExtensionErrorStroll(StrollError): pass
class MiscErrorStroll(StrollError): pass
class NameErrorStroll(StrollError): pass
class TypeErrorStroll(StrollError): pass
class ArgumentErrorStroll(StrollError): pass
class RuntimeErrorStroll(StrollError): pass



# Helper to raise syntax errors
# Parser/runtime can call this.


def raise_syntax(message, token=None, *, filename=None):
    line = getattr(token, "line", None)
    col = getattr(token, "column", None)
    val = getattr(token, "value", token)
    raise SyntaxErrorStroll(
        message,
        line=line,
        column=col,
        filename=filename,
        token=val
    )


# Old terminate() function
# Still kept for compatibility.


def terminate(token):
    print(Fore.YELLOW + f"On token: [ {token} ]" + Style.RESET_ALL)
    os._exit(1)
