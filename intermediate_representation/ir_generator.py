from ast_classes import NumberExpr, PrintStmt, BinaryExpr, VarDeclStmt, VarExpr

class IRInstr:
    def __init__(self, op, arg1=None, arg2=None, res=None):
        self.op   = op      # operator name, e.g. 'add', 'mul', 'param', 'call', 'return'
        self.arg1 = arg1    # first argument
        self.arg2 = arg2    # second argument (if any)
        self.res  = res     # result temp or label
    def __repr__(self):
        return f"{self.res or ''} = {self.op} {self.arg1 or ''} {self.arg2 or ''}" if self.res else f"{self.op} {self.arg1 or ''} {self.arg2 or ''}"

class IRGenerator:
    """
    
    """
    def __init__(self, asts):
        self.asts = asts
        self.temp_id  = 0
        self.label_id = 0
        self.ir_list = []

    def new_temp(self):
        """generete new temporrary variable"""
        self.temp_id += 1
        return "t" + str(self.temp_id)

    def new_label(self, name="L"):
        """ genereate new label"""
        self.label_id += 1
        return name + str(self.label_id)

    def gen(self):
        for node in self.asts:
            if isinstance(node, PrintStmt):
                self.gen_print(node)
            elif isinstance(node, VarDeclStmt):
                self.gen_var_decl(node)
            else:
                raise NotImplementedError(f"Nieobslugiwany AST: {type(node)}")
        return self.ir_list
    
    def gen_print(self, node):
        tmp = self.gen_expr(node.expr) #generete IR for expr - print(expr)

        #print parmas:
        self.ir_list.append(IRInstr('param', "fmt")) # fmt - format param for printf
        self.ir_list.append(IRInstr('param', tmp)) # param of what to print
        #call print:
        call_tmp = self.new_label("call")
        self.ir_list.append(IRInstr('call', 'printf', None, call_tmp))

    def gen_var_decl(self, node):
        expr_tmp = self.gen_expr(node.expr)
        self.ir_list.append(IRInstr('store', node.var_name, expr_tmp, None))

    def gen_expr(self, node):
        if isinstance(node, NumberExpr):
            temp  = self.new_temp()
            self.ir_list.append(IRInstr('const', node.value, None, temp))
            return temp
        if isinstance(node, BinaryExpr):
            left = self.gen_expr(node.left)
            right = self.gen_expr(node.right)
            res = self.new_temp()
            operator_map = {'+':'add', '-':'sub', '*':'mul', '/':'div'}
            operator = operator_map[node.op]
            self.ir_list.append(IRInstr(operator, left, right, res))
            return res
        if isinstance(node, VarExpr):
            temp = self.new_temp()
            self.ir_list.append(IRInstr('load', node.name, None, temp))
            return temp
        
        raise NotImplementedError(f"IR gen for {type(node)} error")
            
