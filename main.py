import subprocess
from code_generator.asm_generator import AsmGenerator
from lexical_analysis.lexer import Lexer
from syntax_analysis.parser import Parser
from intermediate_representation.ir_generator import IRGenerator
from intermediate_representation.ir_optimizer import IROptimizer


src    = "int x = 5 + 3; x = x * 2; print(\"hello\");"
tokens = Lexer(src).tokenize()
print(tokens)
ast    = Parser(tokens).parse()
print(ast)
ir_instr = IRGenerator(ast).gen()

for innstr in ir_instr:
    print(innstr)

print("###### IR optimized:")
ir_optimized = IROptimizer(ir_instr).optimize()
for innstr in ir_optimized:
    print(innstr)

asm = AsmGenerator(ir_instr).gen()
print(asm)

with open("out.asm", "w") as f:
    f.write(asm)

subprocess.run(["nasm", "-felf64", "out.asm", "-o", "out.o"], check=True)
subprocess.run(["gcc", "out.o", "-no-pie", "-o", "a.out"], check=True)
print("Executable 'a.out' generated.")