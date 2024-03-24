import unittest
from runtime.ast import BoolLiteral, FloatLiteral, IntLiteral, StringLiteral
from runtime.interpreter import literal_parser
from runtime.tokenizer import Tokenizer

class TestParser(unittest.TestCase):
    
    def test_literal_parser(self):
        t = Tokenizer()

        t.init("123")
        t.get_next_token()
        literal = literal_parser(t)
        self.assertEqual(isinstance(literal, IntLiteral), True)
        self.assertEqual(literal.value, 123)

        t.init("123.1")
        t.get_next_token()
        literal = literal_parser(t)
        self.assertEqual(isinstance(literal, FloatLiteral), True)
        self.assertEqual(literal.value, 123.1)

        t.init("true")
        t.get_next_token()
        literal = literal_parser(t)
        self.assertEqual(isinstance(literal, BoolLiteral), True)
        self.assertEqual(literal.value, True)

        t.init("false")
        t.get_next_token()
        literal = literal_parser(t)
        self.assertEqual(isinstance(literal, BoolLiteral), True)
        self.assertEqual(literal.value, False)

        t.init("\"fwewefwef\"")
        t.get_next_token()
        literal = literal_parser(t)
        self.assertEqual(isinstance(literal, StringLiteral), True)
        self.assertEqual(literal.value, "fwewefwef")

        t.init("fwewefwef")
        t.get_next_token()