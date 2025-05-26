# ast.py
"""
Abstract Syntax Tree Clases
"""
class NumberExpr:
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"NumberExpr({self.value})"

class PrintStmt:
    def __init__(self, expr: NumberExpr):
        self.expr = expr

    def __repr__(self):
        return f"PrintStmt({self.expr})"
