from ast_classes import *

class SemanticAnalyzer:
    def __init__(self, asts):
        self.asts = asts
        self.var_symbols = {}
        self.errors = []
    
    def analyze(self):
        for node in self.asts:
            self.visit(node)
        if self.errors:
            print("SEMANTIC ERRORS:")
            for err in self.errors:
                print("  ", err)
            raise RuntimeError("Semantic analysis failed!")

    def visit(self, node):
        if isinstance(node, VarDeclStmt):
            if node.var_name in self.var_symbols:
                self.errors.append(f"Redefinition of variable {node.var_name}")
            self.var_symbols[node.var_name] = node.var_type
            self.visit(node.expr)
        elif isinstance(node, AssignStmt):
            if node.var_name not in self.var_symbols:
                self.errors.append(f"Assignment to undeclared variable {node.var_name}")
            self.visit(node.expr)
        elif isinstance(node, VarExpr):
            if node.name not in self.var_symbols:
                self.errors.append(f"Use of undeclared variable {node.name}")
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