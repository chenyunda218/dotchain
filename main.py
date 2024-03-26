

from runtime.interpreter import ExpressionParser, ExpressionStack, expression_parser
from runtime.runtime import Runtime
from runtime.tokenizer import TokenType, Tokenizer, Token
import json

script = """
(!hello);
"""

if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    parser = ExpressionParser(t)
    # parser.push_token(Token(TokenType.LEFT_PAREN, "(", 0, 0, 1, 0))
    expression = parser.parse()
    # print(expression.dict())
    parser._debug_print_stack()
    parser._debug_print_tokens()