
class TokenSpecification():
    
    spec = [
        #KEY WORDS
        ("PRINT", r"print\b"),
        ("INT",   r"int\b"),

        # IDENTIFIERS
        ("IDENT", r"[a-zA-Z_][a-zA-Z0-9_]*"), # variable names, function names, etc

        #LITERALS
        ("NUMBER", r"\d+"),  # integer

        #PUNCTUATION
        ("SEMI", r";"),
        ("ASSIGN", r"="),

        #BRACETS
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),

        #MATH OPERATORS
        ("ADD", r"\+"),
        ("SUB", r"-"),
        ("MUL", r"\*"),
        ("DIV", r"/"),

        ("SKIP", r"[ \t\n]+"), #skip tabs, space, newline
        ("MISMATCH", r"."), #other - error catch (needs to be last)

        ]