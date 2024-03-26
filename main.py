from runtime.ast import BinaryExpression, Expression
from runtime.interpreter import ExpressionParser, let_expression
from runtime.runtime import Runtime
from runtime.tokenizer import TokenType, Tokenizer, Token
import json

script = """
-123 + -123 /a / 123;
"""



if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    parser = ExpressionParser(t).parse()
    json_object = json.dumps(parser.dict()) 
    # Print JSON object
    print(json_object) 
    