# syntax_analysis/parser.py

from ast_classes import NumberExpr, PrintStmt, BinaryExpr

class Parser:
    def __init__(self, tokens):
        self.tokens  = tokens
        self.pos     = 0
        self.current = tokens[0]
        self.asts = [] #Abstract Syntax Trees

    def advance(self):
        """move to the next token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]

    def expect(self, kind):
        """check expected token, raise error or advance"""
        if self.current.kind != kind:
            raise SyntaxError(
                f"Expected {kind}, got {self.current.kind} "
                f"at {self.current.line}:{self.current.col}"
            )
        tok = self.current
        self.advance()
        return tok

    def parse(self):
        while self.current.kind != "EOF":
            self.asts.append(self.parse_statment())
        self.expect("EOF")
        return self.asts

    def parse_statment(self):
        """
        Statement  ::= PrintStmt | ExprStmt
        """
        if self.current.kind == "PRINT":
            return self.parse_print_stmt()
        ### ADD MORE HERE
        else:
            return self.parse_expr()







    def parse_print_stmt(self):
        self.expect("PRINT")
        self.expect("LPAREN")
        expr = self.parse_expr()
        self.expect("RPAREN")
        return PrintStmt(expr)

    def parse_expr(self):
        # handles addition: Expr ::= Factor { ADD Factor }
        left = self.parse_factor()
        while self.current.kind in ("ADD", "SUB"):
            op_tok = self.current
            right  = self.parse_factor()
            left   = BinaryExpr(op_tok.text, left, right)
        return left

    def parse_factor(self):
        # handles numbers and parenthesized sub-expressions
        if self.current.kind == "NUMBER":
            tok = self.expect("NUMBER")
            return NumberExpr(int(tok.text))
        if self.current.kind == "LPAREN":
            self.expect("LPAREN")
            node = self.parse_expr()
            self.expect("RPAREN")
            return node
        raise SyntaxError(
            f"Unexpected {self.current.kind} at {self.current.line}:{self.current.col}"
        )
