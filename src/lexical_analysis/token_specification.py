
class TokenSpecification():
    
    spec = [
        #KEY WORDS
        ("PRINT", r"print\b"),
        ("INT",   r"int\b"),
        ("STRING", r"str\b"),
        ("IF",    r"if\b"),
        ("ELSE",  r"else\b"),
        ("WHILE", r"while\b"),

        # IDENTIFIERS
        ("IDENT", r"[a-zA-Z_][a-zA-Z0-9_]*"), # variable names, function names, etc

        #LITERALS
        ("NUMBER", r"-?\d+"),  # integer (supports optional leading minus for negatives)
        ("STRING_LITERAL", r'"[^"]*"'),  # string literal (double quotes)

        #COMPARISON OPERATORS
        ("EQ", r"=="),
        ("NEQ", r"!="),
        ("LEQ", r"<="),
        ("GEQ", r">="),
        ("LT", r"<"),
        ("GT", r">"),

        #PUNCTUATION
        ("SEMI", r";"),
        ("ASSIGN", r"="),

        #BRACETS
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("LBRACE", r"\{"),
        ("RBRACE", r"\}"),

        #MATH OPERATORS
        ("ADD", r"\+"),
        ("SUB", r"-"),
        ("MUL", r"\*"),
        ("DIV", r"/"),

        ("COMMENT", r"#[^\n]*"),
        ("NEWLINE", r"\n"),

        ("SKIP", r"[ \t]+"), #skip tabs, whitespace
        ("MISMATCH", r"."), #other - error catch (needs to be last)

        ]