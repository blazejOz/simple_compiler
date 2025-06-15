from ast_classes import *
from intermediate_representation.ir_instruction import IRInstr

class IRGenerator:
    """
    Generate Intermediate Representation (IR) from AST nodes.
    Tracks variable types for print/assignment of string or int.
    """
    def __init__(self, asts):
        self.ast_nodes = asts
        self.temp_id  = 0
        self.label_id = 0
        self.ir_list = []
        self.var_symbols = {}

    def new_temp(self):
        self.temp_id += 1
        return "t" + str(self.temp_id)

    def new_label(self, name="L"):
        self.label_id += 1
        return name + str(self.label_id)

    def get_var_type(self, name):
        typ = self.var_symbols.get(name)
        if typ is None:
            raise RuntimeError(f"Unknown variable '{name}'")
        return typ

    def gen(self):
        for node in self.ast_nodes:
            self.gen_node(node)
        return self.ir_list

    def gen_node(self, node):
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
        cond_tmp = self.gen_expr(node.condition)
        true_label = self.new_label("true")
        false_label = self.new_label("false")
        end_label = self.new_label("end")
        self.ir_list.append(IRInstr('if', cond_tmp, None, true_label))
        self.ir_list.append(IRInstr('goto', None, None, false_label))
        self.ir_list.append(IRInstr('label', None, None, true_label))
        if isinstance(node.then_branch, BlockStmt):
            self.gen_block(node.then_branch)
        self.ir_list.append(IRInstr('goto', None, None, end_label))
        self.ir_list.append(IRInstr('label', None, None, false_label))
        if isinstance(node.else_branch, BlockStmt):
            self.gen_block(node.else_branch)
        self.ir_list.append(IRInstr('label', None, None, end_label))

    def gen_block(self, node):
        for stmt in node.statements:
            self.gen_node(stmt)

    def gen_print(self, node):
        expr = node.expr
        if isinstance(expr, NumberExpr):
            tmp = self.gen_expr(expr)
            self.ir_list.append(IRInstr('param', "fmt_int"))
            self.ir_list.append(IRInstr('param', tmp))
        elif isinstance(expr, StringExpr):
            tmp = self.gen_expr(expr)
            self.ir_list.append(IRInstr('param', "fmt_str"))
            self.ir_list.append(IRInstr('param', tmp))
        elif isinstance(expr, VarExpr):
            typ = self.get_var_type(expr.name)
            if typ == "STRING":
                self.ir_list.append(IRInstr('param', "fmt_str"))
                self.ir_list.append(IRInstr('param', expr.name))
            else:
                tmp = self.gen_expr(expr)
                self.ir_list.append(IRInstr('param', "fmt_int"))
                self.ir_list.append(IRInstr('param', tmp))
        else:
            raise NotImplementedError("print only supports numbers, variables, or strings")
        call_tmp = self.new_label("call")
        self.ir_list.append(IRInstr('call', 'printf', None, call_tmp))

    def gen_var_decl(self, node):
        # node.var_type must be 'INT' or 'STRING'
        self.var_symbols[node.var_name] = node.var_type
        if node.var_type == 'STRING':
            string_val = self.get_string_val(node.expr)
            self.ir_list.append(IRInstr('store_str', node.var_name, string_val , None))
            return
        expr_tmp = self.gen_expr(node.expr)
        self.ir_list.append(IRInstr('store', node.var_name, expr_tmp, None))

    def gen_assign(self, node):
        typ = self.get_var_type(node.var_name)
        expr_tmp = self.gen_expr(node.expr)
        if typ == "STRING":
            self.ir_list.append(IRInstr('store_str', node.var_name, expr_tmp, None))
        else:
            self.ir_list.append(IRInstr('store', node.var_name, expr_tmp, None))

    def gen_expr(self, node):
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
            typ = self.get_var_type(node.name)
            dest = self.new_temp()
            self.ir_list.append(IRInstr('load', node.name, None, dest))
            return dest
        if isinstance(node, StringExpr):
            string_name = self.new_label("str")
            self.ir_list.append(IRInstr('store_str', string_name , node.value, None, ))
            return string_name
        raise NotImplementedError(f"IR gen for {type(node)} error")
    
    def get_string_val(self, node):
        if isinstance(node, StringExpr):
            string_value = node.value
            return string_value
        raise NotImplementedError(f"IR gen for string {type(node)} error")