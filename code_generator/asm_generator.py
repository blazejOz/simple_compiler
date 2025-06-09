
class AsmGenreator():
    """
    Generate assembly code using libc library
    """
    def __init__(self, ir_list):
        self.ir_list = ir_list
        self.free_regs = ["r10","r11","r12","r13","r14","r15"]
        self.reg_map = {}
        self.params = []
        self.asm = []

    
    def gen(self):
        self.gen_header()
        for ir in self.ir_list:
            handler = getattr(self, f"emit_{ir.op}", None)
            if handler:
                handler(ir)
            else:
                raise NotImplementedError(f"Nieobslugiwany IR: {ir.op}")
        self.gen_footer()
        return "\n".join(self.asm)

    def allocate_reg(self, temp):
        """
        Allocate a register for a temporary variable.
        If the register is already allocated, return the existing register.
        """
        if temp in self.reg_map:
            return self.reg_map[temp]
        if not self.free_regs:
            raise RuntimeError("No free registers available")
        reg = self.free_regs.pop(0)
        self.reg_map[temp] = reg
        return reg

    def emit_const(self, instr):
        r = self.allocate_reg(instr.res)
        self.asm.append(f"    mov   {r}, {instr.arg1}")

    def emit_param(self, instr):
        self.params.append(instr.arg1)

    ARG_REGS = ["rdi","rsi","rdx","rcx","r8","r9"]

    def emit_call(self, instr):
        """
        Emit a call instruction.
        This function handles the preparation of parameters and the call to the function.
        """
        for i, p in enumerate(self.params):
            if p == "fmt":
                # first param is always the format string
                self.asm.append("    lea   rdi, [rel fmt]")
            else:
                reg = self.reg_map[p]            
                target = self.ARG_REGS[i]             
                self.asm.append(f"    mov   {target}, {reg}")
        self.asm.append("    xor   eax, eax")
        self.asm.append(f"    call  {instr.arg1}")
        self.params.clear()

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
        self.asm.append("    mov   rax, 0")
        self.asm.append("    ret")