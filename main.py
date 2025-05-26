from lexical_analysis.lexer import Lexer
from syntax_analysis.parser import Parser

src    = "print(123)"
tokens = Lexer(src).tokenize()
ast    = Parser(tokens).parse()
print(ast)    # powinno wypisać: PrintStmt(NumberExpr(123))
