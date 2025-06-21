
class AsmGenerator:
    # Temporary registers for x86-64
    TEMP_REGS = ["rdx", "rcx", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"] 

    def __init__(self, ir_list):
        self.ir_list = ir_list
        self.ir_list_index = 0
        self.asm = []
        self.free_regs = set(self.TEMP_REGS) 
        self.temp_to_reg = {} # Map temporary variables to registers
        self.param_queue = [] # Queue for parameters for printf
        self.string_vars = {} # Store string variables for .data section

    
    def gen(self):
        """
        Generate assembly code from the intermediate representation (IR) list.
        """
        self.collect_strings()
        self.gen_header()
        for instr in self.ir_list:
            self.gen_emit(instr)
            self.ir_list_index += 1
        self.gen_footer()
        return "\n".join(self.asm)

    def gen_emit(self, instr):
        handler = getattr(self, f"emit_{instr.op}", None)
        if handler:
            handler(instr)
        else:
            raise NotImplementedError(f"Unsupported IR: {instr.op}")
    
    def gen_header(self):
        self.asm.append("section .data")
        self.asm.append('    fmt_int: db "%d", 10, 0')
        self.asm.append('    fmt_str: db "%s", 10, 0')
        # Add string variables to the .data section
        for name, value in self.string_vars.items():
            self.asm.append(f'    {name}: db {value}, 0')
        self.asm.append("")
        self.asm.append("section .bss")
        # Allocate space for variables in the .bss section
        for var in self.collect_vars():
            if var not in self.string_vars:
                self.asm.append(f"    {var}: resq 1")
        self.asm.append("")
        self.asm.append("section .text")
        self.asm.append("    global main")
        self.asm.append("    extern printf")
        self.asm.append("")
        self.asm.append("main:")

    def gen_footer(self):
        self.asm.append("    mov rax, 0")
        self.asm.append("    ret")
    
    def collect_strings(self):
        for instr in self.ir_list:
            if instr.op == "store_str":
                self.string_vars[instr.arg1] = instr.arg2

    def collect_vars(self):
        vars = set()
        for instr in self.ir_list:
            if instr.op == "store":
                vars.add(instr.arg1)
            if instr.op == "load":
                vars.add(instr.arg1)
        return vars
    
    def reg_byte(self, reg):
        # Map 64-bit register to its 8-bit version for set* instructions
        mapping = {
            "rax": "al", "rbx": "bl", "rcx": "cl", "rdx": "dl",
            "rsi": "sil", "rdi": "dil",
            "rbp": "bpl", "rsp": "spl",
            "r8": "r8b", "r9": "r9b", "r10": "r10b", "r11": "r11b",
            "r12": "r12b", "r13": "r13b", "r14": "r14b", "r15": "r15b"
        }
        return mapping.get(reg, reg)
    
    def allocate_reg(self, temp):
        """
        Allocate a register for a temporary variable.
        """
        if temp not in self.temp_to_reg:
            if not self.free_regs:
                raise RuntimeError("Ran out of temp registers!")
            reg = self.free_regs.pop()
            self.temp_to_reg[temp] = reg
        return self.temp_to_reg[temp]
    
    def deallocate_reg(self, temp):
        """
        Deallocate a register for a temporary variable.
        """
        if temp in self.temp_to_reg:
            reg = self.temp_to_reg[temp]
            self.free_regs.add(reg)
            del self.temp_to_reg[temp]
    
    def is_temp_used_later(self, temp):
        """
        Check if a temporary variable is used later in the IR list.
        """
        for instr in self.ir_list[self.ir_list_index+1:]:
            if instr.dest == temp or instr.arg1 == temp or instr.arg2 == temp:
                return True
        return False

    ### Assembly Code Generation Methods ###
    def emit_label(self, instr):
        self.asm.append(f"{instr.dest}:")

    def emit_goto(self, instr):
        self.asm.append(f"    jmp {instr.dest}")

    def emit_if(self, instr):
        reg = self.temp_to_reg[instr.arg1]
        self.asm.append(f"    cmp {reg}, 0")
        self.asm.append(f"    jne {instr.dest}")

    def emit_if_false(self, instr):
        reg = self.temp_to_reg[instr.arg1]
        self.asm.append(f"    cmp {reg}, 0")
        self.asm.append(f"    je {instr.dest}")

    def emit_store(self, instr):
        reg = self.temp_to_reg[instr.arg2]
        self.asm.append(f"    mov [{instr.arg1}], {reg}")

    def emit_store_str(self, instr):
        # Already handled in .data
        pass

    def emit_load(self, instr):
        reg = self.allocate_reg(instr.dest)
        self.asm.append(f"    mov {reg}, [{instr.arg1}]")

    def emit_const(self, instr):
        reg = self.allocate_reg(instr.dest)
        self.asm.append(f"    mov {reg}, {instr.arg1}")

    def emit_add(self, instr):
        reg1 = self.temp_to_reg[instr.arg1]
        reg2 = self.temp_to_reg[instr.arg2]
        reg_res = self.allocate_reg(instr.dest)
        self.asm.append(f"    mov {reg_res}, {reg1}")
        self.asm.append(f"    add {reg_res}, {reg2}")
        #delocate reg if not used later
        if not self.is_temp_used_later(instr.arg1):
            self.deallocate_reg(instr.arg1)
        if not self.is_temp_used_later(instr.arg2):
            self.deallocate_reg(instr.arg2)

    def emit_sub(self, instr):
        reg1 = self.temp_to_reg[instr.arg1]
        reg2 = self.temp_to_reg[instr.arg2]
        reg_res = self.allocate_reg(instr.dest)
        self.asm.append(f"    mov {reg_res}, {reg1}")
        self.asm.append(f"    sub {reg_res}, {reg2}")
        #delocate reg if not used later
        if not self.is_temp_used_later(instr.arg1):
            self.deallocate_reg(instr.arg1)
        if not self.is_temp_used_later(instr.arg2):
            self.deallocate_reg(instr.arg2)

    def emit_mul(self, instr):
        reg1 = self.temp_to_reg[instr.arg1]
        reg2 = self.temp_to_reg[instr.arg2]
        reg_res = self.allocate_reg(instr.dest)
        self.asm.append(f"    mov {reg_res}, {reg1}")
        self.asm.append(f"    imul {reg_res}, {reg2}")
        #delocate reg if not used later
        if not self.is_temp_used_later(instr.arg1):
            self.deallocate_reg(instr.arg1)
        if not self.is_temp_used_later(instr.arg2):
            self.deallocate_reg(instr.arg2)

    def emit_div(self, instr):
        reg1 = self.temp_to_reg[instr.arg1]
        reg2 = self.temp_to_reg[instr.arg2]
        reg_res = self.allocate_reg(instr.dest)
        self.asm.append(f"    mov rax, {reg1}")
        self.asm.append(f"    cqo")
        self.asm.append(f"    idiv {reg2}")
        self.asm.append(f"    mov {reg_res}, rax")
        #delocate reg if not used later
        if not self.is_temp_used_later(instr.arg1):
            self.deallocate_reg(instr.arg1)
        if not self.is_temp_used_later(instr.arg2):
            self.deallocate_reg(instr.arg2)

    def emit_gt(self, instr):
        reg1 = self.temp_to_reg[instr.arg1]
        reg2 = self.temp_to_reg[instr.arg2]
        reg_res = self.allocate_reg(instr.dest)
        self.asm.append(f"    mov {reg_res}, 0")
        self.asm.append(f"    cmp {reg1}, {reg2}")
        self.asm.append(f"    setg {self.reg_byte(reg_res)}")

    def emit_geq(self, instr):
        reg1 = self.temp_to_reg[instr.arg1]
        reg2 = self.temp_to_reg[instr.arg2]
        reg_res = self.allocate_reg(instr.dest)
        self.asm.append(f"    mov {reg_res}, 0")
        self.asm.append(f"    cmp {reg1}, {reg2}")
        self.asm.append(f"    setge {self.reg_byte(reg_res)}")

    def emit_lt(self, instr):
        reg1 = self.temp_to_reg[instr.arg1]
        reg2 = self.temp_to_reg[instr.arg2]
        reg_res = self.allocate_reg(instr.dest)
        self.asm.append(f"    mov {reg_res}, 0")
        self.asm.append(f"    cmp {reg1}, {reg2}")
        self.asm.append(f"    setl {self.reg_byte(reg_res)}")

    def emit_leq(self, instr):
        reg1 = self.temp_to_reg[instr.arg1]
        reg2 = self.temp_to_reg[instr.arg2]
        reg_res = self.allocate_reg(instr.dest)
        self.asm.append(f"    mov {reg_res}, 0")
        self.asm.append(f"    cmp {reg1}, {reg2}")
        self.asm.append(f"    setle {self.reg_byte(reg_res)}")

    def emit_eq(self, instr):
        reg1 = self.temp_to_reg[instr.arg1]
        reg2 = self.temp_to_reg[instr.arg2]
        reg_res = self.allocate_reg(instr.dest)
        self.asm.append(f"    mov {reg_res}, 0")
        self.asm.append(f"    cmp {reg1}, {reg2}")
        self.asm.append(f"    sete {self.reg_byte(reg_res)}")

    def emit_neq(self, instr):
        reg1 = self.temp_to_reg[instr.arg1]
        reg2 = self.temp_to_reg[instr.arg2]
        reg_res = self.allocate_reg(instr.dest)
        self.asm.append(f"    mov {reg_res}, 0")
        self.asm.append(f"    cmp {reg1}, {reg2}")
        self.asm.append(f"    setne {self.reg_byte(reg_res)}")

    def emit_param(self, instr):
        self.param_queue.append(instr.arg1)

    def emit_call(self, instr):
        
        if len(self.param_queue) < 2:
            raise RuntimeError("Not enough parameters for printf call")
        fmt = self.param_queue[-2]
        val = self.param_queue[-1]

        if fmt == "fmt_int":
            self.asm.append("    lea rdi, [rel fmt_int]")
        elif fmt == "fmt_str":
            self.asm.append("    lea rdi, [rel fmt_str]")
        else:
            raise RuntimeError(f"Unknown format string: {fmt}")
        # Set value
        if isinstance(val, str) and val.startswith("t"):
            reg = self.temp_to_reg[val]
            self.asm.append(f"    mov rsi, {reg}")
        else:
            # Assume it's a variable name (string label)
            self.asm.append(f"    lea rsi, [rel {val}]")
        self.asm.append("    xor eax, eax")
        self.asm.append(f"    call {instr.arg1}")
        self.param_queue.clear()
        
