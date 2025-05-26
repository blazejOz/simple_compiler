
class TokenSpecification():
    
    spec = [
        #KEY WORDS
        ("PRINT", r"print\b"),

        ("NUMBER",   r"\d+"),

        #BRACETS
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),

        ("SKIP", r"[ \t\n]+"), #skip tabs, space, newline
        ("MISMATCH", r"."), #other - error catch

        ]