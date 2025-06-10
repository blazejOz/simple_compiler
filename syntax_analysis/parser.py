from ast_classes import IdentExpr, NumberExpr, PrintStmt, BinaryExpr , VarDeclStmt

class Parser:
    def __init__(self, tokens):
        self.tokens  = tokens
        self.pos     = 0
        self.current = tokens[0]
        self.asts    = [] #Abstract Syntax Trees

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
        token = self.current
        self.advance()
        return token

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
        if self.current.kind == "INT":
            return self.parse_var_decl_stmt()
        
        expr = self.parse_expr()
        self.expect("SEMI")
        return expr

    def parse_var_decl_stmt(self):
        """
        VarDeclStmt ::= "int" Identifier "=" Expr ";"
        """
        self.expect("INT")
        var_name = self.expect("IDENT").text
        self.expect("ASSIGN")
        expr = self.parse_expr()
        self.expect("SEMI")
        return VarDeclStmt(var_name, expr)

    def parse_print_stmt(self):
        """
        PrintStmt  ::= "print" "(" Expr ")"
        """
        self.expect("PRINT")
        self.expect("LPAREN")
        expr = self.parse_expr()
        self.expect("RPAREN")
        self.expect("SEMI")
        return PrintStmt(expr)

    def parse_expr(self):
        """
        Expr       ::= Term { ("+" | "-") Term }

        for entry 1 + 2 + 3:
        left = BinaryExpr('+', BinaryExpr('+', NumberExpr(1), NumberExpr(2)), NumberExpr(3))
        """
        left = self.parse_term()
        while self.current.kind in ("ADD", "SUB"):
            operator = self.current.text
            self.advance()
            right = self.parse_term()
            left = BinaryExpr(operator, left, right) # Left build up until no more addition or substraction
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current.kind in ("MUL", "DIV"):
            operator = self.current.text
            self.advance()
            right = self.parse_factor()
            left = BinaryExpr(operator, left, right)
        return left

    def parse_factor(self):
        if self.current.kind == "NUMBER":
            token = self.expect("NUMBER")
            return NumberExpr(int(token.text))
        if self.current.kind == "IDENT":
            token = self.expect("IDENT")
            return IdentExpr(token.text)
        if self.current.kind == "LPAREN":
            self.expect("LPAREN")
            expr = self.parse_expr()
            self.expect("RPAREN")
            return expr
        raise SyntaxError(f"Unexpected {self.current}")


