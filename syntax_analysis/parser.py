from ast_classes import NumberExpr, PrintStmt

class Parser:
    def __init__(self, tokens):
        self.tokens  = tokens
        self.pos     = 0
        self.cur     = tokens[0]

    def parse(self):
        stmts = []
        while self.cur.kind != "EOF":
            stmts.append(self.parse_print_stmt()) 
        self.expect("EOF")
        return stmts

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.cur = self.tokens[self.pos]
    
    def expect(self, kind):
        if self.cur.kind != kind:
            raise SyntaxError(f"Expected {kind}, got {self.cur.kind} at {self.cur.line}:{self.cur.col}")
        tok = self.cur
        self.advance()
        return tok

    def parse_print_stmt(self):
        self.expect("PRINT")
        self.expect("LPAREN")
        num = self.expect("NUMBER")
        self.expect("RPAREN")
        return PrintStmt(NumberExpr(int(num.text)))