
class AsmGenreator():
    """
    Generate assembly code using libc library
    """
    def __init__(self, ir_list):
        self.ir_list = ir_list
        self.asm = []

    
    def gen(self):
        self.gen_header()

        for ir in self.ir_list:
            pass

        self.gen_footer()


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