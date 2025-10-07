class Sytaxerror:
    def __inti__(self, line, msg):
        self.line = line
        self.msg = msg
    def __repr__(self):
        return f'Syntax error on line{self.line} -> "{self.msg}!"'
class Extensionerror:
    def __inti__(self, filename, fileext, msg):
        self.filename = filename
        self.fileext = fileext
        self.msg = msg
    def __repr__(self):
        return f'File extension error for file: {self.filename}, expected file: {self.fileext} -> "{self.msg}!"'
class Miscerror:
    def __inti__(self, line, msg):
        self.line = line
        self.msg = msg
    def __repr__(self):
        return f'Misc error on line{self.line} -> "{self.msg}!"'