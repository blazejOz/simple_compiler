from ast_classes import AssignStmt, NumberExpr, PrintStmt, BinaryExpr, StringExpr, VarDeclStmt, VarExpr, IfStmt, BlockStmt, CompareExpr, WhileStmt

class IRInstr:
    def __init__(self, op, arg1=None, arg2=None, dest=None):
        self.op   = op      # operator name, e.g. 'add', 'mul', 'param', 'call', 'return'
        self.arg1 = arg1    # first argument
        self.arg2 = arg2    # second argument (if any)
        self.dest  = dest     # result, temp or label
    
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

class IRGenerator:
    """
    Generate Intermediate Representation (IR) from AST nodes.
    This class takes a list of AST nodes and generates a list of IR instructions.
    """
    def __init__(self, asts):
        self.ast_nodes = asts
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
        for node in self.ast_nodes:
            self.gen_node(node)
        return self.ir_list
    
    def gen_node(self, node):
        """
        Generate IR for a single AST node.
        """
        if isinstance(node, PrintStmt):
            self.gen_print(node)
        elif isinstance(node, VarDeclStmt):
            self.gen_var_decl(node)
        elif isinstance(node, IfStmt):
            self.gen_if(node)
        elif isinstance(node, WhileStmt):
            self.gen_while(node)
        elif isinstance(node, AssignStmt):
            self.gen_assign(node)
        else:
            raise NotImplementedError(f"Unimplemented AST : {type(node)}")

    def gen_while(self, node):
        """
        Generate IR for while statement.
        """
        start_label = self.new_label("start")
        end_label = self.new_label("end")
        self.ir_list.append(IRInstr('label', None, None, start_label))
        cond_tmp = self.gen_expr(node.condition)
        self.ir_list.append(IRInstr('if_false', cond_tmp, None, end_label))
        if isinstance(node.body, BlockStmt):
            self.gen_block(node.body)
        self.ir_list.append(IRInstr('goto', None, None, start_label))
        self.ir_list.append(IRInstr('label', None, None, end_label))

    def gen_if(self, node):
        """
        Generate IR for if statement.
        """
        cond_tmp = self.gen_expr(node.condition) #generate IR for condition
        true_label = self.new_label("true")
        false_label = self.new_label("false")
        end_label = self.new_label("end")

        #generate IR for if condition
        self.ir_list.append(IRInstr('if', cond_tmp, None, true_label)) # if condition goto true_label
        self.ir_list.append(IRInstr('goto', None, None, false_label)) # else goto false_label
        self.ir_list.append(IRInstr('label', None, None, true_label)) # true branch label
        #generate IR for true branch
        if isinstance(node.then_branch, BlockStmt):
            self.gen_block(node.then_branch)

        self.ir_list.append(IRInstr('goto', None, None, end_label)) # goto end label
        #generate IR for false branch
        self.ir_list.append(IRInstr('label', None, None, false_label)) # false branch label
        if isinstance(node.else_branch, BlockStmt):
            self.gen_block(node.else_branch)
        self.ir_list.append(IRInstr('label', None, None, end_label)) # end label

    def gen_block(self, node):
        """
        Generate IR for block statement
        """
        for stmt in node.statements:
            self.gen_node(stmt) #generate IR for each statement in block

    def gen_print(self, node):
        """
        Generate IR for print statement"""
        tmp = self.gen_expr(node.expr) #generete IR for expr - print(expr)

        #print parmas:
        self.ir_list.append(IRInstr('param', "fmt")) # fmt - format param for printf
        self.ir_list.append(IRInstr('param', tmp)) # param of what to print
        #call print:
        call_tmp = self.new_label("call")
        self.ir_list.append(IRInstr('call', 'printf', None, call_tmp))

    def gen_var_decl(self, node):
        """
        Generate IR for variable declaration statement
        """
        if node.var_type == 'string':
            expr_tmp = self.gen_expr(node.expr)
            self.ir_list.append(IRInstr('const', node.value, None, node.var_name))
            return
        expr_tmp = self.gen_expr(node.expr)
        self.ir_list.append(IRInstr('store', node.var_name, expr_tmp, None))

    def gen_assign(self, node):
        """
        Generate IR for assignment statement
        """
        expr_tmp = self.gen_expr(node.expr)
        self.ir_list.append(IRInstr('store', node.var_name, expr_tmp, None))

    def gen_expr(self, node):
        """
        Generate IR for expression node.
        """
        if isinstance(node, CompareExpr):
            left = self.gen_expr(node.left)
            right = self.gen_expr(node.right)
            dest = self.new_temp()
            operator_map = {'==':'eq', '!=':'neq', '<':'lt', '>':'gt', '<=':'leq', '>=':'geq'}
            operator = operator_map[node.op]
            self.ir_list.append(IRInstr(operator, left, right, dest))
            return dest
        if isinstance(node, NumberExpr):
            dest  = self.new_temp()
            self.ir_list.append(IRInstr('const', node.value, None, dest))
            return dest
        if isinstance(node, BinaryExpr):
            left = self.gen_expr(node.left)
            right = self.gen_expr(node.right)
            dest = self.new_temp()
            operator_map = {'+':'add', '-':'sub', '*':'mul', '/':'div'}
            operator = operator_map[node.op]
            self.ir_list.append(IRInstr(operator, left, right, dest))
            return dest
        if isinstance(node, VarExpr):
            dest = self.new_temp()
            self.ir_list.append(IRInstr('load', node.name, None, dest))
            return dest
        if isinstance(node, StringExpr):
            dest = self.new_temp()
            self.ir_list.append(IRInstr('const', node.value, None, dest))
            return dest
        
        raise NotImplementedError(f"IR gen for {type(node)} error")
            
