import re
from lexical_analysis.token_specification import TokenSpecification

class Lexer():
    def __init__(self, src: str):
       self.src = src
       self.tokens = []

    def tokenize(self):
        master_pattern = re.compile(
            "|".join(f"(?P<{name}>{pat})" for name, pat in TokenSpecification.spec)
            )
        
        print(master_pattern)


lexer = Lexer("nothing")
lexer.tokenize()