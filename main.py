from lexical_analysis.lexer import Lexer
from syntax_analysis.parser import Parser
from intermediate_representation.ir_generator import IRGenerator


src    = "print(123)"
tokens = Lexer(src).tokenize()
ast    = Parser(tokens).parse()
ir_instr = IRGenerator(ast).gen()

print(ir_instr)
