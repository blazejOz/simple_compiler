
class TokenSpecification():
    
    spec = [
        #KEY WORDS
        ("PRINT", r"print\b"),

        ("NUMBER",   r"\d+"),

        #BRACETS
        ("LPARENT", r"\("),
        ("RPARENT", r"\)"),

        ("SKIP", r"[ \t\n]+"), #skip tabs, space, newline
        ("MISSMATCH", r"."), #other - error catch

        ]