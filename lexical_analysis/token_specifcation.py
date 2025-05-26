
class TokenSpecification():
    def __inint__(self):
        self.token_spec = [
        
        ("NUMBER",   r"\d+"),

        #KEY WORDS
        ("PRINT", r"print\b")

        #BRACETS
        ("LPARENT", r"("),
        ("RPARENT", r")")


        ]