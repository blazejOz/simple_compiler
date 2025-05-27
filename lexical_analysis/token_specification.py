
class TokenSpecification():
    
    spec = [
        #KEY WORDS
        ("PRINT", r"print\b"),

        ("NUMBER",   r"\d+"),

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