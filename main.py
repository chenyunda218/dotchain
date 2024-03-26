from runtime.ast import BinaryExpression, Expression
from runtime.interpreter import ExpressionParser
from runtime.runtime import Runtime
from runtime.tokenizer import TokenType, Tokenizer, Token
import json

script = """
9+(3-1)*3+10/2;
"""



if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    parser = ExpressionParser(t)
    # parser.push_token(Token(TokenType.LEFT_PAREN, "(", 0, 0, 1, 0))
    expression = parser.parse()
    json_object = json.dumps(expression.dict()) 
    # Print JSON object
    print(json_object) 
