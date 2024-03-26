
import unittest
from runtime.interpreter import ExpressionParser, StatementParser
from runtime.runtime import Runtime
from runtime.tokenizer import TokenType, Tokenizer,Token

class TestStatementParser(unittest.TestCase):

    def test_parser(self):
        t = Tokenizer()
        t.init("9+(3-1)*3+10/2;")
        parser = StatementParser(t)
        