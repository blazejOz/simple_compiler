import re
from lexical_analysis.token_specification import TokenSpecification
from lexical_analysis.token import Token

class Lexer():
    def __init__(self, src: str):
       self.src = src
       self.tokens = []

    def tokenize(self):
        master_pattern = re.compile(
            "|".join(f"(?P<{name}>{pat})" for name, pat in TokenSpecification.spec)
            )
        
        line = 1
        col = 1
        for match in re.finditer(master_pattern, self.src):
            kind = match.lastgroup # matched group
            value = match.group() # value captured
            if kind == "SKIP":
                col += len(value)
                line += value.count("\n")
                continue
            if kind == "MISMATCH":
                raise RuntimeError(f"Nieczekiwany {value!r} na {line}:{col}")
            
            tok = Token(kind, value, line, col)
            self.tokens.append(tok)
            col += len(value)

        self.tokens.append(Token("EOF", "", line, col))
        return self.tokens
