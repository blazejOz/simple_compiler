class IRInstr:
    def __init__(self, op, arg1=None, arg2=None, dest=None):
        self.op   = op      # operator name, e.g. 'add', 'mul', 'param', 'call', 'return'
        self.arg1 = arg1    # first argument
        self.arg2 = arg2    # second argument (if any)
        self.dest  = dest   # result, temp or label
    
    def __repr__(self):
        if self.op == "label":
            return f"{self.dest}:"
        if self.op == "goto":
            return f"goto {self.dest}"
        if self.op == "if_false":
            return f"if_false {self.arg1} goto {self.dest}"
        if self.op == "if":
            return f"if {self.arg1} goto {self.dest}"
        if self.op == "store":
            return f"store {self.arg1} {self.arg2}"
        if self.op == "store_str":
            return f"store_str {self.arg1} {self.arg2}"
        if self.op == "load":
            return f"{self.dest} = load {self.arg1}"
        if self.op == "const":
            return f"{self.dest} = const {self.arg1}"
        if self.op == "param":
            return f"param {self.arg1}"
        if self.op == "call":
            return f"{self.dest} = call {self.arg1}"
        if self.op in {"add", "sub", "mul", "div", "eq", "neq", "lt", "gt", "leq", "geq"}:
            return f"{self.dest} = {self.op} {self.arg1} {self.arg2}"
        return f"{self.op} {self.arg1 or ''} {self.arg2 or ''} {self.dest or ''}"
    
    def full_str(self):
        """
        Return full string representation of the instruction.
        """
        return f"{self.op} {self.arg1 or 'none'} {self.arg2 or 'none'} {self.dest or 'none'}".strip()