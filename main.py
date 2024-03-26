from runtime.ast import BinaryExpression, Expression
from runtime.interpreter import ExpressionParser, let_expression
from runtime.runtime import Runtime
from runtime.tokenizer import TokenType, Tokenizer, Token
import json

script = """
let hell = -a() + 3/ -b();
"""



if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    parser = let_expression(t)
    json_object = json.dumps(parser.dict()) 
    # Print JSON object
    print(json_object) 
    