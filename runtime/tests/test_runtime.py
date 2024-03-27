
import unittest
from runtime.interpreter import ExpressionParser
from runtime.ast import PythonRuntime
from runtime.tokenizer import TokenType, Tokenizer,Token

class TestRuntime(unittest.TestCase):

    def test_eval(self):
        t = Tokenizer()
        t.init("9+(3-1)*3+10/2;")
        parser = ExpressionParser(t)
        expression = parser.parse()
        runtime = PythonRuntime()