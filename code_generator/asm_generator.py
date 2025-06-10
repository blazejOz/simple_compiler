class AsmGenerator:
    ARG_REGS = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]

    def __init__(self, ir_list):
        self.ir_list = ir_list
        self.asm = []
        self.temp_to_reg = {}
        self.free_regs = ["r10", "r11", "r12", "r13", "r14", "r15"]
        self.param_queue = []

    def gen(self):
        self.gen_header()
        for instr in self.ir_list:
            handler = getattr(self, f"emit_{instr.op}", None)
            if handler:
                handler(instr)
            else:
                raise NotImplementedError(f"Unsupported IR: {instr.op}")
        self.gen_footer()
        return "\n".join(self.asm)

    def allocate_reg(self, temp):
        if temp in self.temp_to_reg:
            return self.temp_to_reg[temp]
        if not self.free_regs:
            raise RuntimeError("No free registers available")
        reg = self.free_regs.pop(0)
        self.temp_to_reg[temp] = reg
        return reg

    def emit_const(self, instr):
        reg = self.allocate_reg(instr.res)
        self.asm.append(f"    mov {reg}, {instr.arg1}")

    def emit_add(self, instr):
        reg1 = self.temp_to_reg[instr.arg1]
        reg2 = self.temp_to_reg[instr.arg2]
        reg_res = self.allocate_reg(instr.res)
        self.asm.append(f"    mov {reg_res}, {reg1}")
        self.asm.append(f"    add {reg_res}, {reg2}")

    def emit_sub(self, instr):
        reg1 = self.temp_to_reg[instr.arg1]
        reg2 = self.temp_to_reg[instr.arg2]
        reg_res = self.allocate_reg(instr.res)
        self.asm.append(f"    mov {reg_res}, {reg1}")
        self.asm.append(f"    sub {reg_res}, {reg2}")

    def emit_mul(self, instr):
        reg1 = self.temp_to_reg[instr.arg1]
        reg2 = self.temp_to_reg[instr.arg2]
        reg_res = self.allocate_reg(instr.res)
        self.asm.append(f"    mov {reg_res}, {reg1}")
        self.asm.append(f"    imul {reg_res}, {reg2}")

    def emit_div(self, instr):
        # For x86-64, division is more complex (uses rax/rdx)
        reg1 = self.temp_to_reg[instr.arg1]
        reg2 = self.temp_to_reg[instr.arg2]
        reg_res = self.allocate_reg(instr.res)
        self.asm.append(f"    mov rax, {reg1}")
        self.asm.append(f"    cqo")
        self.asm.append(f"    idiv {reg2}")
        self.asm.append(f"    mov {reg_res}, rax")

    def emit_param(self, instr):
        self.param_queue.append(instr.arg1)

    def emit_call(self, instr):
        # Move parameters to argument registers
        for i, p in enumerate(self.param_queue):
            if p == "fmt":
                self.asm.append(f"    lea {self.ARG_REGS[i]}, [rel fmt]")
            else:
                reg = self.temp_to_reg[p]
                self.asm.append(f"    mov {self.ARG_REGS[i]}, {reg}")
        self.asm.append("    xor eax, eax")
        self.asm.append(f"    call {instr.arg1}")
        self.param_queue.clear()

    def gen_header(self):
        self.asm.append("section .data")
        self.asm.append('    fmt: db "%d", 10, 0')
        self.asm.append("")
        self.asm.append("section .text")
        self.asm.append("    global main")
        self.asm.append("    extern printf")
        self.asm.append("")
        self.asm.append("main:")

    def gen_footer(self):
        self.asm.append("    mov rax, 0")
        self.asm.append("    ret")
        self.asm.append("    mov   rax, 0")
        self.asm.append("    ret")