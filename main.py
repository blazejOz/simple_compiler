from lexical_analysis.lexer import Lexer
from syntax_analysis.parser import Parser
from intermediate_representation.ir_generator import IRGenerator


src    = "print(1+2*3)"
tokens = Lexer(src).tokenize()
# print(tokens)
ast    = Parser(tokens).parse()
print(ast)
ir_instr = IRGenerator(ast).gen()

for innstr in ir_instr:
    print(innstr)
