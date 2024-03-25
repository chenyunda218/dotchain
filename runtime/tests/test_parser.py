import unittest
from runtime.ast import BoolLiteral, FloatLiteral, IntLiteral, StringLiteral, UnaryExpression
from runtime.interpreter import expression_parser, identifier_or_func_call_parser, literal_parser, try_fun, unary_expression_parser
from runtime.tokenizer import Tokenizer

class TestParser(unittest.TestCase):

    def test_expression_parser(self):
        t = Tokenizer()
        t.init("123")
        t.get_next_token()
        literal = expression_parser(t)
        self.assertIsInstance(literal, IntLiteral)
        self.assertEqual(literal.value, 123)

        t.init("123.1")
        t.get_next_token()
        literal = expression_parser(t)
        self.assertIsInstance(literal, FloatLiteral)
        self.assertEqual(literal.value, 123.1)

        t.init("true")
        t.get_next_token()
        literal = expression_parser(t)
        self.assertIsInstance(literal, BoolLiteral)
        self.assertEqual(literal.value, True)

        t.init("false")
        t.get_next_token()
        literal = expression_parser(t)
        self.assertIsInstance(literal, BoolLiteral)
        self.assertEqual(literal.value, False)

        t.init("+123")
        t.get_next_token()
        literal = expression_parser(t)
        

    def test_unary_expression_parser(self):
        t = Tokenizer()
        t.init("!false")
        t.get_next_token()
        unary = unary_expression_parser(t)
        self.assertEqual(unary.operator, "!")
        self.assertIsInstance(unary, UnaryExpression)
        self.assertIsInstance(unary.expression, BoolLiteral)
        self.assertEqual(unary.expression.value, False)

        t.init("!true")
        t.get_next_token()
        unary = unary_expression_parser(t)
        self.assertEqual(unary.operator, "!")
        self.assertIsInstance(unary, UnaryExpression)
        self.assertIsInstance(unary.expression, BoolLiteral)
        self.assertEqual(unary.expression.value, True)

        t.init("-123")
        t.get_next_token()
        unary = unary_expression_parser(t)
        self.assertEqual(unary.operator, "-")
        self.assertIsInstance(unary, UnaryExpression)
        self.assertIsInstance(unary.expression, IntLiteral)
        self.assertEqual(unary.expression.value, 123)

        t.init("+123")
        t.get_next_token()
        unary = unary_expression_parser(t)
        self.assertEqual(unary.operator, "+")
        self.assertIsInstance(unary, UnaryExpression)
        self.assertIsInstance(unary.expression, IntLiteral)
        self.assertEqual(unary.expression.value, 123)

        t.init("-123.1")
        t.get_next_token()
        unary = unary_expression_parser(t)
        self.assertEqual(unary.operator, "-")
        self.assertIsInstance(unary, UnaryExpression)
        self.assertIsInstance(unary.expression, FloatLiteral)
        self.assertEqual(unary.expression.value, 123.1)
        
        t.init("+123.1")
        t.get_next_token()
        unary = unary_expression_parser(t)
        self.assertEqual(unary.operator, "+")
        self.assertIsInstance(unary, UnaryExpression)
        self.assertIsInstance(unary.expression, FloatLiteral)

    def test_identifier_parser(self):
        t = Tokenizer()
        t.init("hello asdfasd")
        t.get_next_token()
        identifier = identifier_or_func_call_parser(t)
        self.assertEqual(identifier.name, "hello")
        t.get_current_token()
        identifier = identifier_or_func_call_parser(t)
        self.assertEqual(identifier.name, "asdfasd")
    
    def test_literal_parser(self):
        t = Tokenizer()
        t.init("123")
        t.get_next_token()
        literal = literal_parser(t)
        self.assertIsInstance(literal, IntLiteral)
        self.assertEqual(literal.value, 123)

        t.init("123.1")
        t.get_next_token()
        literal = literal_parser(t)
        self.assertIsInstance(literal, FloatLiteral)
        self.assertEqual(literal.value, 123.1)

        t.init("true")
        t.get_next_token()
        literal = literal_parser(t)
        self.assertIsInstance(literal, BoolLiteral)
        self.assertEqual(literal.value, True)

        t.init_and_next("false")
        literal = literal_parser(t)
        self.assertIsInstance(literal, BoolLiteral)
        self.assertEqual(literal.value, False)

        t.init_and_next("\"fwewefwef\"")
        literal = literal_parser(t)
        self.assertIsInstance(literal, StringLiteral)
        self.assertEqual(literal.value, "fwewefwef")

        t.init("fwewefwef")
        t.get_next_token()

    def test_try_fun(self):
        t = Tokenizer()
        t.init_and_next("""() =>""")
        self.assertEqual(try_fun(t), True)

        t.init_and_next("""(a) =>""")
        self.assertEqual(try_fun(t), True)

        t.init_and_next("""(a,b) =>""")
        self.assertEqual(try_fun(t), True)

        t.init_and_next("""(a,b,c) =>""")
        self.assertEqual(try_fun(t), True)

        t.init_and_next("""(123,b,c) =>""")
        self.assertEqual(try_fun(t), False)
        t.init_and_next("""(123,b,c) =>""")
        self.assertEqual(try_fun(t), False)

        t.init_and_next("""(true,b) =>""")
        self.assertEqual(try_fun(t), False)

        t.init_and_next("""(false) =>""")
        self.assertEqual(try_fun(t), False)