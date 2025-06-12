from intermediate_representation.ir_instruction import IRInstr

class IROptimizer:
    def __init__(self, ir_list):
        self.ir_list = ir_list

    def optimize(self):
        # Implement optimization passes
        self.constant_folding()
        self.dead_code_elimination()
        return self.ir_list

    def constant_folding(self):
        """
        Perform constant folding optimization on the IR code.
        This optimization replaces constant expressions with their computed values.
        """
        constants = {}
        new_ir_code = []
        for instr in self.ir_list:
            if instr.op == 'const':
                constants[instr.dest] = instr.arg1
                new_ir_code.append(instr)
            elif instr.op in {'add', 'sub', 'mul', 'div'}:
                x = constants.get(instr.arg1)
                y = constants.get(instr.arg2)
                if x is not None and y is not None:
                    # Fold constant expression
                    if instr.op == 'add':
                        result = x + y
                    elif instr.op == 'sub':
                        result = x - y
                    elif instr.op == 'mul':
                        result = x * y
                    elif instr.op == 'div':
                        if y == 0:
                            raise ZeroDivisionError("Division by zero in constant folding")
                        result = x / y
                    
                    # Create a new instruction with the folded constant
                    new_instr = IRInstr('const', result, None, instr.dest)
                    constants[instr.dest] = result
                    new_ir_code.append(new_instr)
                else:
                    new_ir_code.append(instr)
            else:
                new_ir_code.append(instr)
        self.ir_list = new_ir_code
            

    def dead_code_elimination(self):
        """
        Perform dead code elimination optimization on the IR code.
        """
        used_dests = set()
        # collect all destinations that are used in args
        for instr in self.ir_list:
            for arg in (instr.arg1, instr.arg2):
                if isinstance(arg, str) and arg.startswith('t'):
                    used_dests.add(arg)
        
        new_ir_code = []
        # filter out indtructions not in used_dests
        for instr in self.ir_list:
            if instr.op in ("const", "add", "sub", "mul", "div"):
                if instr.dest in used_dests:
                    new_ir_code.append(instr)
            else:
                new_ir_code.append(instr)
        self.ir_list = new_ir_code
            