from ast_classes import VarExpr, NumberExpr, PrintStmt, BinaryExpr , VarDeclStmt, IfStmt, CompareExpr, BlockStmt, WhileStmt, AssignStmt, StringExpr

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
        if self.current.kind == "STRING":
            return self.parse_var_decl_stmt()
        if self.current.kind == "IF":
            return self.parse_if_stmt()
        if self.current.kind == "WHILE":
            return self.parse_while_stmt()
        if self.current.kind == "IDENT":
            return self.parse_assign_stmt()
        
        expr = self.parse_expr()
        self.expect("SEMI")
        return expr
    
    def parse_while_stmt(self):
        """
        WhileStmt  ::= "while" "(" Expr ")" BlockStmt
        """
        self.expect("WHILE")
        self.expect("LPAREN")
        condition = self.parse_expr()
        self.expect("RPAREN")
        body = self.parse_block_stmt()
        return WhileStmt(condition, body)

    def parse_if_stmt(self):
        """
        IfStmt     ::= "if" "(" Expr ")" "{" Statement "}" [ "else" "{" Statement "}" ]
        """
        self.expect("IF")
        self.expect("LPAREN")
        condition = self.parse_expr()
        self.expect("RPAREN")
        true_branch = self.parse_block_stmt()
        if self.current.kind == "ELSE":
            self.expect("ELSE")

            false_branch = self.parse_block_stmt()

            return IfStmt(condition, true_branch, false_branch)
        return IfStmt(condition, true_branch)
    
    def parse_block_stmt(self):
        """
        BlockStmt  ::= Statement { Statement }
        """
        statements = []
        self.expect("LBRACE")
        while self.current.kind != "RBRACE":
            statements.append(self.parse_statment())
        self.expect("RBRACE")
        return BlockStmt(statements)


    def parse_var_decl_stmt(self):
        """
        VarDeclStmt ::= Type Identifier "=" Expr ";"
        """
        var_type = self.current.kind
        if var_type == "INT":
            self.expect("INT")
            var_name = self.expect("IDENT").text
            self.expect("ASSIGN")
            expr = self.parse_expr()
            self.expect("SEMI")
            return VarDeclStmt(var_type, var_name, expr)
        if var_type == "STRING":
            self.expect("STRING")
            var_name = self.expect("IDENT").text
            self.expect("ASSIGN")

            expr = StringExpr(self.expect("STRING_LITERAL").text)
            self.expect("SEMI")
            return VarDeclStmt(var_type, var_name, expr)

    def parse_assign_stmt(self):
        """
        AssignStmt ::= Identifier "=" Expr ";"
        """
        var_name = self.expect("IDENT").text
        self.expect("ASSIGN")
        expr = self.parse_expr()
        self.expect("SEMI")
        return AssignStmt(var_name, expr)

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
        Expr         ::= CompareExpr
        CompareExpr  ::= AddExpr [ CompareOp AddExpr ]
        CompareOp    ::= "==" | "!=" | "<" | "<=" | ">" | ">="
        """
        left = self.parse_add_expr()
        if self.current.kind in ("EQ", "NEQ", "LT", "LEQ", "GT", "GEQ"):
            operator = self.current.text
            self.advance()
            right = self.parse_add_expr()
            return CompareExpr(left, operator, right)
        return left
    
    def parse_add_expr(self):
        """
        AddExpr     ::= Term [ ("+" | "-") Term ]
        """
        left = self.parse_term() 
        while self.current.kind in ("ADD", "SUB"):
            operator = self.current.text
            self.advance()
            right = self.parse_term()
            left = BinaryExpr(operator, left, right) # Left build up until no more addition or substraction
        return left

    def parse_term(self):
        """
        Term        ::= Factor [ ("*" | "/") Factor ]
        """
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
            return VarExpr(token.text)
        if self.current.kind == "LPAREN":
            self.expect("LPAREN")
            expr = self.parse_expr()
            self.expect("RPAREN")
            return expr
        raise SyntaxError(f"Unexpected {self.current}")


