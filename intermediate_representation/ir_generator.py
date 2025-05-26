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

    def new_temp(self):
        self.temp_id += 1
        return f"t{self.temp_id}"

    def new_label(self, base="L"):  
        self.label_id += 1
        return f"{base}{self.label_id}"

    def gen(self):
        for node in self.asts:    
            if isinstance(node, PrintStmt):
                self.gen_print(node)
            else:
                raise NotImplementedError(f"IR gen for {type(node)} not supported yet")
            return self.instrs

    def gen_print(self, node: PrintStmt):
        # generate IR for expression
        tmp = self.gen_expr(node.expr)
        # push parameters (example IR)
        self.instrs.append(IRInstr('param', 'fmt'))
        self.instrs.append(IRInstr('param', tmp))
        # call printf
        self.instrs.append(IRInstr('call', 'printf', None, f"tcall{self.new_label()}") )

    def gen_expr(self, expr):
        if isinstance(expr, NumberExpr):
            tmp = self.new_temp()
            self.instrs.append(IRInstr('const', expr.value, None, tmp))
            return tmp
        else:
            raise NotImplementedError(f"IR gen for {type(expr)} not supported yet")