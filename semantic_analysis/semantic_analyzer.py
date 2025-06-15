from ast_classes import *

class SemanticAnalyzer:
    def __init__(self, asts):
        self.asts = asts
        self.var_symbols = {}

    def analyze(self):
        for node in self.asts:
            self.visit(node)

    def visit(self, node):
        """
        Check for variable decalraction, assignemt, undeclared errors
        """
        if isinstance(node, VarDeclStmt):
            if node.var_name in self.var_symbols:
                raise RuntimeError(f"Redefinition of variable {node.var_name}")
            expr_type = self.guess_type(node.expr)
            if node.var_type != expr_type:
                raise RuntimeError(
                    f"Type mismatch in declaration: variable '{node.var_name}' is '{node.var_type}', but assigned value is '{expr_type}'"
                )
            self.var_symbols[node.var_name] = node.var_type
            self.visit(node.expr)
        elif isinstance(node, AssignStmt):
            if node.var_name not in self.var_symbols:
                raise RuntimeError(f"Assignment to undeclared variable {node.var_name}")
            expected_type = self.var_symbols[node.var_name]
            actual_type = self.guess_type(node.expr)
            if expected_type != actual_type:
                raise RuntimeError(
                    f"Type mismatch: cannot assign {actual_type} to {expected_type} variable '{node.var_name}'"
                )
            self.visit(node.expr)
        elif isinstance(node, VarIdentifier):
            if node.name not in self.var_symbols:
                raise RuntimeError(f"Use of undeclared variable {node.name}")
        elif isinstance(node, PrintStmt):
            self.visit(node.expr)
        elif isinstance(node, BinaryExpr):
            self.visit(node.left)
            self.visit(node.right)
        elif isinstance(node, CompareExpr):
            self.visit(node.left)
            self.visit(node.right)
        elif isinstance(node, NumberExpr) or isinstance(node, StringExpr):
            pass
        elif isinstance(node, IfStmt):
            self.visit(node.condition)
            self.visit(node.then_branch)
            if node.else_branch:
                self.visit(node.else_branch)
        elif isinstance(node, BlockStmt):
            for stmt in node.statements:
                self.visit(stmt)

    def guess_type(self, expr):
        if isinstance(expr, NumberExpr):
            return "INT"
        elif isinstance(expr, StringExpr):
            return "STRING"
        elif isinstance(expr, VarIdentifier):
            return self.var_symbols.get(expr.name, None)
        return None
