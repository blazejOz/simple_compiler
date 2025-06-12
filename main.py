import subprocess
import argparse
from code_generator.asm_generator import AsmGenerator
from lexical_analysis.lexer import Lexer
from syntax_analysis.parser import Parser
from intermediate_representation.ir_generator import IRGenerator
from intermediate_representation.ir_optimizer import IROptimizer


def main():
    parser = argparse.ArgumentParser(description="Simple Compiler to assembly code")
    parser.add_argument("source", nargs="?", help="Input source file")
    parser.add_argument("--spec", action="store_true", help="Print language specification")
    parser.add_argument("--lex", action="store_true", help="Print lexical analysis")
    parser.add_argument("--par", action="store_true", help="Print syntax analysis")
    parser.add_argument("--ir", action="store_true", help="Print intermediate representation (IR)")
    parser.add_argument("--iro", action="store_true", help="Print optimized intermediate representation (IR)")
    parser.add_argument("--asm", action="store_true", help="Print assembly code")
    parser.add_argument("--all", action="store_true", help="Print all stages and run the program")
    parser.add_argument("--run", action="store_true", help="Compile and run the program")
    args = parser.parse_args()

    if args.spec:
        with open("docs/language_specification.txt", "r") as spec_file:
            print(spec_file.read())

    if args.source:
        with open(args.source, 'r') as file:
            source_code = file.read()
        
        tokens = Lexer(source_code).tokenize()
        ast = Parser(tokens).parse()
        ir = IRGenerator(ast).gen()
        ir_opt = IROptimizer(ir).optimize()
        asm = AsmGenerator(ir_opt).gen()

        if args.lex or args.all:
            print("##### Tokens #####")
            for token in tokens:
                print(token)
        if args.par or args.all:
            print("##### AST #####")
            print(ast)
        if args.ir or args.all:
            print("##### IR #####")
            for instruction in ir:
                print(instruction)
        if args.iro or args.all:
            print("#####Optimized IR#####")
            for instruction in ir_opt:
                print(instruction)
        if args.asm or args.all:
            print("##### ASM #####")
            print(asm)
        
        if args.run or args.all:
            with open("out.asm", "w") as asm_file:
                asm_file.write(asm)
            subprocess.run(["nasm", "-felf64", "out.asm", "-o", "out.o"], check=True)
            subprocess.run(["gcc", "out.o", "-no-pie", "-o", "a.out"], check=True)
            print("Executable 'a.out' generated.")
            print()
            subprocess.run(["./a.out"])
    else:
        repl()

        
def repl():
    print("Compiler REPL mode. Type code and press enter. Empty line = quit.")
    while True:
        src = input(">>> ")
        if not src.strip():
            break
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        ir = IRGenerator(ast).gen()
        asm = AsmGenerator(ir).gen()
        print("ASM:")
        print(asm)
        

if __name__ == "__main__":
    main()
