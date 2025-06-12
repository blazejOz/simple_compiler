# basic_compiler

A simple compiler written in Python for a basic programming language supporting integers, strings, variables, arithmetic, control flow, and printing.  
The compiler translates source code to x86-64 assembly and produces a native executable.

---

## Features

- **Data types:** `int` (64-bit), `str` (string literals)
- **Statements:** variable declaration, assignment, print, if/else, while loops
- **Expressions:** arithmetic, comparison, variables, literals
- **Comments:** `#` for single-line comments
- **Generates:** x86-64 NASM assembly, links with GCC

---

## Language Example

```c
int x = 5;
while (x > 0) {
    print(x);
    x = x - 1;
}
str msg = "done!";
print(msg);
print("Goodbye!");
```

See [`docs/language_specification.txt`](docs/language_specification.txt) for full details.

---

## Usage

### Compile and run a program

```sh
python main.py myprogram.txt --run
```

### Show language specification

```sh
python main.py --spec
```

### Print intermediate stages

- **Lexical analysis:** `--lex`
- **Syntax analysis:** `--par`
- **Intermediate Representation (IR):** `--ir`
- **Optimized IR:** `--iro`
- **Assembly code:** `--asm`
- **All stages:** `--all`

Example:
```sh
python main.py myprogram.txt --all
```

If no source file is given, you will be prompted to enter a path.

---

## Output

- Assembly: `out.asm`
- Object: `out.o`
- Executable: `a.out`

---

## Requirements

- Python 3.7+
- NASM assembler
- GCC (for linking)

---

## Project Structure

```
basic_compiler/
├── code_generator/           # Assembly code generation
├── docs/                     # Language specification and docs
├── intermediate_representation/ # IR generation and optimization
├── lexical_analysis/         # Lexer and token specification
├── syntax_analysis/          # Parser and AST classes
├── main.py                   # Compiler entry point
├── README.md
```

---

## License

MIT License

---

## Author

blaz
