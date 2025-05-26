class Token:
    def __init__(self, kind: str, text: str, line: int, col: int):
        self.kind = kind    # np. "NUMBER", "PRINT"
        self.text = text
        self.line = line
        self.col  = col
    def __repr__(self):
        return f"{self.kind}({self.text!r})@{self.line}:{self.col}"