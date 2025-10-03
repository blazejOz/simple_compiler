import unittest
from src.lexical_analysis.lexer import Lexer
from src.lexical_analysis.token import Token

class TestLexer(unittest.TestCase):
    def test_basic_tokens(self):
        source = "int x = 42\n"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        kinds = [tok.kind for tok in tokens]
        self.assertIn("ID", kinds)
        self.assertIn("CONST", kinds)
        self.assertIn("NEWLINE", kinds)
        self.assertIn("EOF", kinds)

    def test_operators_and_assignment(self):
        source = "x = y + 2 * 3;"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        kinds = [tok.kind for tok in tokens]
        self.assertIn("ID", kinds)
        self.assertIn("CONST", kinds)
        self.assertIn("ASSIGN", kinds)
        self.assertIn("PLUS", kinds)
        self.assertIn("MUL", kinds)
        self.assertIn("SEMI", kinds)

    def test_comments_and_whitespace(self):
        source = "int x = 1; // this is a comment\nx = x + 2;"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        kinds = [tok.kind for tok in tokens]
        self.assertIn("COMMENT", kinds)
        self.assertIn("NEWLINE", kinds)
        self.assertIn("ID", kinds)
        self.assertIn("CONST", kinds)

    def test_multiple_lines(self):
        source = "int a = 1;\nint b = 2;\n"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        newlines = [tok for tok in tokens if tok.kind == "NEWLINE"]
        self.assertEqual(len(newlines), 2)

    def test_error_handling(self):
        source = "int x = @"
        lexer = Lexer(source)
        with self.assertRaises(RuntimeError):
            lexer.tokenize()

    def test_token_positions(self):
        source = "int x = 42\n"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        # Check that line and column are tracked
        for tok in tokens:
            self.assertIsInstance(tok.line, int)
            self.assertIsInstance(tok.col, int)

if __name__ == "__main__":
    unittest.main()