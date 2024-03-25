import unittest
from runtime.ast import BoolLiteral, FloatLiteral, IntLiteral, StringLiteral, UnaryExpression
from runtime.interpreter import ExpressionStack
from runtime.tokenizer import Tokenizer

class TestExpressionStack(unittest.TestCase):
    
    def test_push(self):
        t = Tokenizer()
        t.init_and_next("(")

        stack = ExpressionStack(t.clone())
        self.assertEqual(len(stack.tokens), 0)
        self.assertEqual(stack._has_brackets(), False)
        stack.push_token(t.get_current_token())
        self.assertEqual(len(stack.tokens), 1)
        self.assertEqual(stack._has_brackets(), True)

        self.assertEqual(stack.pop().value, "(")
        self.assertEqual(len(stack.tokens), 0)

    def test_pop(self):
        t = Tokenizer()
        t.init_and_next("( +  )")
        stack = ExpressionStack(t.clone())
        stack.push_token(t.get_current_token())
        stack.push_token(t.get_next_token())
        stack.push_token(t.get_next_token())
        self.assertEqual(len(stack.tokens), 3)
        self.assertEqual(stack._has_brackets(), True)
        self.assertEqual(stack.pop().value, ")")
        self.assertEqual(stack.top().value, ")")
        self.assertEqual(stack.pop().value, "+")
        self.assertEqual(stack.top().value, "+")
        self.assertEqual(stack.pop().value, "(")
        self.assertEqual(stack.top().value, "(")
        self.assertEqual(len(stack.tokens), 0)
        self.assertEqual(stack._has_brackets(), False)

    def test_pop_by_brackets(self):
        t = Tokenizer()
        t.init("( +  )")
        stack = ExpressionStack(t.clone())
        stack.push_token(t.get_next_token())
        stack.push_token(t.get_next_token())
        stack.push_token(t.get_next_token())
        self.assertEqual(len(stack.tokens), 3)
        self.assertEqual(stack._has_brackets(), True)
        stack.pop_by_brackets()
        self.assertEqual(stack._has_brackets(), False)

        t.init("( + -  * / % ")
        stack = ExpressionStack(t.clone())
        stack.push_token(t.get_next_token())
        self.assertEqual(stack.top_token().value, "(")
        stack.push_token(t.get_next_token())
        self.assertEqual(stack.top_token().value, "+")
        stack.push_token(t.get_next_token())
        self.assertEqual(stack.top_token().value, "-")
        stack.push_token(t.get_next_token())
        self.assertEqual(stack.top_token().value, "*")
        stack.push_token(t.get_next_token())
        self.assertEqual(stack.top_token().value, "/")
        stack.push_token(t.get_next_token())
        self.assertEqual(stack.top_token().value, "%")
        self.assertEqual(len(stack.tokens), 6)
        stack.pop_by_brackets()
        self.assertEqual(stack._has_brackets(), False)
        self.assertEqual(len(stack.stack), 5)
        self.assertEqual(stack.top().value, "+")

    def test__is_operator(self):
        t = Tokenizer()
        t.init("+ - * / % ( 123 ) false true hello")
        stack = ExpressionStack(t.clone())
        self.assertEqual(stack._is_operator(t.get_next_token()), True)
        self.assertEqual(stack._is_operator(t.get_next_token()), True)
        self.assertEqual(stack._is_operator(t.get_next_token()), True)
        self.assertEqual(stack._is_operator(t.get_next_token()), True)
        self.assertEqual(stack._is_operator(t.get_next_token()), True)
        self.assertEqual(stack._is_operator(t.get_next_token()), True)
        self.assertEqual(stack._is_operator(t.get_next_token()), False)
        self.assertEqual(stack._is_operator(t.get_next_token()), True)
        self.assertEqual(stack._is_operator(t.get_next_token()), False)
        self.assertEqual(stack._is_operator(t.get_next_token()), False)
        self.assertEqual(stack._is_operator(t.get_next_token()), False)

    def test__end(self):
        t = Tokenizer()
        t.init_and_next("asdf;")
        stack = ExpressionStack(t.clone())
        self.assertEqual(stack._end(), False)

        t.init_and_next(";")
        stack = ExpressionStack(t.clone())
        self.assertEqual(stack._end(), True)

        t.init_and_next("")
        stack = ExpressionStack(t.clone())
        self.assertEqual(stack._end(), True)

        t.init_and_next(")")
        stack = ExpressionStack(t.clone())
        self.assertEqual(stack._end(), True)

    def test__top_token_propity(self):
        t = Tokenizer()
        t.init_and_next("+")
        stack = ExpressionStack(t.clone())
        stack.push()
        self.assertEqual(stack.top_token_propity(), 1)

        t.init_and_next("-")
        stack = ExpressionStack(t.clone())
        stack.push()
        self.assertEqual(stack.top_token_propity(), 1)

        t.init_and_next("*")
        stack = ExpressionStack(t.clone())
        stack.push()
        self.assertEqual(stack.top_token_propity(), 2)

        t.init_and_next("/")
        stack = ExpressionStack(t.clone())
        stack.push()
        self.assertEqual(stack.top_token_propity(), 2)


        t.init_and_next("%")
        stack = ExpressionStack(t.clone())
        stack.push()
        self.assertEqual(stack.top_token_propity(), 2)

        t.init_and_next("")
        stack = ExpressionStack(t.clone())
        self.assertEqual(stack.top_token_propity(), 0)

    def test__pop_all_tokens(self):
        t = Tokenizer()
        t.init_and_next("+ - * / %")
        stack = ExpressionStack(t.clone())
        stack.push()
        stack.push()
        stack.push()
        stack.push()
        stack.push()
        # self.assertEqual(len(stack.tokens), 5)

    def test_push_token_and_progress(self):
        t = Tokenizer()
        t.init_and_next("(1 + 2)")
        stack = ExpressionStack(t.clone())
        stack.push()
        self.assertEqual(len(stack.tokens), 1)
        stack.push()
        self.assertEqual(len(stack.stack), 1)
        stack.push()
        self.assertEqual(len(stack.tokens), 2)
        stack.push()
        self.assertEqual(len(stack.stack), 2)
        stack.push()
        self.assertEqual(len(stack.tokens), 0)
        self.assertEqual(len(stack.stack), 3)
        
        t = Tokenizer()
        t.init_and_next("1 + 2 * 4")
        stack = ExpressionStack(t.clone())
        stack.push()
        self.assertEqual(len(stack.stack), 1)
        stack.push()
        self.assertEqual(len(stack.tokens), 1)
        stack.push()
        self.assertEqual(len(stack.stack), 2)
        stack.push()
        self.assertEqual(len(stack.tokens), 2)
        stack.push()
        self.assertEqual(len(stack.stack), 3)

        t = Tokenizer()
        t.init_and_next("1 * 2 + 4")
        stack = ExpressionStack(t.clone())
        stack.push()
        self.assertEqual(len(stack.stack), 1)
        stack.push()
        self.assertEqual(len(stack.tokens), 1)
        stack.push()
        self.assertEqual(len(stack.stack), 2)
        stack.push()
        self.assertEqual(len(stack.tokens), 1)
        self.assertEqual(len(stack.stack), 3)
        stack.push()
        self.assertEqual(len(stack.tokens), 1)
        self.assertEqual(len(stack.stack), 4)

        t = Tokenizer()
        t.init_and_next("1 * (2 + 4)")
        stack = ExpressionStack(t.clone())
        stack.push()
        self.assertEqual(len(stack.stack), 1)
        stack.push()
        self.assertEqual(len(stack.tokens), 1)
        stack.push()
        self.assertEqual(len(stack.stack), 1)
        self.assertEqual(len(stack.tokens), 2)
        stack.push()
        self.assertEqual(len(stack.stack), 2)
        stack.push()
        self.assertEqual(len(stack.tokens), 3)
        self.assertEqual(len(stack.stack), 2)
        stack.push()
        self.assertEqual(len(stack.stack), 3)
        stack.push()
        self.assertEqual(len(stack.tokens), 1)
        self.assertEqual(len(stack.stack), 4)
        