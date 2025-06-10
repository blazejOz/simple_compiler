# ast.py
"""
Abstract Syntax Tree Clases
"""
class ASTNode:
    def __repr__(self):
        return f"{self.__class__.__name__}()"

class NumberExpr(ASTNode):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"NumberExpr({self.value})"

class IdentExpr(ASTNode):
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return f"IdentExpr({self.name!r})"

class PrintStmt(ASTNode):
    def __init__(self, expr: NumberExpr):
        self.expr = expr

    def __repr__(self):
        return f"PrintStmt({self.expr})"

class BinaryExpr(ASTNode):
    def __init__(self, operator: str, left, right):
        self.op = operator
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinaryExpr({self.left!r}, '{self.op}', {self.right!r})"
    
class VarDeclStmt(ASTNode):
    def __init__(self, var_name: str, expr):
        self.var_name = var_name
        self.expr = expr

    def __repr__(self):
        return f"VarDeclStmt({self.var_name}, {self.expr})"