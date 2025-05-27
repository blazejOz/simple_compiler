# code_generator/ir_generator.py
# Skeleton for IR generation

from ast_classes import NumberExpr, PrintStmt

class IRInstr:
    def __init__(self, op, arg1=None, arg2=None, res=None):
        self.op   = op      # operator name, e.g. 'add', 'mul', 'param', 'call', 'return'
        self.arg1 = arg1    # first argument
        self.arg2 = arg2    # second argument (if any)
        self.res  = res     # result temp or label
    def __repr__(self):
        return f"{self.res or ''} = {self.op} {self.arg1 or ''} {self.arg2 or ''}" if self.res else f"{self.op} {self.arg1 or ''} {self.arg2 or ''}"

class IRGenerator:
    def __init__(self, asts):
        self.asts = asts
        self.temp_id  = 0
        self.label_id = 0
        self.instrs = []

    