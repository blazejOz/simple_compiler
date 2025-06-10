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

class VarExpr(ASTNode):
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
    
class AssignStmt(ASTNode):
    def __init__(self, var_name, expr):
        self.var_name = var_name
        self.expr = expr
    def __repr__(self):
        return f"AssignStmt({self.var_name}, {self.expr})"

class IfStmt(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"IfStmt({self.condition!r}, {self.then_branch!r}, {self.else_branch!r})"

class WhileStmt(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileStmt({self.condition!r}, {self.body!r})"

class CompareExpr(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"CompareExpr({self.left!r}, '{self.op}', {self.right!r})"

class BlockStmt(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"BlockStmt({self.statements!r})"