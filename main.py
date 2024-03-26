

from runtime.interpreter import ExpressionParser
from runtime.runtime import Runtime
from runtime.tokenizer import TokenType, Tokenizer, Token
import json

script = """
1 + 2 * 3 - 4 / 5;
"""

if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    parser = ExpressionParser(t)
    # parser.push_token(Token(TokenType.LEFT_PAREN, "(", 0, 0, 1, 0))
    expression = parser.parse()
    # print(expression.dict())